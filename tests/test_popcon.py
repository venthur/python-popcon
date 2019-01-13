import popcon


def test_version():
    assert hasattr(popcon, '__version__')


def test_package():
    popcon.package('reportbug')


def test_package_raw():
    popcon.package_raw('reportbug')


def test_source_package():
    popcon.source_package('reportbug')


def test_source_package_raw():
    popcon.source_package_raw('reportbug')
