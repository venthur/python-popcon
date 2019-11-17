#!/usr/bin/env python


"""Get Debian popcon values for given packages.

The usage of this module is easy:

    >>> import popcon
    >>> popcon.package('reportbug-ng')
    {'reportbug-ng': 323}
    >>> popcon.package('reportbug-ng', 'reportbug')
    {'reportbug-ng': 323, 'reportbug': 75065}

The raw data (vote, old, recent, no-file) is also available, the sum of
the raw numbers is the number of installations as reported by
`popcon.package`.

    >>> popcon.package_raw('reportbug-ng', 'reportbug')
    {'reportbug-ng': Package(vote=50, old=187, recent=86, no_files=0),
            'reportbug': Package(vote=5279, old=59652, recent=10118,
            no_files=16)}

Behind the scene popcon will try to use cached information saved in a
file in the ~/.cache/popcon directory. If the relevant file is not
available, or older than `EXPIRY` seconds (default is 7 days) it will
download fresh data and save that.

The cached data will be kept in memory unless `KEEP_DATA` is set to
False.

"""


import warnings
import time
from urllib.request import Request, urlopen
import gzip
import io
import tempfile
import pickle
import os
import collections
import logging


logger = logging.getLogger(__name__)


XDG_CACHE_HOME = os.environ.get('XDG_CACHE_HOME',
                                os.path.expandvars('$HOME/.cache'))

__author__ = 'Bastian Venthur <venthur@debian.org>'

Package = collections.namedtuple(
    "Package", ["vote", "old", "recent", "no_files"])


# week in seconds
EXPIRY = 86400 * 7
KEEP_DATA = True
cached_data = {}
cached_timestamp = {}


def _fetch(url):
    """Fetch all popcon results and return unparsed data.

    Parameters
    ----------
    url : str
        the url of the gzipped popcon results

    Returns
    -------
    txt : str
        the uncompressed data

    """
    request = Request(url)
    response = urlopen(request)
    txt = response.read()
    response.close()
    txt = _decompress(txt)
    return txt


def _parse(results):
    """Parse all-popcon-results file.

    Parameters
    ----------
    results : str
        the results file

    Returns
    -------
    ans : dict
        package name -> `Package` namedtuple mapping, containing the
        package information

    """
    ans = dict()
    results = results.splitlines()
    for line in results:
        elems = line.split()
        if elems[0] != b"Package:":
            continue
        ans[elems[1]] = Package(*(int(i) for i in elems[2:]))
    return ans


def _parse_stats(results):
    """Parse "statistics" files.

    Parameters
    ----------
    results : str
        the results file

    Returns
    -------
    ans : dict
        package name -> `Package` namedtuple mapping, containing the
        package information

    """
    ans = dict()
    results = results.splitlines()
    for line in results:
        elems = line.split()
        try:
            int(elems[0])
            int(elems[2])  # e.g. skip pass the "not in sid" pseudo-package
            if elems[1] == b"Total":
                continue
        except Exception:
            continue
        ans[elems[1]] = Package(*(int(i) for i in elems[3:]))
    return ans


def _decompress(compressed):
    """Decompress a gzipped string.

    Parameters
    ----------
    compressed : str
        the compressed string

    Returns
    -------
    data : str
        the uncompressed string

    """
    gzippedstream = io.BytesIO(compressed)
    gzipper = gzip.GzipFile(fileobj=gzippedstream)
    data = gzipper.read()
    return data


def package(*package_list):
    """Return the number of installations.

    The return value is a dict where the keys are the packages and the
    values the number of installations. If a package was not found it is
    not in the dict.

    This function is deprecated, please use `packages` instead.

    Parameters
    ----------
    package_list : tuple of strings
        the package names

    Returns
    -------
    ans : dict
        packagename -> number of installations mapping

    """
    logger.warning('package is deprecated, please use packages instead')
    return packages(*package_list)


def packages(package_list):
    """Return the number of installations.

    The return value is a dict where the keys are the packages and the
    values the number of installations. If a package was not found it is
    not in the dict.

    Parameters
    ----------
    package_list : list of strings
        the package names

    Returns
    -------
    ans : dict
        packagename -> number of installations mapping

    """
    raw = packages_raw(package_list)
    ans = dict()
    for pkg, values in list(raw.items()):
        ans[pkg] = sum(values)
    return ans


def source_package(*package_list):
    """Return the number of installations, for source packages.

    See `package` for the format of the returned data.

    At present, this is only an approximation that instead gives the
    maximum value, out of the number of installations of any binary
    package belonging to each source package.

    This function is deprecated, please use `source_packages` instead.

    Parameters
    ----------
    package_list : tuple of strings
        the package names

    Returns
    -------
    ans : dict
        packagename -> number of installations mapping

    """
    logger.warning(
            'source_package is deprecated, please use source_packages instead')
    return source_packages(*package_list)


def source_packages(package_list):
    """Return the number of installations, for source packages.

    See `package` for the format of the returned data.

    At present, this is only an approximation that instead gives the
    maximum value, out of the number of installations of any binary
    package belonging to each source package.

    Parameters
    ----------
    package_list : list of strings
        the package names

    Returns
    -------
    ans : dict
        packagename -> number of installations mapping

    """
    raw = source_packages_raw(package_list)
    ans = dict()
    for pkg, values in list(raw.items()):
        ans[pkg] = sum(values)
    return ans


def package_raw(*package_list):
    """Return the raw popcon values for the given packages.

    The return value is a dict where the keys are the packages and the
    values a named tuple of integers: (vote, old, recent, no-files)

    * vote: number of people who use this package regulary
    * old: is the number of people who installed, but don't use this
      package regularly
    * recent: is the number of people who upgraded this package recently
    * no-files: is the number of people whose entry didn't contain
      enough information (atime and ctime were 0)

    This function is deprecated, please use `packages_raw` instead.

    Parameters
    ----------
    package_list : tuple of strings
        the package names

    Returns
    -------
    ans : dict

    """
    logger.warning(
            'package_raw is deprecated, please use packages_raw instead')
    return packages_raw(*package_list)


def packages_raw(package_list):
    """Return the raw popcon values for the given packages.

    The return value is a dict where the keys are the packages and the
    values a named tuple of integers: (vote, old, recent, no-files)

    * vote: number of people who use this package regulary
    * old: is the number of people who installed, but don't use this
      package regularly
    * recent: is the number of people who upgraded this package recently
    * no-files: is the number of people whose entry didn't contain
      enough information (atime and ctime were 0)

    Parameters
    ----------
    package_list : list of strings
        the package names

    Returns
    -------
    ans : dict

    """
    return _packages_raw_generic(
        "http://popcon.debian.org/all-popcon-results.txt.gz",
        _parse, "debian", package_list)


def source_package_raw(*package_list):
    """Return the raw popcon values for the given source packages.

    See `package_raw` for the format of the returned data.

    At present, this is only an approximation that instead gives the
    maximum value, out of the number of installations of any binary
    package belonging to each source package.

    This function is deprecated, please use `source_packages_raw` instead.

    Parameters
    ----------
    package_list : tuple of strings

    Returns
    -------
    ans : dict

    """
    logger.warning('source_package_raw is deprecated, please use'
                   ' source_packages_raw  instead')
    return source_packages_raw(*package_list)


def source_packages_raw(package_list):
    """Return the raw popcon values for the given source packages.

    See `package_raw` for the format of the returned data.

    At present, this is only an approximation that instead gives the
    maximum value, out of the number of installations of any binary
    package belonging to each source package.

    Parameters
    ----------
    package_list : list of strings

    Returns
    -------
    ans : dict

    """
    return _packages_raw_generic(
        "http://popcon.debian.org/sourcemax/by_inst.gz",
        _parse_stats, "debian-sourcemax", package_list)


def _packages_raw_generic(url, parse, key, package_list):
    """The work mule

    Parameters
    ----------
    url : str
        the url to use
    parse : function
        the parser function
    key : str
        "debian-sourcemax" or "debian"
    package_list : list of strings
        the debian package names

    Returns
    -------
    ans : dict

    """
    global cached_data, cached_timestamp
    # implements BASEDIRSPEC
    # http://standards.freedesktop.org/basedir-spec/basedir-spec-0.6.html
    dumpfile = os.path.join(
        XDG_CACHE_HOME,
        'popcon',
        "%s.%s" % (key, pickle.format_version))

    earliest_possible_mtime = max(
        time.time() - EXPIRY,
        os.stat(__file__).st_mtime)

    if (key in cached_data
            and cached_timestamp.get(key, 0) <= earliest_possible_mtime):
        del cached_data[key]

    data = cached_data.get(key, None)
    if (data is None
            and os.path.exists(dumpfile)
            and os.stat(dumpfile).st_mtime > earliest_possible_mtime):
        try:
            with open(dumpfile, 'rb') as fh:
                data = pickle.load(fh)
            cached_timestamp[key] = os.stat(dumpfile).st_mtime
        except Exception:
            import traceback
            warnings.warn("Problems loading cache file: %s" % dumpfile)
            traceback.print_exc()

    if data is None:
        data = _fetch(url)
        data = parse(data)
        # i still think that makedirs should behave like mkdir -p
        if not os.path.isdir(os.path.dirname(dumpfile)):
            os.makedirs(
                os.path.dirname(dumpfile),
                mode=0o700)  # mode according to BASEDIRSPEC
        # as soon as python2.6 is in stable, we can use delete=False
        # here and replace the flush/rename/try:close sequence with the
        # cleaner close/rename.
        temp = tempfile.NamedTemporaryFile(dir=os.path.dirname(dumpfile))
        pickle.dump(data, temp)
        temp.flush()
        os.rename(temp.name, dumpfile)
        try:
            temp.close()
        except OSError:
            pass
        cached_timestamp[key] = time.time()
    ans = dict()
    for pkg in package_list:
        # Lookup using bytestrings, but always index results by the
        # original so that callsites can look it up.
        lookup = pkg if isinstance(pkg, bytes) else pkg.encode('utf-8')
        if lookup in data:
            ans[pkg] = data[lookup]
    if KEEP_DATA:
        cached_data[key] = data
    return ans
