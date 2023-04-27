import unittest

from v2.main import get_enabled_books, get_config


class TestBase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        config_data = get_config()
        cls._enabled_books = get_enabled_books(config_data)

    @classmethod
    def tearDownClass(cls):
        for book in cls._enabled_books:
            book.quit_session()
