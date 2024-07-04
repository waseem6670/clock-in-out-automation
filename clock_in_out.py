import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import datetime
import os
import random

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')
URL = "https://rochem.darwinbox.in/user/login"
LEAVE = os.getenv('LEAVE', 'false').lower() == 'true'

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
        email_element = driver.find_element(By.ID, "login_email")
        password_element = driver.find_element(By.ID, "login_password")
        submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        
        if email_element and password_element and submit_button:
            logging.info("Found login elements.")
            email_element.send_keys(EMAIL)
            password_element.send_keys(PASSWORD)
            submit_button.click()
        else:
            logging.error("Login elements not found.")
            return  # Exit the function if elements are not found
        
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

def run_at_random_minute(hour, start_minute, end_minute, action):
    random_minute = random.randint(start_minute, end_minute)
    target_time = datetime.datetime.combine(datetime.datetime.today(), datetime.time(hour, random_minute))
    now = datetime.datetime.now()
    
    if target_time < now:
        target_time += datetime.timedelta(days=1)  # If the target time is already past, schedule for the next day
    
    wait_time = (target_time - now).total_seconds()
    logging.info(f"Scheduled to {action} at {target_time.strftime('%H:%M')} (in {wait_time / 60:.2f} minutes)")
    
    time.sleep(wait_time)
    clock_in_or_out(action)

def main():
    logging.info("Starting clock-in/out script.")
    
    if LEAVE:
        logging.info("Today is marked as leave. No clock-in/out required.")
        return
    
    today = datetime.datetime.today()
    current_hour = today.hour + 5  # Convert UTC to IST
    current_minute = today.minute + 30
    if current_minute >= 60:
        current_minute -= 60
        current_hour += 1
    
    if today.weekday() == 6:  # Sunday is 6
        logging.info("Today is Sunday. No clock-in/out required.")
    elif 8 <= current_hour < 9:
        logging.info("Scheduling clock-in.")
        run_at_random_minute(8, 30, 59, "clock-in")
    elif 17 <= current_hour < 18:
        logging.info("Scheduling clock-out.")
        run_at_random_minute(17, 30, 59, "clock-out")
    else:
        logging.info("Current time is not within the clock-in/out range.")

if __name__ == "__main__":
    main()
