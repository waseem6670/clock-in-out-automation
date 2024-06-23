from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from datetime import datetime
import os

# Define constants
LOGIN_URL = "https://rochem.darwinbox.in/user/login"
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

def clock_in_or_out(action):
    # Set up Chrome options for headless browser
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Initialize the WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        # Navigate to login page
        driver.get(LOGIN_URL)
        
        # Login
        driver.find_element(By.ID, "login_email").send_keys(EMAIL)
        driver.find_element(By.ID, "login_password").send_keys(PASSWORD)
        driver.find_element(By.NAME, "login_submit").click()
        
        # Wait for page to load
        time.sleep(5)
        
        # Click the clock in/out button
        if action == "clockin":
            clockin_button = driver.find_element(By.XPATH, "//*[@id='clockin_button']")
            clockin_button.click()
        elif action == "clockout":
            clockout_button = driver.find_element(By.XPATH, "//*[@id='clockout_button']")
            clockout_button.click()
        
        # Wait for the action to complete
        time.sleep(2)
    
    finally:
        # Close the browser
        driver.quit()

def is_leave_day():
    # Check if today is a leave day
    leave_dates = ["2024-06-01", "2024-06-02"]  # Example leave dates
    today = datetime.today().strftime('%Y-%m-%d')
    return today in leave_dates

def main():
    if datetime.today().weekday() == 6:  # 6 means Sunday
        return
    
    if is_leave_day():
        return
    
    # Determine the action based on the current time
    now = datetime.now()
    hour = now.hour

    if hour < 12:
        clock_in_or_out("clockin")
    else:
        clock_in_or_out("clockout")

if __name__ == "__main__":
    main()
