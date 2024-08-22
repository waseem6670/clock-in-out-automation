import os
from datetime import datetime, timedelta
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

# Coordinates for the clock button (replace with actual values)
CLOCKIN_X, CLOCKIN_Y = 927, 20  # Replace with actual clock-in button coordinates
CLOCKOUT_X, CLOCKOUT_Y = 927, 20  # Replace with actual clock-out button coordinates

# Function to perform click at specific coordinates
def click_at_coordinates(driver, x, y):
    driver.execute_script(f"document.elementFromPoint({x}, {y}).click();")

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
    
    try:
        driver.get('https://rochem.darwinbox.in/user/login')

        # Perform login
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.ID, "UserLogin_username"))).send_keys(os.getenv('EMAIL'))
        driver.find_element(By.ID, "UserLogin_password").send_keys(os.getenv('PASSWORD'))
        driver.find_element(By.ID, "login-submit").click()
        
        logging.info("Logging-in successful.")
        time.sleep(10)  # Wait for 10 seconds after successful login
        
        # Wait for the top bar to be visible
        wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="dbox-top-bar"]')))
        
        # Click based on action
        if action == "clockin":
            # click_at_coordinates(driver, CLOCKIN_X, CLOCKIN_Y)
            logging.info("Clock-in successful.")
        elif action == "clockout":
            # click_at_coordinates(driver, CLOCKOUT_X, CLOCKOUT_Y)
            logging.info("Clock-out successful.")
        else:
            logging.error("Invalid action specified.")
            return
        
    except Exception as e:
        logging.error(f"An error occurred during {action}: {e}")
    finally:
        driver.quit()

def main():
    now = datetime.utcnow() + timedelta(hours=5, minutes=30)  # Convert to IST
    current_time = now.strftime("%H:%M")
    
    logging.info(f"Current IST time: {current_time}")

    # Check if today is a leave day or Sunday
    leave = os.getenv('LEAVE', 'false').lower() == 'true'
    if leave or now.weekday() == 6:  # 6 represents Sunday
        logging.info("Today is a leave day or Sunday. No clock-in required.")
        return
    
    # Perform clock-in or clock-out
    clock_in_or_out("clockin")
    clock_in_or_out("clockout")

if __name__ == "__main__":
    main()
