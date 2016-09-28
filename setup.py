#!/usr/bin/env python

import sys
from distutils.core import setup

sys.path.insert(0, 'src')

import popcon


setup(name='python-popcon',
      version=popcon.__version__,
      description="Python inteface to Debian's popcon database",
      author='Bastian Venthur',
      author_email='venthur@debian.org',
      url='http://github.com/venthur/python-popcon',
      py_modules=['popcon'],
      package_dir={"": "src"},
)
