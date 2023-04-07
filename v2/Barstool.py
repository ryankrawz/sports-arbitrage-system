import Sportsbook


class Barstool(Sportsbook):
    def __init__(self, url: str, username: str, password: str, browser: str):
        super().__init__(url, username, password, browser)

    def login(self) -> bool:
        pass

    def get_current_balance(self) -> float:
        pass

    def get_moneyline_odds(self, sport: str) -> dict:
        pass

    def place_moneyline_bet(self, favored: str, opponent: str, odds: int, amount: float) -> bool:
        pass
