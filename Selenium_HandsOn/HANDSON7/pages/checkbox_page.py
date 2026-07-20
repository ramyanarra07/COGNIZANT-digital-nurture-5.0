from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CheckboxPage(BasePage):
    def _get_checkbox_locator(self, index):
        # Dynamically builds relative XPaths safely based on index position
        return (By.XPATH, f"(//input[@type='checkbox' and not(@id='box')])[{index}]")

    def check_option(self, index):
        locator = self._get_checkbox_locator(index)
        checkbox = self.wait_for_element_clickable(locator)
        if not checkbox.is_selected():
            checkbox.click()

    def uncheck_option(self, index):
        locator = self._get_checkbox_locator(index)
        checkbox = self.wait_for_element_clickable(locator)
        if checkbox.is_selected():
            checkbox.click()

    def is_option_checked(self, index):
        locator = self._get_checkbox_locator(index)
        return self.wait_for_element(locator).is_selected()