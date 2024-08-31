import os
from datetime import datetime, timedelta
import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup logging
logging.basicConfig(level=logging.INFO)

# Function to perform clock in/out
def clock_in_or_out(action):
    options = Options()
    # Uncomment the line below to run in headless mode after debugging
    # options.add_argument('--headless')  
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
        
        # Wait for the topbar to be hydrated and the clock-in/out button to be clickable
        clock_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Clock')]")))

        # Debug information
        logging.info(f"Clock button found: {clock_button}")
        logging.info(f"Is button displayed? {clock_button.is_displayed()}")
        logging.info(f"Is button enabled? {clock_button.is_enabled()}")
        
        # Click the button if found
        if clock_button.is_displayed() and clock_button.is_enabled():
            clock_button.click()
            logging.info("Clock-in/out button clicked.")
        else:
            logging.error("Clock-in/out button is not interactable.")
            
    except Exception as e:
        logging.error(f"An error occurred during {action}: {e}")
    finally:
        # Save screenshot for debugging
        driver.save_screenshot(f"{action}_screenshot.png")
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
