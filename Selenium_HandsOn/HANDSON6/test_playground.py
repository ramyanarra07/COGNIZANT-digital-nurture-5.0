"""
HANDS-ON 6 - test_playground.py
pytest test suite for LambdaTest Selenium Playground pages.
Run with: pytest test_playground.py -v
"""

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException


def robust_click(driver, element):
    """Scroll into view, wait a beat for any animation, click - with a
    JS-click fallback if something briefly overlaps the element."""
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
    WebDriverWait(driver, 5).until(lambda d: element.is_displayed())
    try:
        element.click()
    except ElementClickInterceptedException:
        driver.execute_script("arguments[0].click();", element)


def get_message_input(driver):
    return WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "user-message"))
    )


def click_get_checked_value(driver):
    try:
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "showInput"))
        )
    except Exception:
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(),'Get Checked') or contains(text(),'Submit')]")
            )
        )
    robust_click(driver, button)


def get_displayed_message(driver):
    try:
        return WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.ID, "message"))
        )
    except Exception:
        return WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//p[@id='message'] | //*[contains(@class,'message')]")
            )
        )


def get_first_checkbox(driver):
    """Target the 'Click on check box' single-checkbox demo directly by its
    visible label - confirmed present on the live redesigned page."""
    try:
        return WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//label[contains(text(),'Click on check box')]/preceding-sibling::input"
                           " | //label[contains(text(),'Click on check box')]/input")
            )
        )
    except Exception:
        # fallback: first checkbox input anywhere on the page
        return WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "(//input[@type='checkbox'])[1]"))
        )


# ---------- Step 42: single form submission ----------
def test_simple_form_submission(driver, base_url):
    driver.get(base_url + "simple-form-demo")
    get_message_input(driver).send_keys("Hello Selenium")
    click_get_checked_value(driver)
    displayed = get_displayed_message(driver)
    assert displayed.text == "Hello Selenium"


# ---------- Step 43: checkbox select / deselect ----------
def test_checkbox_demo(driver, base_url):
    driver.get(base_url + "checkbox-demo")
    checkbox = get_first_checkbox(driver)

    robust_click(driver, checkbox)
    assert checkbox.is_selected() is True

    robust_click(driver, checkbox)
    assert checkbox.is_selected() is False


# ---------- Step 45: parameterised form submission (3 runs) ----------
@pytest.mark.parametrize("message", ["Hello", "Selenium Automation", "12345"])
def test_simple_form_submission_param(driver, base_url, message):
    driver.get(base_url + "simple-form-demo")
    get_message_input(driver).send_keys(message)
    click_get_checked_value(driver)
    displayed = get_displayed_message(driver)
    assert displayed.text == message


# ---------- Step 49: dropdown selection ----------
def test_dropdown_selection(driver, base_url):
    driver.get(base_url + "select-dropdown-demo")
    dropdown_element = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "select-demo"))
    )
    select = Select(dropdown_element)
    select.select_by_visible_text("Wednesday")
    assert select.first_selected_option.text == "Wednesday"