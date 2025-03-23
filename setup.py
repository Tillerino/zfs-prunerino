from setuptools import setup

with open("README.md", 'r') as f:
  long_description = f.read()

setup(
  name='zfs-prunerino',
  version='0.1',
  description='Simple tool to prune zfs snapshots with spaced retention',
  license="Apache License 2.0",
  long_description=long_description,
  author='Tillmann Gaida',
  author_email='tillmann.gaida@gmail.com',
  url="https://github.com/Tillerino/zfs-prunerino",
  packages=['zfs_prunerino'],
  install_requires=[], #none
  entry_points={'console_scripts': [
    'zfs-prunerino = zfs_prunerino.main:main',
  ]}
)
