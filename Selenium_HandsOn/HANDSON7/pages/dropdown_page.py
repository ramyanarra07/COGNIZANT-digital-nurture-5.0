from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage

class DropdownPage(BasePage):
    SELECT_LIST = (By.ID, 'select-demo')
    SELECTED_TEXT = (By.CSS_SELECTOR, '.selected-value')

    def select_day(self, day_name):
        dropdown_element = self.wait_for_element(self.SELECT_LIST)
        select = Select(dropdown_element)
        select.select_by_visible_text(day_name)

    def get_selected_day(self):
        return self.wait_for_element(self.SELECTED_TEXT).text