import argparse

from popcon import packages, packages_raw


def main(args=None):
    """Main entrypoint for the CLI.

    Parameters
    ----------
    args list[str]
        optional parameters, used for testing

    """
    args = parse_args(args)
    pkg = args.package
    # respective withs for package and numbers
    pwidth = 20
    nwidth = 10
    if not args.verbose:
        results = packages(pkg)
        if not results:
            return
        # calculate pwidth based on maximum length of package name, but at
        # least 7 characters to accommodate for the "PACKAGE" string in the
        # header
        pwidth = max(7, max(len(i) for i in results.keys()))
        print(f'{"PACKAGE":>{pwidth}} {"SUM":<{nwidth}}')
        for package, number in results.items():
            print(f'{package:>{pwidth}} {number:<{nwidth}}')
    else:
        results = packages_raw(pkg)
        if not results:
            return
        # calculate pwidth based on maximum length of package name, but at
        # least 7 characters to accommodate for the "PACKAGE" string in the
        # header
        pwidth = max(7, max(len(i) for i in results.keys()))
        print(
            f'{"PACKAGE":>{pwidth}} {"SUM":<{nwidth}} '
            f'{"VOTE":<{nwidth}} {"OLD":<{nwidth}} '
            f'{"RECENT":<{nwidth}} {"NO FILES":<{nwidth}}'
        )
        for package, values in results.items():
            vote = values.vote
            old = values.old
            recent = values.recent
            no_files = values.no_files
            sum_ = sum([vote, old, recent, no_files])
            print(
                f'{package:>{pwidth}} {sum_:<{nwidth}} '
                f'{vote:<{nwidth}} {old:<{nwidth}} '
                f'{recent:<{nwidth}} {no_files:<{nwidth}}'
            )


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

    parser.add_argument(
        '-v', '--verbose',
        help="more verbose package output",
        action="store_true",
    )

    return parser.parse_args(args)


if __name__ == '__main__':
    main()
