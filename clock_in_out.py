from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import logging
import time

# Setup logging
logging.basicConfig(level=logging.INFO)

def click_at_coordinates(driver, x, y):
    try:
        # Use ActionChains to move to the coordinates and click
        actions = ActionChains(driver)
        actions.move_by_offset(x, y).click().perform()
        logging.info(f"Clicked at coordinates ({x}, {y}).")
    except Exception as e:
        logging.error(f"An error occurred while clicking at coordinates: {e}")

def main():
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920x1080')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        driver.get('https://rochem.darwinbox.in/user/login')

        # Perform login
        driver.find_element(By.ID, "UserLogin_username").send_keys('your_email')
        driver.find_element(By.ID, "UserLogin_password").send_keys('your_password')
        driver.find_element(By.ID, "login-submit").click()
        
        logging.info("Login successful.")
        time.sleep(10)  # Wait for the page to load

        # Replace these coordinates with your actual x and y values
        x_coordinate = 927  # Replace with actual x-coordinate
        y_coordinate = 20  # Replace with actual y-coordinate

        logging.info("fond the co ordinate 927,20.")

        # Click at the specified coordinates
        # click_at_coordinates(driver, x_coordinate, y_coordinate)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
