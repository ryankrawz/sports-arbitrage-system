from re import search

from selenium.webdriver import Chrome


# Custom wait condition for checking if text inside element matches regular expression
class element_text_matches_re(object):
    def __init__(self, locator, exp: str):
        self.locator = locator
        self.exp = exp

    def __call__(self, driver: Chrome):
        element = driver.find_element(*self.locator)
        return element if search(self.exp, element.text) is not None else False
