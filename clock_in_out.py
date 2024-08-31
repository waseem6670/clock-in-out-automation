import os
import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Setup logging
logging.basicConfig(level=logging.INFO)

def clock_in_or_out(action):
    options = Options()
    # Commenting out headless for debugging purposes
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
        
        # Wait for the hydrated topbar to appear after login
        time.sleep(10)  # Waiting for the page to fully load (can be optimized)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".div > header > div > div.section__right > ul > li.clockinout_btn.prevent-close > span > img")))  # Replace with actual selector

        # Locate the clock-in/out button within the hydrated topbar
        script = "return document.elementFromPoint(927, 20);"
        element = driver.execute_script(script)
        
        if element:
            logging.info(f"Element found at (927, 20): {element.tag_name}")
            logging.info(f"Text: {element.text.strip()}")
            
            # Ensure the element is interactable
            if element.is_displayed() and element.is_enabled():
                driver.execute_script("arguments[0].click();", element)
                logging.info("Click action performed on the element.")
            else:
                logging.error("Element at the specified coordinates is not interactable.")
        else:
            logging.error("No element found at the specified coordinates.")
    except Exception as e:
        logging.error(f"An error occurred during {action}: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    clock_in_or_out("clockin")
