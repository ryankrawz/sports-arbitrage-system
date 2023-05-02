from abc import ABC, abstractmethod
from decimal import Decimal
import re

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from books.utils import element_text_matches_re


class Sportsbook(ABC):
    # Number of seconds web driver will wait for element
    POLL_TIMEOUT = 10
    # Anything other than a digit or "." character
    NON_DECIMAL_EXP = re.compile(r'[^\d.]')
    # One or more whitespace characters
    WHITESPACE_EXP = re.compile(r'\s+')

    ##########
    # XPATHS #
    ##########

    # Button to open login screen and enter credentials
    login_button: str = None
    # Input field for entering username
    username_field: str = None
    # Input field for entering password
    password_field: str = None
    # Button to submit credentials
    submit_login: str = None
    # Element whose presence indicates successful login
    logged_in: str = None

    # Contains the account balance
    account_balance: str = None

    # Button for specific sport, with {sport} being the replacement field
    sport_button: str = None
    # Indicator that correct sport has successfully been clicked
    sport_selected: str = None
    # Container for odds of single event
    event_container: str = None
    # Names of the event participants
    event_participant_1: str = None
    event_participant_2: str = None
    # Moneyline odds on the event's participants
    event_moneyline_odds_1: str = None
    event_moneyline_odds_2: str = None

    def __init__(self, url: str, username: str, password: str):
        self.name = self.__class__.__name__
        self.url = url
        self.username = username
        self.password = password
        # Requires Chrome web driver to run headless
        options = Options()
        # Maximize browser window to reduce chance of element being missed
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--headless')
        # Blink is Chromium's rendering engine and can be picked up by bot detection
        options.add_argument('--disable-blink-features=AutomationControlled')
        self.driver = webdriver.Chrome(options=options)
        # Rotating user agent to Chrome/83.0.4103.53 to also help avoid detection
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'
        })

    def __log_error_message(self, origin: str, e: Exception):
        errorStack = repr(e)
        errorMessage = str(e)
        print(f'\n[ERROR] {self.name} {origin}\n{errorStack}\n{errorMessage}')

    def __log_warning_message(self, origin: str, warning: str):
        print(f'\n[WARNING] {self.name} {origin}\n{warning}')

    def __generate_event_odds_obj(self, opponent_name: str, odds: WebElement) -> dict:
        return {
            'odds': self.additional_odds_processing(odds.text),
            'opponent': opponent_name,
        }
    
    # If no property has a sport extension (e.g. "__hockey"), then there are no
    # custom XPaths and the default one can be returned.
    def __get_custom_xpath_attr(self, attr_root: str, num: int, sport: str) -> str:
        return getattr(self, f'{attr_root}_{num}__{sport}', getattr(self, f'{attr_root}_{num}'))
    
    # Extract lowercase mascot name (exclude city)
    def __parse_team_name(self, name_str: str) -> str:
        words = self.WHITESPACE_EXP.split(name_str.strip().lower())
        # Special case for Red/White Sox since last word of mascot name is the same
        return words[-2] + words[-1] if words[-1] == 'sox' else words[-1]

    # Returns a boolean indicating whether or not login was successful
    def login(self) -> bool:
        self.driver.get(self.url)
        # Navigate to login page
        self.click_button(self.login_button)
        # Enter credentials
        self.provide_input_to_element(self.username_field, self.username)
        self.provide_input_to_element(self.password_field, self.password)
        # Click "Log In" button
        self.click_button(self.submit_login)
        return self.element_exists(self.logged_in)

    # Returns current account balance
    def get_current_balance(self) -> Decimal:
        try:
            # Wait until nonzero balance is populated since some sites may set a default of 0
            element = WebDriverWait(self.driver, self.POLL_TIMEOUT).until(
                element_text_matches_re((By.XPATH, self.account_balance), r'[1-9]')
            )
            return Decimal(self.NON_DECIMAL_EXP.sub('', element.text))
        except Exception as e:
            self.__log_error_message(f'get_current_balance()', e)
            self.quit_session()
            raise e

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
        moneyline_odds = {}
        # Select the sport
        self.click_button(self.sport_button.format(sport=sport))
        # Collect betting events
        sport_clicked = self.element_exists(self.sport_selected.format(sport=sport))
        if sport_clicked:
            events = self.driver.find_elements(By.XPATH, self.event_container)
            invalid_event_counter = 0
            for event in events:
                try:
                    team_1 = event.find_element(By.XPATH, self.__get_custom_xpath_attr('event_participant', 1, sport))
                    team_2 = event.find_element(By.XPATH, self.__get_custom_xpath_attr('event_participant', 2, sport))
                    odds_1 = event.find_element(By.XPATH, self.__get_custom_xpath_attr('event_moneyline_odds', 1, sport))
                    odds_2 = event.find_element(By.XPATH, self.__get_custom_xpath_attr('event_moneyline_odds', 2, sport))
                    # Extract lowercase mascot name (exclude city)
                    team_1_name = self.__parse_team_name(team_1.text)
                    team_2_name = self.__parse_team_name(team_2.text)
                    moneyline_odds[team_1_name] = self.__generate_event_odds_obj(team_2_name, odds_1)
                    moneyline_odds[team_2_name] = self.__generate_event_odds_obj(team_1_name, odds_2)
                except:
                    invalid_event_counter += 1
            if invalid_event_counter > 0:
                totalEvents = len(events)
                self.__log_warning_message(
                    f'get_moneyline_odds({sport})',
                    f'{invalid_event_counter} event elements of {totalEvents} found in XPath were missing name and odds data for both teams:\n{self.event_container}'
                )
        else:
            self.__log_error_message(f'get_moneyline_odds({sport})', Exception(f'Could not retrieve event list for {sport}'))
            self.quit_session()
        return moneyline_odds

    # Returns a boolean indicating whether or not bet was successfully placed
    # If false is returned, the likely cause is odds movement
    # NOTE: function assumes that the bet option is available at driver's current URL,
    #       which typically means that get_moneyline_odds() has been called
    @abstractmethod
    def place_moneyline_bet(self, favored: str, opponent: str, odds: int, amount: float) -> bool:
        pass

    # Odds values from some books will need more handling
    def additional_odds_processing(self, odds_value: str) -> int:
        # Automatically handles strings with +/- signs
        return int(odds_value)

    def quit_session(self):
        self.driver.quit()

    def element_exists(self, xpath: str) -> bool:
        try:
            WebDriverWait(self.driver, self.POLL_TIMEOUT).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            return True
        except Exception as e:
            self.__log_error_message(f'element_exists({xpath})', e)
            return False

    def wait_to_be_clickable(self, xpath: str) -> WebElement:
        try:
            return WebDriverWait(self.driver, self.POLL_TIMEOUT).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
        except Exception as e:
            self.__log_error_message(f'wait_to_be_clickable({xpath})', e)
            self.quit_session()
            raise e
    
    def click_button(self, xpath: str):
        element = self.wait_to_be_clickable(xpath)
        ActionChains(self.driver).click(element).perform()

    def provide_input_to_element(self, xpath: str, input: str):
        element = self.wait_to_be_clickable(xpath)
        action = ActionChains(self.driver)
        # Retry sending input since send_keys will intermittently fail
        num_attempts = 0
        while element.get_attribute('value') != input:
            # Fail after 10 attempts
            if num_attempts == 10:
                self.__log_error_message(f'provide_input_to_element({xpath})', Exception('Could not provide input to element after 10 attempts'))
                self.quit_session()
                break
            action.click(on_element=element)
            action.send_keys(input)
            action.perform()
            action.reset_actions()
            num_attempts += 1
