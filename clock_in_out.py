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

# Coordinates to inspect (replace with your values)
INSPECT_X, INSPECT_Y = 927, 20

# Function to print element details at specific coordinates
def print_element_details_at_coordinates(driver, x, y):
    try:
        element = driver.execute_script(f"return document.elementFromPoint({x}, {y});")
        if element:
            logging.info(f"Element found at ({x}, {y}):")
            logging.info(f"Tag Name: {element.tag_name}")
            
            # Safely log attributes
            attributes = element.get_property('attributes')
            if attributes:
                attributes_info = []
                for attr in attributes:
                    attr_name = attr['name']
                    attr_value = attr['value']
                    attributes_info.append(f'{attr_name}: {attr_value}')
                logging.info(f"Attributes: {attributes_info}")
            else:
                logging.info("No attributes found.")
            
            logging.info(f"Text: {element.text}")
        else:
            logging.info(f"No element found at ({x}, {y}).")
    except Exception as e:
        logging.error(f"An error occurred while fetching element details: {e}")

# Function to perform clock in/out (just as a placeholder)
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
        
        # Print element details at specified coordinates
        print_element_details_at_coordinates(driver, INSPECT_X, INSPECT_Y)
        
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

if __name__ == "__main__":
    main()
