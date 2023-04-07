from selenium import webdriver


class Sportsbook:
    def __init__(self, url: str, username: str, password: str, browser: str):
        self.url = url
        self.username = username
        self.password = password
        # Dynamically instantiate web driver based on the type of browser provided
        driver = getattr(webdriver, browser)
        self.driver = driver()

    # Returns a boolean indicating whether or not login was successful
    def login(self) -> bool:
        raise NotImplementedError('Subclass must implement login()')

    # Returns current account balance
    def get_current_balance(self) -> float:
        raise NotImplementedError('Subclass must implement get_current_balance()')

    # Parameter is one of the array items found in the "sports" field of config.json
    # Returns an object like the following (keys are the team mascots in lowercase):
    # {
    #     'marlins': {
    #         'odds': -150,
    #         'opponent': 'braves'
    #     },
    #     'braves': {
    #         'odds': 100,
    #         'opponent': 'marlins'
    #     }
    # }
    def get_moneyline_odds(self, sport: str) -> dict:
        raise NotImplementedError('Subclass must implement get_moneyline_odds()')

    # Returns a boolean indicating whether or not bet was successfully placed
    # If false is returned, the likely cause is odds movement
    # NOTE: function assumes that the bet option is available at driver's current URL,
    #       which typically means that get_moneyline_odds() has been called
    def place_moneyline_bet(self, favored: str, opponent: str, odds: int, amount: float) -> bool:
        raise NotImplementedError('Subclass must implement place_moneyline_bet()')
