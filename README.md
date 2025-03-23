# zfs-prunerino
Simple tool to prune zfs snapshots with spaced retention

I looked at a few tools to create, transfer and prune zfs snapshots.
Most are really complex, typically requiring global configuration and background processes.
At the same time, they are often very opinionated.
I prefer small, composable tools.

`zfs-prunerino 23h,6d,3w,11m,10y | xargs -n 1 sudo zfs destroy`

## Pruning snapshots

Snapshots are often kept based on rules like:
- keep daily snapshots for 7 days
- keep weekly snapshots for 4 weeks
- keep monthly snapshots for 12 months
- keep yearly snapshots for 7 years

This is very simple to implement if you can either:
- align the grid to the time, e.g. always make snapshots at 00:00, all monthly snapshots at the 1st of the month, and so on
- mark your snapshots as `daily`/`weekly`/... when they are created

Both are possible, but have a big effect on _creating_ snapshots.
What if you wanted to create snapshots willy-nilly, but still prune them?

zfs-prunerino follows a very simple approach:
- Based on the given rules, lay out a list of timestamps where there _should_ be snapshots.
- For each of those, find the closest snapshot and mark it.
- Prune all other snapshots.

As time progresses, this will result in a _reasonably_ spaced list of snapshots.

## Usage

zfs-prunerino outputs a list of snapshots to destroy.
Dry-run? Manage sudo? No thank you. It's your setup, you know best.
Just stick the output into how ever you want to destroy snapshots.

Simple: `zfs-prunerino 23h,6d,3w,11m,10y | xargs -n 1 sudo zfs destroy`

Complex:
- Look at the output of `zfs-prunerino` for a "dry run"
- `--verbose` will print the matching between timestamps and snapshots to stdout
- `--prefix` will prefix filter for datasets with the given prefix
