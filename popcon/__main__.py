import argparse

from popcon import packages


def main(args=None):
    """Main entrypoint for the CLI.

    Parameters
    ----------
    args list[str]
        optional parameters, used for testing

    """
    args = parse_args(args)
    pkg = args.package
    print(pkg)
    print(packages(pkg))


def parse_args(args=None):
    """Parse command line arguments.

    Parameters
    ----------
    args list[str]
        optional parameters, used for testing

    Returns
    -------
    argparse.Namespace

    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        'package',
        nargs="+",
        help="the package name(s)",
    )

    return parser.parse_args(args)


if __name__ == '__main__':
    main()
