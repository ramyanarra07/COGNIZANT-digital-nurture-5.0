"""
HANDS-ON 6 - conftest.py
Shared fixtures + screenshot-on-failure hook for pytest_playground.py
"""

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="session")
def base_url():
    """Step 48: session-scoped constant reused by every test instead of
    hardcoding the URL in each test."""
    return "https://www.lambdatest.com/selenium-playground/"


@pytest.fixture(scope="function")
def driver():
    """Step 41: fresh Chrome instance per test - setup before yield,
    teardown after yield (equivalent to setUp/tearDown in unittest)."""
    drv = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    drv.maximize_window()
    yield drv
    drv.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Step 46: capture a screenshot automatically whenever a test fails."""
    outcome = yield
    report = outcome.get_result()
    setattr(item, "rep_" + report.when, report)

    if report.when == "call" and report.failed:
        test_driver = item.funcargs.get("driver")
        if test_driver is not None:
            test_name = item.name.replace("[", "_").replace("]", "_").replace("/", "_")
            screenshot_path = f"{test_name}_failure.png"
            try:
                test_driver.save_screenshot(screenshot_path)
                print(f"\nScreenshot saved: {screenshot_path}")
            except Exception as e:
                print(f"\nCould not save screenshot: {e}")