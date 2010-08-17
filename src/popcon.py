#!/usr/bin/env python

# popcon.py -
# Copyright (C) 2010  Bastian Venthur
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
    {'reportbug-ng': [50, 187, 86, 0], 'reportbug': [5279, 59652, 10118, 16]}

Behind the scences popcon will try to use cached infomation saved in
`DUMPFILE`. If that file is not available, or older than `EXPIRY` seconds
(default is 7 days) it will download fresh data and save that into `DUMPFILE`.
"""

__author__ = 'Bastian Venthur <venthur@debian.org>'


import time
import urllib2
import gzip
import StringIO
import cPickle as pickle
import os

# week in seconds
EXPIRY = 86400 * 7
DUMPFILE = os.path.expanduser('~/popcon.cache')
RESULTS_URL = "http://popcon.debian.org/all-popcon-results.txt.gz"

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
        ans[elems[1]] = [int(i) for i in elems[2:]]
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
    list of integers: [vote, old, recent, no-files]

        vote: number of people who use this package regulary
        old: is the number of people who installed, but don't use this package 
             regularly
        recent: is the number of people who upgraded this package recently
        no-files: is the number of people whose entry didn't contain enough 
                  information (atime and ctime were 0)
    """
    try:
        handle = open(DUMPFILE, 'r')
        (timestamp, data) = pickle.load(handle)
        handle.close()
        if (timestamp + EXPIRY) < time.time():
            raise
    except:
        data = _fetch()
        data = _parse(data)
        handle = open(DUMPFILE, 'w')
        timestamp = time.time()
        pickle.dump((timestamp, data), handle)
        handle.close()
    ans = dict()
    for pkg in packages:
        if data.has_key(pkg):
            ans[pkg] = data[pkg]
    return ans

