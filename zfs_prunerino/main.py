#!/usr/bin/env python3
import subprocess, time, argparse, sys

def parse_args():
    parser = argparse.ArgumentParser(description='Simple tool to prune zfs snapshots. Will output a list of snapshots that can be destroyed according to the grid.')
    parser.add_argument('--prefix', type=str, required=False, help='Prefix of datasets to prune. Example: /zfs-root/backups/', default='')
    parser.add_argument('--verbose', action='store_true', help='If set, details will be printed to stderr')
    parser.add_argument('grid', type=str, help='Comma-separated grid of snapshots to keep. Each entry specifies the number of snapshots to keep for this interval. Example: 23h,6d,3w,11m,10y')
    return parser.parse_args()

def generate_desired_timestamps(grid_str):
  deltas = {
    "h": 60 * 60,
    "d": 60 * 60 * 24,
    "w": 60 * 60 * 24 * 7,
    "m": 60 * 60 * 24 * 30,
    "y": 60 * 60 * 24 * 365
  }

  current_timestamp = int(time.time())
  plan = [ { 'timestamp': current_timestamp, 'name': 'now' } ];
  grid = grid_str.split(',')
  for g in grid:
    kind = g[-1]
    if not kind in deltas:
      raise Exception("Unknown kind: " + kind)
    delta = deltas[kind]
    length = int(g[0:-1])
    for i in range(1, length + 1):
      plan.append({ 'timestamp': current_timestamp - i * delta, 'name': str(i) + kind })

  return plan

def list_snapshots(prefix):
  snapshots = { }
  result = subprocess.run(["zfs", "get", "creation", "-t", "snapshot", "-p", "-H" ],
    capture_output=True, text=True, check=True)
  for line in result.stdout.split('\n'):
    if line.strip() == "":
      continue
    [ name, _, timestamp, *_ ] = line.split('\t')
    if not name.startswith(prefix):
      continue
    [ dataset, snapshot ] = name.split('@')
    if not dataset in snapshots:
      snapshots[dataset] = [ ]
    snapshots[dataset].append({ "name": snapshot, "timestamp": int(timestamp), "matches": [ ] })

  return snapshots

def main():
    args = parse_args()
    plan = generate_desired_timestamps(args.grid)
    snapshots = list_snapshots(args.prefix)

    # find snapshots to keep
    for dataset, snapshots in snapshots.items():
      for p in plan:
        # find the closest snapshot to this desired timestamp
        snapshots.sort(key=lambda x: abs(x["timestamp"] - p["timestamp"]))
        snapshots[0]["matches"].append(p["name"])

      for snapshot in snapshots:
        if args.verbose:
          print(f"{dataset}@{snapshot['name']}", "matches:",
                ",".join(snapshot["matches"]) if snapshot['matches'] else "nothing and can be pruned",
                file=sys.stderr)
        if not snapshot["matches"]:
          print(f"{dataset}@{snapshot['name']}")

if __name__ == '__main__':
    main()
