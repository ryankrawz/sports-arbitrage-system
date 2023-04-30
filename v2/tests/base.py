import unittest

from v2.main import get_config, get_enabled_books


class TestBase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        config_data = get_config()
        cls._test_sport = config_data['sports'][0]
        cls._enabled_books = get_enabled_books(config_data)

    @classmethod
    def tearDownClass(cls):
        for book in cls._enabled_books:
            book.quit_session()
