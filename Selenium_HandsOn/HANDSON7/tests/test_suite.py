import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.simple_form_page import SimpleFormPage
from pages.checkbox_page import CheckboxPage
from pages.dropdown_page import DropdownPage
from pages.input_form_page import InputFormPage

BASE_URL = "https://www.lambdatest.com/selenium-playground"

@pytest.fixture
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--window-size=1280,800')
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_simple_form_submission(driver):
    # Step 55 Implementation
    simple_form = SimpleFormPage(driver)
    simple_form.navigate_to(f"{BASE_URL}/simple-form-demo")
    
    simple_form.enter_message("Hello Selenium")
    simple_form.click_submit()
    
    assert simple_form.get_displayed_message() == "Hello Selenium"

def test_checkbox_demo(driver):
    # Step 56 Implementation - Checkbox
    checkbox_page = CheckboxPage(driver)
    checkbox_page.navigate_to(f"{BASE_URL}/checkbox-demo")
    
    checkbox_page.check_option(1)
    assert checkbox_page.is_option_checked(1) == True
    
    checkbox_page.uncheck_option(1)
    assert checkbox_page.is_option_checked(1) == False

def test_dropdown_selection(driver):
    # Step 56 Implementation - Dropdown
    dropdown_page = DropdownPage(driver)
    dropdown_page.navigate_to(f"{BASE_URL}/select-dropdown-demo")
    
    dropdown_page.select_day("Friday")
    assert "Friday" in dropdown_page.get_selected_day()

def test_input_form_submit(driver):
    # Step 57 Implementation
    input_form = InputFormPage(driver)
    input_form.navigate_to(f"{BASE_URL}/input-form-demo")
    
    input_form.fill_form("John Doe", "john@example.com", "1234567890", "123 Test St")
    input_form.submit_form()
    
    assert "successfully" in input_form.get_success_message().lower()

# ==============================================================================
# STEP 59: TECHNICAL ANALYSIS COMMENTARY
#
# Problem in Flat (Non-POM) Scripts:
# If the submit button's ID changed from 'submit' to 'btn-submit', a flat script
# architecture forces you to hunt down and manually change every single instance
# of `driver.find_element(By.ID, 'submit')` across dozens of separate test files.
# This makes maintenance expensive and error-prone.
#
# How POM Solves This:
# POM maps locators as centralized class-level properties inside specific page classes. 
# Because the test scripts only call abstractions like `page.click_submit()`, you only 
# have to update the locator string *once* inside `simple_form_page.py`. Every test file 
# automatically inherits the fix without changing a single line of assertion logic.
# ==============================================================================