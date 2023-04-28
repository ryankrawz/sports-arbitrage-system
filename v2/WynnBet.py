from v2.Sportsbook import Sportsbook


class WynnBet(Sportsbook):
    login_button = '/html/body/app-root/div/app-header/header/div[2]/div/div/a[1]'
    username_field = '//input[@id="username"]'
    password_field = '//input[@id="password"]'
    submit_login = '//button[@type="submit"]'
    logged_in = '//a[@class="account-menu-button"]'

    account_balance = '//span[@class="money--currency"]'

    def __init__(self, url: str, username: str, password: str):
        super().__init__(url, username, password)

    def get_moneyline_odds(self, sport: str) -> dict:
        pass

    def place_moneyline_bet(self, favored: str, opponent: str, odds: int, amount: float) -> bool:
        pass
