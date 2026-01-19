import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuration and constants for maintainability
LOGIN_URL = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
VALID_USERNAME = "Admin"
VALID_PASSWORD = "admin123"
USERNAME_INPUT_XPATH = "//input[@name='username']"
PASSWORD_INPUT_XPATH = "//input[@name='password']"
LOGIN_BUTTON_XPATH = "//button[@type='submit']"
DASHBOARD_HEADER_XPATH = "//h6[text()='Dashboard']"
PAGE_LOAD_TIMEOUT = 30
ELEMENT_TIMEOUT = 15

def get_chrome_driver():
    """Initializes and returns a headless Chrome WebDriver instance with robust options for CI/CD."""
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
    return driver

def wait_for_element(driver, by, value, timeout=ELEMENT_TIMEOUT):
    """Waits for a web element to be present and visible."""
    try:
        return WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((by, value))
        )
    except Exception as e:
        raise AssertionError(f"Element not found: {value}. Exception: {str(e)}")

@pytest.mark.login
def test_automate_login_functionality_for_orangehrm():
    """
    Test Case: Automate login functionality for OrangeHRM (KAN-15)
    Steps:
      1. Navigate to the login page
      2. Enter valid username
      3. Enter valid password
      4. Click on Login button
    Expected Result:
      User should be redirected to the dashboard page.
    """
    driver = None
    try:
        driver = get_chrome_driver()
        # Step 1: Navigate to the login page
        driver.get(LOGIN_URL)
        assert "orangehrmlive" in driver.current_url.lower(), "Not on OrangeHRM login page."

        # Step 2: Enter valid username
        username_input = wait_for_element(driver, By.XPATH, USERNAME_INPUT_XPATH)
        username_input.clear()
        username_input.send_keys(VALID_USERNAME)

        # Step 3: Enter valid password
        password_input = wait_for_element(driver, By.XPATH, PASSWORD_INPUT_XPATH)
        password_input.clear()
        password_input.send_keys(VALID_PASSWORD)

        # Step 4: Click on Login button
        login_button = wait_for_element(driver, By.XPATH, LOGIN_BUTTON_XPATH)
        login_button.click()

        # Validation: Wait for dashboard header to appear
        dashboard_header = wait_for_element(driver, By.XPATH, DASHBOARD_HEADER_XPATH, timeout=ELEMENT_TIMEOUT)
        assert dashboard_header.is_displayed(), "Dashboard header not visible. Login may have failed."

        # Additional Validation: Ensure URL has changed to dashboard
        WebDriverWait(driver, ELEMENT_TIMEOUT).until(
            lambda d: "dashboard" in d.current_url.lower()
        )
        assert "dashboard" in driver.current_url.lower(), (
            f"Expected to be on dashboard page, but current URL is: {driver.current_url}"
        )

    except AssertionError as ae:
        pytest.fail(f"Assertion failed: {str(ae)}")
    except Exception as e:
        pytest.fail(f"Test execution error: {str(e)}")
    finally:
        if driver:
            driver.quit()
