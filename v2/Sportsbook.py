from abc import ABC, abstractmethod

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class Sportsbook(ABC):
    # XPATHS
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

    def __init__(self, url: str, username: str, password: str):
        self.url = url
        self.username = username
        self.password = password
        # Requires Chrome web driver to run headless
        options = Options()
        # Maximize browser window to reduce chance of element being missed
        options.add_argument('start-maximized')
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(chrome_options=options)

    def log_error_message(self, origin: str, e: Exception):
        errorStack = repr(e)
        errorMessage = str(e)
        print(f'\n[ERROR] {origin}\n{errorStack}\n{errorMessage}')

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
    @abstractmethod
    def get_current_balance(self) -> float:
        pass

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
    @abstractmethod
    def get_moneyline_odds(self, sport: str) -> dict:
        pass

    # Returns a boolean indicating whether or not bet was successfully placed
    # If false is returned, the likely cause is odds movement
    # NOTE: function assumes that the bet option is available at driver's current URL,
    #       which typically means that get_moneyline_odds() has been called
    @abstractmethod
    def place_moneyline_bet(self, favored: str, opponent: str, odds: int, amount: float) -> bool:
        pass

    def quit_session(self):
        self.driver.quit()

    def element_exists(self, xpath: str) -> bool:
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            return True
        except Exception as e:
            self.log_error_message(f'element_exists({xpath})', e)
            return False

    def wait_to_be_clickable(self, xpath: str) -> WebElement:
        try:
            # Wait 10 seconds maximum
            return WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
        except Exception as e:
            self.log_error_message(f'wait_to_be_clickable({xpath})', e)
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
                self.log_error_message(f'provide_input_to_element({xpath})', Exception('Could not provide input to element after 10 attempts'))
                self.quit_session()
            action.click(on_element=element)
            action.send_keys(input)
            action.perform()
            action.reset_actions()
            num_attempts += 1
