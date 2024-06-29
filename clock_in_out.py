import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

EMAIL = "wasim.raja@rochem.in"
PASSWORD = "Rochem@123"
URL = "https://rochem.darwinbox.in/user/login"

def setup_driver():
    logging.info("Setting up the Chrome driver.")
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    return driver

def clock_in_or_out(action):
    logging.info(f"Attempting to {action}.")
    driver = setup_driver()
    driver.get(URL)
    time.sleep(5)  # Give the page time to load
    
    try:
        logging.info("Filling in the login form.")
        email_element = driver.find_element(By.ID, "UserLogin_username")
        password_element = driver.find_element(By.ID, "UserLogin_password")
        submit_button = driver.find_element(By.ID, "login-submit")
        
        if email_element and password_element and submit_button:
            email_element.send_keys(EMAIL)
            password_element.send_keys(PASSWORD)
            submit_button.click()
        else:
            logging.error("Login elements not found.")
        
        time.sleep(5)  # Wait for login to process
        logging.info("Logged in successfully.")
        
        # Navigate to the clock-in/clock-out button and click it
        button = driver.find_element(By.XPATH, "//button[@id='clockin_out_button_id']")
        if button:
            button.click()
            logging.info(f"{action.capitalize()} successful.")
        else:
            logging.error(f"Clock-in/clock-out button not found for {action}.")
            
    except Exception as e:
        logging.error(f"Failed to {action}: {e}")
    finally:
        driver.quit()

def main():
    logging.info("Starting clock-in/out script.")
    
    current_hour = time.gmtime().tm_hour + 5  # Convert UTC to IST
    current_minute = time.gmtime().tm_min + 30
    if current_minute >= 60:
        current_minute -= 60
        current_hour += 1

    if current_hour == 8 and 30 <= current_minute <= 59:
        logging.info("Performing clock-in.")
        clock_in_or_out("clock-in")
    elif current_hour == 17 and 30 <= current_minute <= 59:
        logging.info("Performing clock-out.")
        clock_in_or_out("clock-out")
    else:
        logging.info("Current time is not within the clock-in/out range.")

if __name__ == "__main__":
    main()
