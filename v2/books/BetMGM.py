from books.Sportsbook import Sportsbook


class BetMGM(Sportsbook):
    login_button = '//span[@data-testid="signin"]'
    username_field = '//input[@name="username"]'
    password_field = '//input[@name="password"]'
    submit_login = '//button[contains(@class, "login")]'
    logged_in = '//div[@class="account-menu-anchor"]'

    account_balance = '//div[contains(@class, "user-balance")]'

    sport_button = '//a[contains(@href, "/en/sports/{sport}")]'
    event_container = '//ms-tabbed-grid-widget[1]/ms-grid/div/ms-event-group/ms-six-pack-event'
    event_participant_1 = './div/a/ms-event-detail/ms-event-name/ms-inline-tooltip/div/div[1]/div/div'
    event_participant_2 = './div/a/ms-event-detail/ms-event-name/ms-inline-tooltip/div/div[2]/div/div'
    event_moneyline_odds_1 = './div/div/div[1]/ms-option-group[3]/ms-option[1]/ms-event-pick/div/div[2]/ms-font-resizer'
    event_moneyline_odds_2 = './div/div/div[1]/ms-option-group[3]/ms-option[2]/ms-event-pick/div/div[2]/ms-font-resizer'

    def __init__(self, url: str, username: str, password: str):
        super().__init__(url, username, password)

    def additional_odds_processing(self, odds_value: str) -> int:
        # MGM sometimes sends total return on bet, so if odds on bet were +150, value is 2.5
        try:
            return int(odds_value)
        except:
            odds_float = float(odds_value)
            if odds_float < 2:
                return -round((1 / (odds_float - 1)) * 100)
            else:
                return round((odds_float - 1) * 100)

    def place_moneyline_bet(self, favored: str, opponent: str, odds: int, amount: float) -> bool:
        return True
