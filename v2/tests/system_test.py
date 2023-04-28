import unittest

from v2.tests.base import TestBase


class SystemTest(TestBase):
    def test_login_checkbalance_placebet(self):
        for book in self._enabled_books:
            book_name = book.__class__.__name__
            self.assertTrue(book.login(), msg=f'Failed to log into {book_name}')
            self.assertGreater(book.get_current_balance(), 0, msg=f'Received an empty account balance from {book_name}')

if __name__ == '__main__':
    unittest.main()
