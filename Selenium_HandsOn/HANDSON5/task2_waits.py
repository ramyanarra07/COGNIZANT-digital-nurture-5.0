"""
HANDS-ON 5 - Task 2: WebDriverWait and Expected Conditions
Target: https://www.lambdatest.com/selenium-playground/bootstrap-alert-messages-demo
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    ElementClickInterceptedException,
)
from webdriver_manager.chrome import ChromeDriverManager
import time

URL = "https://www.lambdatest.com/selenium-playground/bootstrap-alert-messages-demo"


def safe_click_success_button(driver):
    """Wait until clickable, scroll into view, click - with a JS-click fallback
    in case something (banner/overlay) intercepts the normal click."""
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Success')]"))
    )
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", button)
    time.sleep(0.3)
    try:
        button.click()
    except ElementClickInterceptedException:
        driver.execute_script("arguments[0].click();", button)
    return button


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()

try:
    # ---------- Step 36: Explicit wait with WebDriverWait + EC ----------
    print("=== Step 36: WebDriverWait + EC ===")
    try:
        driver.get(URL)
        time.sleep(1)

        safe_click_success_button(driver)

        success_alert = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-success"))
        )
        print("Step 36 PASSED - alert became visible")
        print("ACTUAL alert text ->", repr(success_alert.text))
    except (NoSuchElementException, TimeoutException) as e:
        print("Step 36 FAILED -", type(e).__name__, "-", str(e)[:200])

    # ---------- Step 37: time.sleep(3) vs explicit wait - timed comparison ----------
    print("\n=== Step 37: time.sleep(3) vs explicit wait (timed) ===")

    # --- Version A: time.sleep(3) ---
    try:
        driver.get(URL)
        time.sleep(1)
        start_sleep = time.time()
        safe_click_success_button(driver)
        time.sleep(3)
        alert_sleep = driver.find_element(By.CSS_SELECTOR, ".alert-success")
        end_sleep = time.time()
        print(f"time.sleep(3) version took {end_sleep - start_sleep:.2f} seconds, text = {alert_sleep.text!r}")
    except Exception as e:
        print("time.sleep(3) version FAILED -", type(e).__name__, "-", str(e)[:200])

    # --- Version B: explicit wait ---
    try:
        driver.get(URL)
        time.sleep(1)
        start_wait = time.time()
        safe_click_success_button(driver)
        alert_wait = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-success"))
        )
        end_wait = time.time()
        print(f"Explicit wait version took {end_wait - start_wait:.2f} seconds, text = {alert_wait.text!r}")
    except Exception as e:
        print("Explicit wait version FAILED -", type(e).__name__, "-", str(e)[:200])

    print("""
    Comment: time.sleep(3) always blocks for the full 3 seconds regardless
    of how fast the alert actually appears - wasting time on fast machines.
    On slow machines/networks, 3 seconds might not even be enough, causing
    a flaky failure. WebDriverWait polls every 500ms (default) and returns
    the instant the condition is true, so it's faster on fast machines and
    more reliable on slow ones.
    """)

    # ---------- Step 38: element_to_be_clickable ----------
    print("=== Step 38: element_to_be_clickable ===")
    try:
        driver.get(URL)
        time.sleep(1)
        safe_click_success_button(driver)
        print("Step 38 PASSED - button was clickable, clicked successfully")
    except Exception as e:
        print("Step 38 FAILED -", type(e).__name__, "-", str(e)[:200])

    print("""
    visibility_of_element_located vs element_to_be_clickable:
    - visibility_of_element_located: element exists in the DOM AND is visible
      (has height/width, not display:none). It does NOT guarantee the element
      can be interacted with.
    - element_to_be_clickable: element is visible AND enabled AND not obscured
      by another element on top of it. Use this before any .click() call.
    """)

    # ---------- Step 39: FluentWait equivalent in Python ----------
    print("=== Step 39: FluentWait (poll_frequency + ignored_exceptions) ===")
    try:
        driver.get("https://www.lambdatest.com/selenium-playground/dynamic-data-loading-demo")
        time.sleep(1)

        fluent_wait = WebDriverWait(
            driver,
            timeout=10,
            poll_frequency=0.5,
            ignored_exceptions=[NoSuchElementException]
        )
        table_row = fluent_wait.until(
            lambda d: d.find_element(By.CSS_SELECTOR, "table tbody tr")
        )
        print("Step 39 PASSED - dynamically loaded table row found:", table_row.text)
    except TimeoutException:
        print("Step 39 FAILED - table row not found within 10s. Open this page in DevTools,")
        print("confirm the real table/row selector, and update 'table tbody tr' above.")

    print("\n=== All tasks attempted. Review PASSED/FAILED lines above. ===")

finally:
    time.sleep(2)
    driver.quit()