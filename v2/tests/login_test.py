import unittest

from v2.tests.base import TestBase


class TestLogin(TestBase):
    def test_login(self):
        for book in self._enabled_books:
            self.assertTrue(book.login())

if __name__ == '__main__':
    unittest.main()
