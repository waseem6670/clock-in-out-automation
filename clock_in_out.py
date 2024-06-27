import os
import time
import random
from datetime import datetime
import pytz
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Get credentials from environment variables
EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')

# Define the website URL
URL = "https://rochem.darwinbox.in/user/login"

def login(driver):
    try:
        logging.info("Navigating to login page.")
        driver.get(URL)

        # Wait until the email field is present
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "login_email")))

        email_field = driver.find_element(By.ID, "login_email")
        password_field = driver.find_element(By.ID, "login_password")
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")

        email_field.send_keys(EMAIL)
        password_field.send_keys(PASSWORD)
        login_button.click()

        # Wait until the attendance button is present
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "attendance_button")))

        logging.info("Logged in successfully.")
        return True
    except Exception as e:
        logging.error(f"Login failed: {e}")
        return False

def clock_in_out(driver):
    try:
        logging.info("Navigating to attendance page.")
        attendance_button = driver.find_element(By.ID, "attendance_button")
        attendance_button.click()

        # Wait until the success message is present
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "attendance_success_message")))

        logging.info("Clock-in/clock-out successful.")
        return True
    except Exception as e:
        logging.error(f"Clock-in/clock-out failed: {e}")
        return False

def logout(driver):
    try:
        logging.info("Logging out.")
        logout_button = driver.find_element(By.ID, "logout_button")
        logout_button.click()
        
        # Wait until the login page is present
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "login_email")))
        
        logging.info("Logged out successfully.")
        return True
    except Exception as e:
        logging.error(f"Logout failed: {e}")
        return False

def main():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    # Time zone for IST
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    current_hour = now.hour
    current_minute = now.minute

    if now.weekday() == 6:  # 6 means Sunday
        logging.info("It's Sunday. No clock-in/clock-out required.")
        return

    if (8 <= current_hour < 9) or (17 <= current_hour < 18):
        # Generate a random delay within the specified range
        if 8 <= current_hour < 9:
            delay = random.randint(0, 30) * 60  # 0 to 30 minutes in seconds
        else:
            delay = random.randint(0, 30) * 60  # 0 to 30 minutes in seconds

        logging.info(f"Waiting for {delay // 60} minutes before clocking in/out.")
        time.sleep(delay)

        if login(driver):
            if clock_in_out(driver):
                logout(driver)

    driver.quit()

if __name__ == "__main__":
    main()
