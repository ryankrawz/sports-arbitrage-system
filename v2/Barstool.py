from Sportsbook import Sportsbook


class Barstool(Sportsbook):
    login_button = '//div[@aria-label="open login form"]'
    username_field = '//input[@aria-label="USERNAME"]'
    password_field = '//input[@aria-label="Password"]'
    submit_login = '//button[@type="submit"]'
    logged_in = '//div[@aria-label="account"]'

    def __init__(self, url: str, username: str, password: str):
        super().__init__(url, username, password)

    def get_current_balance(self) -> float:
        pass

    def get_moneyline_odds(self, sport: str) -> dict:
        pass

    def place_moneyline_bet(self, favored: str, opponent: str, odds: int, amount: float) -> bool:
        pass
