#!/usr/bin/env python

# popcon.py -
# Copyright (C) 2010-2011  Bastian Venthur
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

The raw data (vote, old, recent, no-file) is also available, the sum of the raw
numbers is the number of installations as reported by `popcon.package`.

    >>> popcon.package_raw('reportbug-ng', 'reportbug')
    {'reportbug-ng': Package(vote=50, old=187, recent=86, no_files=0), 'reportbug': Package(vote=5279, old=59652, recent=10118, no_files=16)}

Behind the scences popcon will try to use cached infomation saved in
`DUMPFILE`. If that file is not available, or older than `EXPIRY` seconds
(default is 7 days) it will download fresh data and save that into `DUMPFILE`.

The cached data will be kept in memory unless `KEEP_DATA` is set to False.
"""

__author__ = 'Bastian Venthur <venthur@debian.org>'


import warnings
import time
import urllib2
import gzip
import StringIO
import tempfile
import cPickle as pickle
import os
import collections

import xdg.BaseDirectory

try:
    Package = collections.namedtuple("Package", ["vote", "old", "recent", "no_files"])
except AttributeError:
    Package = lambda *args: tuple(args)

# week in seconds
EXPIRY = 86400 * 7
DUMPFILE = os.path.join(xdg.BaseDirectory.xdg_cache_home, 'popcon', 'debian') # implements BASEDIRSPEC
RESULTS_URL = "http://popcon.debian.org/all-popcon-results.txt.gz"
KEEP_DATA = True
cached_data = None
cached_timestamp = None

def _fetch():
    """Fetch all popcon results and return unparsed data."""
    request = urllib2.Request(RESULTS_URL)
    response = urllib2.urlopen(request)
    txt = response.read()
    response.close()
    txt = _decompress(txt)
    return txt

def _parse(results):
    """Parse all-popcon-results file."""
    ans = dict()
    results = results.splitlines()
    for line in results:
        elems = line.split()
        if elems[0] != "Package:":
            continue
        ans[elems[1]] = Package(*(int(i) for i in elems[2:]))
    return ans

def _decompress(compressed):
    """Decompress a gzipped string."""
    gzippedstream = StringIO.StringIO(compressed)
    gzipper = gzip.GzipFile(fileobj=gzippedstream)
    data = gzipper.read()
    return data

def package(*packages):
    """Return the number of installations.

    The return value is a dict where the keys are the packages and the values
    the number of installations. If a package was not found it is not in the
    dict.
    """
    raw = package_raw(*packages)
    ans = dict()
    for pkg, values in raw.iteritems():
        ans[pkg] = sum(values)
    return ans

def package_raw(*packages):
    """Return the raw popcon values for the given packages.

    The return value is a dict where the keys are the packages and the values a
    named tuple of integers: (vote, old, recent, no-files)

        vote: number of people who use this package regulary
        old: is the number of people who installed, but don't use this package 
             regularly
        recent: is the number of people who upgraded this package recently
        no-files: is the number of people whose entry didn't contain enough 
                  information (atime and ctime were 0)
    """
    global cached_data, cached_timestamp

    earliest_possible_mtime = max(time.time() - EXPIRY, os.stat(__file__).st_mtime)

    if cached_data is not None and cached_timestamp <= earliest_possible_mtime:
        cached_data = None

    data = cached_data
    if data is None and os.path.exists(DUMPFILE) and os.stat(DUMPFILE).st_mtime > earliest_possible_mtime:
        try:
            handle = open(DUMPFILE, 'r')
            data = pickle.load(handle)
            handle.close()
            cached_timestamp = os.stat(DUMPFILE).st_mtime
        except:
            warnings.warn("Problems loading cache file: %s"%e)

    if data is None:
        data = _fetch()
        data = _parse(data)
        if not os.path.isdir(os.path.dirname(DUMPFILE)): # i still think that makedirs should behave like mkdir -p
            os.makedirs(os.path.dirname(DUMPFILE), mode=0700) # mode according to BASEDIRSPEC
        # as soon as python2.6 is in stable, we can use delete=False here and
        # replace the flush/rename/try:close sequence with the cleaner
        # close/rename.
        temp = tempfile.NamedTemporaryFile(dir=os.path.dirname(DUMPFILE))
        pickle.dump(data, temp)
        temp.flush()
        os.rename(temp.name, DUMPFILE)
        try:
            temp.close()
        except OSError:
            pass
        cached_timestamp = time.time()
    ans = dict()
    for pkg in packages:
        if pkg in data:
            ans[pkg] = data[pkg]
    if KEEP_DATA:
        cached_data = data
    return ans

