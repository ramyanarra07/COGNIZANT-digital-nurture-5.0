"""
HANDS-ON 5 - Task 1: Locator Strategies - From Simple to Robust
Target: https://www.lambdatest.com/selenium-playground/
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()

try:
    # ---------- Step 32-33: Simple Form Demo ----------
    driver.get("https://www.lambdatest.com/selenium-playground/simple-form-demo")
    time.sleep(1)

    # 1. By.ID (confirmed working)
    el_id = driver.find_element(By.ID, "user-message")
    print("By.ID -> PASSED")
    print("FULL outerHTML for reference:\n", el_id.get_attribute("outerHTML"), "\n")
    el_id.send_keys("Locating by ID")

    # 2. By.NAME
    try:
        el_name = driver.find_element(By.NAME, "user-message")
        print("By.NAME -> PASSED, id =", el_name.get_attribute("id"))
    except NoSuchElementException:
        print("By.NAME -> FAILED (no name='user-message' attribute on this element - check the outerHTML above for the real name, or note in your report that this field has no name attribute)")

    # 3. By.CLASS_NAME (must be a SINGLE class, not multiple)
    try:
        el_class = driver.find_element(By.CLASS_NAME, "w-full")
        print("By.CLASS_NAME -> PASSED, id =", el_class.get_attribute("id"))
    except NoSuchElementException:
        print("By.CLASS_NAME -> FAILED (try another single class from the outerHTML above, e.g. 'border-gray-550')")

    # 4. By.TAG_NAME (locate the input tag)
    try:
        inputs = driver.find_elements(By.TAG_NAME, "input")
        print(f"By.TAG_NAME -> PASSED, found {len(inputs)} <input> tag(s) on this page")
    except NoSuchElementException:
        print("By.TAG_NAME -> FAILED")

    # 5. By.XPATH - absolute path
    try:
        el_xpath_abs = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div[2]/form/div/input")
        print("By.XPATH (absolute) -> PASSED, id =", el_xpath_abs.get_attribute("id"))
    except NoSuchElementException:
        print("By.XPATH (absolute) -> FAILED (right-click the field in DevTools > Copy > Copy full XPath, replace the path above)")

    # 6. By.XPATH - relative path using attributes
    try:
        el_xpath_rel = driver.find_element(By.XPATH, "//input[@id='user-message']")
        print("By.XPATH (relative) -> PASSED, id =", el_xpath_rel.get_attribute("id"))
    except NoSuchElementException:
        print("By.XPATH (relative) -> FAILED")

    # ---------- Step 33: Three CSS selectors for the SAME element ----------
    try:
        css_by_id = driver.find_element(By.CSS_SELECTOR, "#user-message")
        print("CSS by ID -> PASSED, id =", css_by_id.get_attribute("id"))
    except NoSuchElementException:
        print("CSS by ID -> FAILED")

    try:
        css_by_attr = driver.find_element(By.CSS_SELECTOR, "input[class*='w-full']")
        print("CSS by attribute -> PASSED, id =", css_by_attr.get_attribute("id"))
    except NoSuchElementException:
        print("CSS by attribute -> FAILED")

    try:
        css_by_parent_child = driver.find_element(By.CSS_SELECTOR, "form input")
        print("CSS by parent > child -> PASSED, id =", css_by_parent_child.get_attribute("id"))
    except NoSuchElementException:
        print("CSS by parent > child -> FAILED")

    # ---------- Step 34: Checkbox Demo page ----------
    driver.get("https://www.lambdatest.com/selenium-playground/checkbox-demo")
    time.sleep(1)

    try:
        first_option_label = driver.find_element(By.XPATH, "//label[text()='Option 1']")
        print("\nExact text() match -> PASSED:", first_option_label.text)
    except NoSuchElementException:
        print("\nExact text() match -> FAILED")

    try:
        all_option_labels = driver.find_elements(By.XPATH, "//label[contains(text(),'Option')]")
        print(f"contains() match -> PASSED, found {len(all_option_labels)} option labels")
        for label in all_option_labels:
            print("   ", label.text)
    except NoSuchElementException:
        print("contains() match -> FAILED")

    # ---------- Step 35: Ranking (most to least preferred) ----------
    """
    Ranking Locator Strategies - Most to Least Preferred for Maintainable Automation
    (Criteria: uniqueness, brittleness to HTML changes, readability)

    1. ID            - Unique per page, fastest, most readable. Best choice when present.
    2. CSS_SELECTOR  - Fast, flexible, readable, survives most HTML structure changes.
    3. XPATH (relative, attribute-based)
                     - Powerful (supports text() and contains()), but slightly slower
                       than CSS and easier to write incorrectly.
    4. NAME          - Simple when present, but many modern sites (like this redesigned
                       LambdaTest page) don't set a name attribute at all.
    5. CLASS_NAME    - Often shared by multiple elements, and only accepts ONE class -
                       breaks immediately if the site uses utility CSS frameworks
                       (Tailwind) with multiple classes per element, as seen here.
    6. XPATH (absolute path) / TAG_NAME
                     - Absolute XPath breaks the instant the DOM structure changes.
                       TAG_NAME almost never returns a unique element on its own.
    """

    print("\nDone. Review the PASSED/FAILED lines above and note the failures")
    print("in your hands-on report as evidence of locator brittleness.")

finally:
    time.sleep(2)
    driver.quit()