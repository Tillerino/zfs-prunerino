from setuptools import setup

with open("README.md", 'r') as f:
  long_description = f.read()

setup(
  name='zfs-prunerino',
  version='1.0',
  description='TODO',
  license="MIT",
  long_description=long_description,
  author='TODO',
  author_email='TODO',
  url="TODO",
  packages=['zfs-prunerino'],  #same as name
  install_requires=[], #none
  entry_points={'console_scripts': [
    'zfs-prunerino = zfs_prunerino:main',
  ]}
)
