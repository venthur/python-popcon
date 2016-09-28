#!/usr/bin/env python

# popcon.py -
# Copyright (C) 2010-2015  Bastian Venthur
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

# relevant specifications:
# * BASEDIRSPEC: http://standards.freedesktop.org/basedir-spec/basedir-spec-0.6.html


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

Behind the scences popcon will try to use cached infomation saved in a
file in the ~/.cache/popcon directory. If the relevant file is not
available, or older than `EXPIRY` seconds (default is 7 days) it will
download fresh data and save that.

The cached data will be kept in memory unless `KEEP_DATA` is set to
False.

"""

from __future__ import division, print_function

import warnings
import time
try:
    # python2
    from urllib2 import Request, urlopen
except ImportError:
    # python3
    from urllib.request import Request, urlopen
import gzip
try:
    # python2
    import StringIO as io
except ImportError:
    # python3
    import io
import tempfile
try:
    # python2
    import cPickle as pickle
except ImportError:
    # python3
    import pickle
import os
import collections

import xdg.BaseDirectory


__author__ = 'Bastian Venthur <venthur@debian.org>'
__version__ = '1.4'

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
        except:
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
    try:
        # python2
        gzippedstream = io.StringIO(compressed)
    except TypeError:
        # python3
        gzippedstream = io.BytesIO(compressed)
    gzipper = gzip.GzipFile(fileobj=gzippedstream)
    data = gzipper.read()
    return data


def package(*packages):
    """Return the number of installations.

    The return value is a dict where the keys are the packages and the
    values the number of installations. If a package was not found it is
    not in the dict.

    Parameters
    ----------
    packages : tuple of strings
        the package names

    Returns
    -------
    ans : dict
        packagename -> number of installations mapping

    """
    raw = package_raw(*packages)
    ans = dict()
    for pkg, values in list(raw.items()):
        ans[pkg] = sum(values)
    return ans


def source_package(*packages):
    """Return the number of installations, for source packages.

    See `package` for the format of the returned data.

    At present, this is only an approximation that instead gives the
    maximum value, out of the number of installations of any binary
    package belonging to each source package.

    Parameters
    ----------
    packages : tuple of strings
        the package names

    Returns
    -------
    ans : dict
        packagename -> number of installations mapping

    """
    raw = source_package_raw(*packages)
    ans = dict()
    for pkg, values in list(raw.items()):
        ans[pkg] = sum(values)
    return ans


def package_raw(*packages):
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
    packages : tuple of strings
        the package names

    Returns
    -------
    ans : dict

    """
    return _package_raw_generic(
        "http://popcon.debian.org/all-popcon-results.txt.gz",
        _parse, "debian", *packages)


def source_package_raw(*packages):
    """Return the raw popcon values for the given source packages.

    See `package_raw` for the format of the returned data.

    At present, this is only an approximation that instead gives the
    maximum value, out of the number of installations of any binary
    package belonging to each source package.

    Parameters
    ----------
    packages : tuple of strings

    Returns
    -------
    ans : dict

    """
    return _package_raw_generic(
        "http://popcon.debian.org/sourcemax/by_inst.gz",
        _parse_stats, "debian-sourcemax", *packages)


def _package_raw_generic(url, parse, key, *packages):
    """The work mule

    Parameters
    ----------
    url : str
        the url to use
    parse : function
        the parser function
    key : str
        "debian-sourcemax" or "debian"
    packages : tuple of strings
        the debian package names

    Returns
    -------
    ans : dict

    """
    global cached_data, cached_timestamp
    dumpfile = os.path.join(
        xdg.BaseDirectory.xdg_cache_home,
        'popcon',
        "%s.%s" % (key, pickle.format_version))  # implements BASEDIRSPEC

    earliest_possible_mtime = max(
        time.time() - EXPIRY,
        os.stat(__file__).st_mtime)

    if key in cached_data and cached_timestamp.get(key, 0) <= earliest_possible_mtime:
        del cached_data[key]

    data = cached_data.get(key, None)
    if data is None and os.path.exists(dumpfile) and os.stat(dumpfile).st_mtime > earliest_possible_mtime:
        try:
            with open(dumpfile, 'rb') as fh:
                data = pickle.load(fh)
            cached_timestamp[key] = os.stat(dumpfile).st_mtime
        except:
            import traceback
            warnings.warn("Problems loading cache file: %s" % dumpfile)
            traceback.print_exc()

    if data is None:
        data = _fetch(url)
        data = parse(data)
        if not os.path.isdir(os.path.dirname(dumpfile)):  # i still think that makedirs should behave like mkdir -p
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
    for pkg in packages:
        # Lookup using bytestrings, but always index results by the original so
        # that callsites can look it up.
        lookup = pkg if isinstance(pkg, bytes) else pkg.encode('utf-8')
        if lookup in data:
            ans[pkg] = data[lookup]
    if KEEP_DATA:
        cached_data[key] = data
    return ans


if __name__ ==  "__main__":
    print(package('reportbug-ng'))
    print(source_package('reportbug-ng', 'reportbug'))
    print(package('reportbug-ng', 'reportbug'))
