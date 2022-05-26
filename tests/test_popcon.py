import popcon


def test_version():
    assert hasattr(popcon, '__version__')


def test_packages():
    res = popcon.packages(['reportbug', 'python-debianbts'])
    assert len(res) == 2


def test_packages_raw():
    res = popcon.packages_raw(['reportbug', 'python-debianbts'])
    assert len(res) == 2


def test_source_packages():
    res = popcon.source_packages(['reportbug', 'python-debianbts'])
    assert len(res) == 2


def test_source_packages_raw():
    res = popcon.source_packages_raw(['reportbug', 'python-debianbts'])
    assert len(res) == 2



