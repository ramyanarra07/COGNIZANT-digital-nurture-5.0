from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage

class InputFormPage(BasePage):
    NAME_FIELD = (By.NAME, 'name')
    EMAIL_FIELD = (By.ID, 'inputEmail4')
    PHONE_FIELD = (By.NAME, 'phone')
    ADDRESS_FIELD = (By.NAME, 'address_line1')
    SUBMIT_BUTTON = (By.XPATH, "//button[contains(text(),'Submit')]")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, '.success-msg')

    def fill_form(self, name, email, phone, address):
        self.wait_for_element(self.NAME_FIELD).send_keys(name)
        self.wait_for_element(self.EMAIL_FIELD).send_keys(email)
        self.wait_for_element(self.PHONE_FIELD).send_keys(phone)
        self.wait_for_element(self.ADDRESS_FIELD).send_keys(address)

    def submit_form(self):
        self.wait_for_element_clickable(self.SUBMIT_BUTTON).click()

    def get_success_message(self):
        return self.wait_for_element(self.SUCCESS_MESSAGE).text