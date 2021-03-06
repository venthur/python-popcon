# Changelog

## [2.0.3] - 2020-02-11

* Fixed missing version bump

## [2.0.2] - 2020-02-11

* Fixed main script to use the new-style functions introduced in 2.0.1
* Import new-style functions in __init__.py

## [2.0.1] - 2019-11-17

* deprecated functions with packages as positional arguments, the new ones use
  list of packages instead
* removed useles requirements.txt
* added html report to coverage


## [2.0.0] - 2019-01-13

* Dropped Python2 support
* moved to pytest
* added Makefile, setup.cfg, flake8
* Fixed lots of pep8 errors

## [1.5.1] - 2018-02-17

* Fixed __main__ handling in __main__.py

## [1.5.0] - 2017-11-04

* Updated packaging (setup.py, etc)
* Added popcon CLI for direct queries from the command line
* Removed dependency from xdg
* Added Travis CI
* Added unit tests
* Added changelog, license, readme
