# python-popcon

Get Debian [popularity contest](https://popcon.debian.org/) values for given
packages.


## Installation

```bash
$ pip install popcon
```


## Usage

The usage of this module is easy:

```python
>>> import popcon
>>> popcon.packages(['reportbug-ng'])
{'reportbug-ng': 323}
>>> popcon.packages(['reportbug-ng', 'reportbug'])
{'reportbug-ng': 323, 'reportbug': 75065}
```

The raw data (vote, old, recent, no-file) is also available, the sum of the raw
numbers is the number of installations as reported by `popcon.package`.

```python
>>> popcon.packages_raw(['reportbug-ng', 'reportbug'])
{'reportbug-ng': Package(vote=50, old=187, recent=86, no_files=0),
 'reportbug': Package(vote=5279, old=59652, recent=10118, no_files=16)}
```

Behind the scene popcon will try to use cached information saved in a file in
the ~/.cache/popcon directory. If the relevant file is not available, or older
than `EXPIRY` seconds (default is 7 days) it will download fresh data and save
that.

The cached data will be kept in memory unless `KEEP_DATA` is set to False.


## Command Line Interface

```
$ popcon reportbug
{'reportbug': 177670}
```
