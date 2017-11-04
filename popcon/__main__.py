from __future__ import absolute_import, print_function

import sys

from popcon.popcon import package


def main():
    if len(sys.argv) == 1:
        raise RuntimeError('No package name given')
    pkg = sys.argv[1]
    print(pkg)
    print(package(pkg))

main()
