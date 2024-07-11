import os
from datetime import datetime, timedelta
import random
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Setup logging
logging.basicConfig(level=logging.INFO)

# Function to perform clock in/out
def clock_in_or_out(action):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920x1080')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    driver.get('https://rochem.darwinbox.in/user/login')
    
    # Perform login
    driver.find_element(By.ID, "UserLogin_username").send_keys(os.getenv('EMAIL'))
    driver.find_element(By.ID, "UserLogin_password").send_keys(os.getenv('PASSWORD'))
    driver.find_element(By.ID, "login-submit").click()
    
    try:
        # Wait for the new page to load by waiting for a known element on the new page
        new_page_element_xpath = '//*[@id="dbox-top-bar"]'
        WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, new_page_element_xpath)))
        logging.info("New page loaded successfully.")

        # Define the XPATH or CSS selector for the SVG element
        svg_xpath = 'https://rochem.darwinbox.in/ms/dboxuilibrary/assets/dboxuilib_dist/www/assets/images/Clock.svg'  # Update this XPATH based on actual SVG element location

        # Perform clock in/out by searching for the SVG element
        WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, svg_xpath)))
        clock_button = driver.find_element(By.XPATH, svg_xpath)
        
        driver.execute_script("arguments[0].click();", clock_button)
        
        logging.info(f"{action.capitalize()} successful.")
    except TimeoutException:
        logging.error(f"TimeoutException: Could not find the clock-in/clock-out element.")
        # Capture the page source for debugging
        page_source = driver.page_source
        with open("page_source.html", "w", encoding="utf-8") as f:
            f.write(page_source)
        logging.info("Page source saved to page_source.html for debugging.")
    finally:
        driver.quit()

def main():
    now = datetime.utcnow() + timedelta(hours=5, minutes=30)  # Convert to IST
    current_time = now.strftime("%H:%M")
    
    # Define clock-in and clock-out time ranges
    clock_in_start = "08:30"
    clock_in_end = "09:00"
    clock_out_start = "17:30"
    clock_out_end = "23:00"

    logging.info(f"Current IST time: {current_time}")
    logging.info(f"Clock-in time range: {clock_in_start} - {clock_in_end}")
    logging.info(f"Clock-out time range: {clock_out_start} - {clock_out_end}")

    # Check if today is a leave day or Sunday
    leave = os.getenv('LEAVE', 'false').lower() == 'true'
    if leave or now.weekday() == 6:  # 6 represents Sunday
        logging.info("Today is a leave day or Sunday. No clock-in required.")
        return
    
    # Random delay within the time range
    if clock_in_start <= current_time <= clock_in_end:
        delay = random.randint(0, 5) * 60  # Random delay between 0 and 30 minutes
        logging.info(f"Waiting for {delay // 60} minutes before clocking in.")
        time.sleep(delay)
        clock_in_or_out("clockin")
    
    elif clock_out_start <= current_time <= clock_out_end:
        delay = random.randint(0, 5) * 60  # Random delay between 0 and 30 minutes
        logging.info(f"Waiting for {delay // 60} minutes before clocking out.")
        time.sleep(delay)
        clock_in_or_out("clockout")
    
    else:
        logging.info("Current time is not within the clock-in/out range.")

if __name__ == "__main__":
    main()
