from setuptools import setup

exec(open('./popcon/version.py').read())

setup(
    name='python-popcon',
    version=__version__,
    description="Python interface to Debian's popularity contest database",
    long_description="This packages allows to query Debian's popularity contest database.",
    keywords='debian, popcon, popularity contest',
    author='Bastian Venthur',
    author_email='venthur@debian.org',
    url='http://github.com/venthur/python-popcon',
    license='GPL2',
    packages=['popcon'],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, <4',
    entry_points={
        'console_scripts': [
            'popcon = popcon.__main__:main'
        ]
    },
)
