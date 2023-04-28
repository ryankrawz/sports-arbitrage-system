import unittest

from v2.tests.base import TestBase


class TestLogin(TestBase):
    def test_login(self):
        for book in self._enabled_books:
            book_name = book.__class__.__name__
            self.assertTrue(book.login(), msg=f'Failed to log into {book_name}')

if __name__ == '__main__':
    unittest.main()
