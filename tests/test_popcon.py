import sqlite3

import popcon
from popcon import popcon as internal

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

def test_create_schema():
    con = sqlite3.connect(
                ":memory:",
                detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES
            )
    con.row_factory = sqlite3.Row

    internal.create_schema(con)
    cur = con.cursor()
    row = cur.execute("""select version from version;""").fetchone()
    version = row['version']

    assert version == 3
