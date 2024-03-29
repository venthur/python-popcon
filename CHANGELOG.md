# Changelog

## [3.0.3] - 2022-06-29

* bumped version to allow for source-only upload in debian

## [3.0.2] - 2022-06-26

* bumped version to allow to migrate to Debian/testing (no changes)

## [3.0.1] - 2022-05-30

* Improved tabular output, for long package names
* Added the sum for verbose output

## [3.0.0] - 2022-05-29

* Removed functions deprecated since 2.0.1
* bumped minimim Python version to 3.7
* Added Python 3.10 to test suite
* use HTTPS everywhere
* updated dev dependencies
* Improved output and added verbose output
* Use argparse for CLI
* test the CLI

## [2.0.4] - 2021-08-08

* updated build system
* updated debian's build system
* use github actions instead of travis
* bumped minimal Python version to 3.6

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
