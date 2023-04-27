from v2.Sportsbook import Sportsbook


class BetMGM(Sportsbook):
    login_button = '//span[@data-testid="signin"]'
    username_field = '//input[@name="username"]'
    password_field = '//input[@name="password"]'
    submit_login = '//button[contains(@class, "login")]'
    logged_in = '//div[@class="account-menu-anchor"]'

    def __init__(self, url: str, username: str, password: str, headless: bool = True):
        super().__init__(url, username, password, headless=headless)

    def get_current_balance(self) -> float:
        pass

    def get_moneyline_odds(self, sport: str) -> dict:
        pass

    def place_moneyline_bet(self, favored: str, opponent: str, odds: int, amount: float) -> bool:
        pass
