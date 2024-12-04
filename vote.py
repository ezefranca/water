from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time

# Constants
BASE_URL = "https://yazioen.featureupvote.com"
SUGGESTION_URL = f"{BASE_URL}/suggestions/92880/read-water-from-ios-apple-health-app"

def setup_driver():
    """Set up Selenium WebDriver."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Specify path to ChromeDriver
    service = Service("path/to/chromedriver")  # Replace with the path to your WebDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def get_csrf_token_and_vote(driver):
    """Fetch the CSRF token and perform a vote."""
    driver.get(SUGGESTION_URL)
    time.sleep(3)  # Allow page to load

    try:
        # Locate the vote button
        vote_button = driver.find_element(By.CLASS_NAME, "btn-upvote")

        # Extract the CSRF token from hx-vals attribute
        hx_vals = vote_button.get_attribute("hx-vals")
        if not hx_vals:
            raise ValueError("CSRF token not found.")
        
        csrf_token = hx_vals.split("csrf_token")[1].split(":")[1].split(",")[0].strip('"')
        print(f"Extracted CSRF Token: {csrf_token}")

        # Click the vote button
        ActionChains(driver).move_to_element(vote_button).click(vote_button).perform()
        print("Vote submitted successfully!")
    except Exception as e:
        print(f"Error during voting: {e}")

def main():
    driver = setup_driver()
    try:
        get_csrf_token_and_vote(driver)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
