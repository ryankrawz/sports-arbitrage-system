import unittest

from v2.tests.base import TestBase


class SystemTest(TestBase):
    def test_login_checkbalance_placebet(self):
        for book in self._enabled_books:
            book_name = book.__class__.__name__
            # Login
            self.assertTrue(book.login(), msg=f'Failed to log into {book_name}')
            # Check account balance
            self.assertGreater(book.get_current_balance(), 0, msg=f'Received an empty account balance from {book_name}')
            # Get moneyline odds
            odds = book.get_moneyline_odds(self._test_sport)
            self.assertGreater(len(odds), 0, msg=f'{book_name} had no {self._test_sport} events')
            self.assertEqual(len(odds) % 2, 0, msg=f'{book_name}\'s events indicated an odd number of teams: {list(odds.keys())}')
            event = odds[list(odds.keys())[0]]
            self.assertIsNotNone(event['odds'], msg=f'{book_name}\'s first event is missing an "odds" key: {event}')
            self.assertIsNotNone(event['opponent'], msg=f'{book_name}\'s first event is missing an "opponent" key: {event}')

if __name__ == '__main__':
    unittest.main()
