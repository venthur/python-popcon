import unittest

import popcon


class TestPopcon(unittest.TestCase):

    def test_version(self):
        try:
            popcon.__version__
        except NameError:
            self.fail()

    def test_package(self):
        popcon.package('reportbug')

    def test_package_raw(self):
        popcon.package_raw('reportbug')

    def test_source_package(self):
        popcon.source_package('reportbug')

    def test_source_package_raw(self):
        popcon.source_package_raw('reportbug')


if __name__ == '__main__':
    unittest.main()
