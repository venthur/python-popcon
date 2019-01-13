import sys

from popcon import package


def main():
    if len(sys.argv) == 1:
        raise RuntimeError('No package name given')
    pkg = sys.argv[1]
    print(pkg)
    print(package(pkg))


if __name__ == '__main__':
    main()
