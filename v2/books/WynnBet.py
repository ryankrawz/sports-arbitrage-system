from books.Sportsbook import Sportsbook


class WynnBet(Sportsbook):
    login_button = '/html/body/app-root/div/app-header/header/div[2]/div/div/a[1]'
    username_field = '//input[@id="username"]'
    password_field = '//input[@id="password"]'
    submit_login = '//button[@type="submit"]'
    logged_in = '//a[@class="account-menu-button"]'

    account_balance = '//span[@class="money--currency"]'

    sport_button = '//button[@data-test="{sport}"]'
    # Currently translates B, H, F to lowercase for Basketball, Baseball, Hockey, Football
    sport_selected = '//div[@class="tabs-list"]/a[contains(translate(@href, "BHF", "bhf"), "/us/sports/{sport}")]'
    # Ignore event table header, which is sibling div of element containers
    event_container = '//*[@id="main-layout"]/div[2]/div/div/div[1]/div[2]/div[2]/div[2]/div[2]/div[position()>1]'
    event_participant_1 = './div[1]/div/div[1]/div/div[1]/div[1]/div/div/div[1]/div[2]'
    event_participant_2 = './div[1]/div/div[1]/div/div[1]/div[1]/div/div/div[2]/div[2]'
    event_moneyline_odds_1 = './div[1]/div/div[2]/div[2]/div/div[1]/button/span/span'
    event_moneyline_odds_2 = './div[1]/div/div[2]/div[2]/div/div[2]/button/span/span'
    
    event_participant_1__hockey = './div[1]/div/div[1]/div/div[1]/div[1]/div/div/div[1]/div'
    event_participant_2__hockey = './div[1]/div/div[1]/div/div[1]/div[1]/div/div/div[2]/div'
    event_moneyline_odds_1__hockey = './div[1]/div/div[2]/div[2]/div/div[1]/button/span/span'
    event_moneyline_odds_2__hockey = './div[1]/div/div[2]/div[2]/div/div[2]/button/span/span'

    def __init__(self, url: str, username: str, password: str):
        super().__init__(url, username, password)

    def place_moneyline_bet(self, favored: str, opponent: str, odds: int, amount: float) -> bool:
        return True
