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

# Setup logging
logging.basicConfig(level=logging.INFO)

def clock_in_or_out(action):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920x1080')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        driver.get('https://rochem.darwinbox.in/user/login')

        # Perform login
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.ID, "UserLogin_username"))).send_keys(os.getenv('EMAIL'))
        driver.find_element(By.ID, "UserLogin_password").send_keys(os.getenv('PASSWORD'))
        driver.find_element(By.ID, "login-submit").click()
        
        logging.info(f"Logging-in successful.")
        time.sleep(10)  # Wait for 10 seconds after successful login
        
        # Wait for the top bar to be visible
        wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="dbox-top-bar"]')))
        
        # Attempt to find the clock button using multiple methods
        clock_button = None
        
        # Method 1: Find by image source
        clock_button = driver.execute_script("""
            var imgs = document.getElementsByTagName('img');
            for (var i = 0; i < imgs.length; i++) {
                if (imgs[i].src.includes('clockin') || imgs[i].src.includes('clockout')) {
                    return imgs[i];
                }
            }
            return null;
        """)
        
        # Method 2: Try finding by XPath or CSS Selector (Modify the selector based on your page structure)
        if not clock_button:
            try:
                clock_button = driver.find_element(By.XPATH, '//*[@id="dbox-top-bar"]//img[contains(@src, "clock")]')
            except Exception as e:
                logging.error(f"XPath method failed: {e}")

        # Method 3: Check if clock button is hidden in a dropdown or additional tab
        if not clock_button:
            try:
                clock_button = driver.execute_script("""
                    var clockin = document.querySelector('a[href*="clockin"]');
                    var clockout = document.querySelector('a[href*="clockout"]');
                    return clockin || clockout;
                """)
            except Exception as e:
                logging.error(f"JavaScript query method failed: {e}")

        if not clock_button:
            logging.error("Could not find the clock button.")
            return

        # Click the clock button using JavaScript
        driver.execute_script("arguments[0].click();", clock_button)
        
        logging.info(f"{action.capitalize()} successful.")
    except Exception as e:
        logging.error(f"An error occurred during {action}: {e}")
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
        delay = random.randint(0, 30) * 60  # Random delay between 0 and 30 minutes
        logging.info(f"Waiting for {delay // 60} minutes before clocking in.")
        time.sleep(delay)
        clock_in_or_out("clockin")
    
    elif clock_out_start <= current_time <= clock_out_end:
        delay = random.randint(0, 3) * 60  # Random delay between 0 and 30 minutes
        logging.info(f"Waiting for {delay // 60} minutes before clocking out.")
        time.sleep(delay)
        clock_in_or_out("clockout")
    
    else:
        logging.info("Current time is not within the clock-in/out range.")

if __name__ == "__main__":
    main()
