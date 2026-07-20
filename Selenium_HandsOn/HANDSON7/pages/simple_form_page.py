from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class SimpleFormPage(BasePage):
    # Class-level tuples for locator management
    MESSAGE_INPUT = (By.ID, 'user-message')
    SUBMIT_BUTTON = (By.XPATH, "//button[contains(text(),'Get Checked Value')]")
    DISPLAYED_MESSAGE = (By.ID, 'message')

    def enter_message(self, text):
        input_field = self.wait_for_element(self.MESSAGE_INPUT)
        input_field.clear()
        input_field.send_keys(text)

    def click_submit(self):
        self.wait_for_element_clickable(self.SUBMIT_BUTTON).click()

    def get_displayed_message(self):
        return self.wait_for_element(self.DISPLAYED_MESSAGE).text