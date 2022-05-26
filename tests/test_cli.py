import popcon.__main__ as cli


def test_main_single_package():
    cli.main('python-debianbts')


def test_main_multi_packages():
    cli.main('python-debianbts python3')
