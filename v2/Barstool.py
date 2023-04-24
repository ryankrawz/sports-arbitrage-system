from Sportsbook import Sportsbook


class Barstool(Sportsbook):
    def __init__(self, url: str, username: str, password: str, browser: str):
        super().__init__(url, username, password, browser)

    def login(self) -> bool:
        self.driver.get(self.url)
        # Navigate to login page
        self.click_button('span.logged-out')
        # Enter credentials
        self.provide_input_to_element('input[aria-label="USERNAME"]', self.username)
        self.provide_input_to_element('input[aria-label="Password"]', self.password)
        # Click "Log In" button
        self.click_button('button[type="submit"]')

    def get_current_balance(self) -> float:
        pass

    def get_moneyline_odds(self, sport: str) -> dict:
        pass

    def place_moneyline_bet(self, favored: str, opponent: str, odds: int, amount: float) -> bool:
        pass
