import popcon


def test_version():
    assert hasattr(popcon, '__version__')


def test_packages():
    res = popcon.package(['reportbug', 'python-debianbts'])
    assert len(res) == 2


def test_packages_raw():
    res = popcon.package_raw(['reportbug', 'python-debianbts'])
    assert len(res) == 2


def test_source_packages():
    res = popcon.source_package(['reportbug', 'python-debianbts'])
    assert len(res) == 2


def test_source_packages_raw():
    res = popcon.source_package_raw(['reportbug', 'python-debianbts'])
    assert len(res) == 2


# reprecated below
def test_package(caplog):
    popcon.package('reportbug')
    assert 'deprecated' in caplog.text


def test_package_raw(caplog):
    popcon.package_raw('reportbug')
    assert 'deprecated' in caplog.text


def test_source_package(caplog):
    popcon.source_package('reportbug')
    assert 'deprecated' in caplog.text


def test_source_package_raw(caplog):
    popcon.source_package_raw('reportbug')
    assert 'deprecated' in caplog.text
