import sys
from setuptools import setup

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
    install_requires=['xdg'],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, <4',
)
