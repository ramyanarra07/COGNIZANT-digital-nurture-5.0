"""
================================================================================
HANDS-ON 4: Selenium WebDriver Setup, Browser Drivers & Basic Commands
================================================================================

TASK 1: SELENIUM ARCHITECTURE DESCRIPTION (Step 24)

1. WebDriver:
   An open-source API framework that allows code scripts to programmatically 
   control browser actions. It communicates directly with the target browser 
   using the native automation engine provided by that specific browser vendor 
   (e.g., ChromeDriver for Google Chrome) via a secure HTTP protocol.

2. Selenium Grid:
   A server framework architecture designed to solve scalability issues by 
   routing commands to remote web browser instances running across multiple physical 
   machines, operating systems, and versions. This allows test suites to run 
   in parallel, cutting down execution time significantly.

3. Selenium IDE:
   A lightweight browser extension (Chrome/Firefox) utilized for rapid prototyping. 
   It implements a simple Record-and-Playback engine that generates test cases 
   visually without coding skills, allowing them to be exported into programming 
   languages like Python for advanced expansion.
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def run_selenium_handson():
    print("Initializing Chrome WebDriver Setup...")
    
    # --------------------------------------------------------------------------
    # STEP 27: Headless Mode Options Setup
    # --------------------------------------------------------------------------
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Runs browser without opening the UI window
    chrome_options.add_argument('--window-size=1280,800') # Recommended layout initial configuration
    
    # Auto-manages and downloads the matching version of ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        # --------------------------------------------------------------------------
        # STEP 26: Implicit Wait Configuration
        # --------------------------------------------------------------------------
        driver.implicitly_wait(10)
        
        """
        CRITICAL COMMENT: Why Implicit Wait Globally is Considered Bad Practice:
        Implicit waits tell the driver polling loop to block code progression until 
        elements arrive, up to the global max threshold (10 seconds here). 
        
        This introduces 3 core architecture problems:
        1. It hides slow page layouts during system testing, making structural latency 
           invisible until production.
        2. Mixing it with Explicit Waits (`WebDriverWait`) often confuses the native 
           browser driver bindings, causing erratic, unexplained thread timeouts.
        3. If a verification check needs to assert that an element is *not* present 
           on screen, it forces the runtime thread to waste the full 10-second wait 
           before returning, slowing down the entire test run.
        """

        # --------------------------------------------------------------------------
        # STEP 25: Navigation and Environment Verification
        # --------------------------------------------------------------------------
        print("\n--- TASK 1 START ---")
        playground_url = "https://www.lambdatest.com/selenium-playground/"
        driver.get(playground_url)
        
        # Prints the target web page title
        print(f"Target Page Title Loaded: {driver.title}")
        print("--- TASK 1 COMPLETE ---")
        
        # --------------------------------------------------------------------------
        # STEP 28: WebDriver Navigation and Links Checks
        # --------------------------------------------------------------------------
        print("\n--- TASK 2 START ---")
        print("Navigating to Simple Form Demo page...")
        
        # Locate the link using link text mapping and click it
        simple_form_link = driver.find_element(By.LINK_TEXT, "Simple Form Demo")
        simple_form_link.click()
        
        # Assert the current URL contains 'simple-form-demo' string
        current_url = driver.current_url
        print(f"Current URL: {current_url}")
        assert 'simple-form-demo' in current_url, "Assertion Failed: URL mismatch!"
        print("Assertion Passed: URL correctly contains 'simple-form-demo'.")
        
        # Navigate backward to previous platform screen view
        print("Navigating back to main playground layout...")
        driver.back()
        
        # --------------------------------------------------------------------------
        # STEP 29: Window Handles Management and Multi-Tab Execution
        # --------------------------------------------------------------------------
        print("\nOpening a new blank browser tab to Google...")
        driver.execute_script('window.open("https://www.google.com");')
        
        # Catalog existing open handle states
        all_handles = driver.window_handles
        print(f"Total Open Windows Tracked: {len(all_handles)}")
        
        # Switch context focus into the secondary workspace index [1]
        driver.switch_to.window(all_handles[1])
        print(f"Switched Window Title Focus: {driver.title}")
        
        # --------------------------------------------------------------------------
        # STEP 30: Context Switching & Capture Screen Verification
        # --------------------------------------------------------------------------
        print("\nSwitching back to the baseline home tab context [0]...")
        driver.switch_to.window(all_handles[0])
        
        screenshot_file = 'playground_screenshot.png'
        driver.save_screenshot(screenshot_file)
        print(f"Screenshot successfully captured and saved as: {screenshot_file}")
        
        # --------------------------------------------------------------------------
        # STEP 31: Window Size Controls Analysis
        # --------------------------------------------------------------------------
        print(f"\nDefault Headless Workspace Boundary Size: {driver.get_window_size()}")
        
        driver.set_window_size(1280, 800)
        print(f"Updated Target Resolution Configured: {driver.get_window_size()}")
        
        """
        CRITICAL COMMENT: Why Consistent Window Size Matters for Responsive UI:
        In responsive designs, elements shifting positions dynamically based on CSS 
        breakpoints can cause automation scripts to fail. If tests run on varying monitor 
        resolutions across localized developer machines or headless CI/CD pipelines:
        1. Click points can shift or get hidden behind menus.
        2. Elements might fall out of view, throwing 'ElementNotInteractableException'.
        Enforcing a static canvas configuration (e.g., 1280x800) standardizes viewport 
        breakpoints, ensuring cross-environment execution stability.
        """
        print("--- TASK 2 COMPLETE ---")
        
    finally:
        # Gracefully terminates all underlying execution nodes
        print("\nTerminating active browser sessions and cleaning up processes...")
        driver.quit()
        print("Execution finished successfully.")

if __name__ == "__main__":
    run_selenium_handson()