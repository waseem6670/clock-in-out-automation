import os
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

def locate_clock_image():
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
        driver.find_element(By.ID, "UserLogin_username").send_keys(os.getenv('EMAIL'))
        driver.find_element(By.ID, "UserLogin_password").send_keys(os.getenv('PASSWORD'))
        driver.find_element(By.ID, "login-submit").click()
        
        logging.info("Logging-in successful.")

        # Wait and navigate to the dashboard
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//a[@href="/dashboard"]'))
        ).click()
        
        logging.info("Navigated to the dashboard.")
        
        # Wait and locate clock button by image src
        try:
            clock_image = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.XPATH, '//img[contains(@src, "Clock.svg")]'))
            )
            logging.info("Clock image located successfully.")
        except Exception as e:
            logging.error(f"Clock image not found: {e}")
            with open('page_source.html', 'w') as f:
                f.write(driver.page_source)
        
    finally:
        driver.quit()

if __name__ == "__main__":
    locate_clock_image()
