import os
from datetime import datetime, timedelta
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

# Function to find the clock button
def find_clock_button(driver):
    elements = driver.find_elements(By.TAG_NAME, 'img')  # Adjust the tag to your needs
    for element in elements:
        if 'clockin' in element.get_attribute('src') or 'clockout' in element.get_attribute('src'):  # Adjust based on image src or another attribute
            return element
    return None

# Function to perform clock in/out
def clock_in_or_out(action):
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920x1080')
    # options.add_argument('--headless')  # Uncomment this if you want to run in headless mode

    # Specify Chrome binary location if necessary
    # options.binary_location = "/path/to/chrome"  # Replace with the actual path to your Chrome executable

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
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="dbox-top-bar"]')))
        
        # Try finding the clock button
        clock_button = find_clock_button(driver)
        if not clock_button:
            clock_button = driver.execute_script("return document.querySelector('img[src*=\"clockin\"]');")  # Update with correct query
        
        if not clock_button:
            logging.error("Could not find the clock button.")
            return
        
        clock_button.click()
        logging.info(f"{action.capitalize()} successful.")
        
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
