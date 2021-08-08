from setuptools import setup

meta = {}
exec(open('./popcon/version.py').read(), meta)
meta['long_description'] = open('./README.md').read()


setup(
    name='python-popcon',
    version=meta['__version__'],
    description="Python interface to Debian's popularity contest database",
    long_description=meta['long_description'],
    long_description_content_type='text/markdown',
    keywords='debian, popcon, popularity contest',
    author='Bastian Venthur',
    author_email='venthur@debian.org',
    url='http://github.com/venthur/python-popcon',
    license='GPL2',
    packages=['popcon'],
    python_requires='>=3.6, <4',
    entry_points={
        'console_scripts': [
            'popcon = popcon.__main__:main'
        ]
    },
)
