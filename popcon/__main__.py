import sys

from popcon import packages


def main():
    if len(sys.argv) == 1:
        raise RuntimeError('No package name given')
    pkg = sys.argv[1]
    print(pkg)
    print(packages([pkg]))


if __name__ == '__main__':
    main()
