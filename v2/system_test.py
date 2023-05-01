import unittest

from main import get_config, get_enabled_books


class SystemTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        config_data = get_config()
        cls._test_sport = config_data['sports'][0]
        cls._enabled_books = get_enabled_books(config_data)

    @classmethod
    def tearDownClass(cls):
        for book in cls._enabled_books:
            book.quit_session()

    def test_login_checkbalance_placebet(self):
        for book in self._enabled_books:
            # Login
            self.assertTrue(book.login(), msg=f'Failed to log into {book.name}')
            # Check account balance
            self.assertGreater(book.get_current_balance(), 0, msg=f'Received an empty account balance from {book.name}')
            # Get moneyline odds
            odds = book.get_moneyline_odds(self._test_sport)
            self.assertGreater(len(odds), 0, msg=f'{book.name} had no {self._test_sport} events')
            self.assertEqual(len(odds) % 2, 0, msg=f'{book.name}\'s events indicated an odd number of teams: {list(odds.keys())}')
            event = odds[list(odds.keys())[0]]
            self.assertIsNotNone(event['odds'], msg=f'{book.name}\'s first event is missing an "odds" key: {event}')
            self.assertIsNotNone(event['opponent'], msg=f'{book.name}\'s first event is missing an "opponent" key: {event}')

if __name__ == '__main__':
    unittest.main()
