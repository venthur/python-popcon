import unittest

import popcon


class TestPopcon(unittest.TestCase):

    def test_version(self):
        try:
            popcon.__version__
        except NameError:
            self.fail()


if __name__ == '__main__':
    unittest.main()
