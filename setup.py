#!/usr/bin/env python

from distutils.core import setup

setup(name='python-popcon',
        version='1.0',
        description="Python inteface to Debian's popcon database",
        author='Bastian Venthur',
        author_email='venthur@debian.org',
        url='http://github.com/venthur/python-popcon',
        py_modules=['popcon'],
        package_dir={"": "src"},
        )

