from v2.Sportsbook import Sportsbook


class DraftKings(Sportsbook):
    login_button = '//a[@data-test-id="Log In-cta-link"]'
    username_field = '//input[@id="login-username-input"]'
    password_field = '//input[@id="login-password-input"]'
    submit_login = '//button[@id="login-submit"]'
    logged_in = '//div[@data-test-id="account-dropdown"]'

    def __init__(self, url: str, username: str, password: str):
        super().__init__(url, username, password)

    def get_moneyline_odds(self, sport: str) -> dict:
        pass

    def place_moneyline_bet(self, favored: str, opponent: str, odds: int, amount: float) -> bool:
        pass
