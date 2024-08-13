from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
import os

def clock_in_or_out():
    options = Options()
    # Uncomment if you want to run in headless mode
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920x1080')

    service = FirefoxService(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)

    try:
        driver.get('https://rochem.darwinbox.in/user/login')

        # Perform login
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.ID, "UserLogin_username"))).send_keys(os.getenv('EMAIL'))
        driver.find_element(By.ID, "UserLogin_password").send_keys(os.getenv('PASSWORD'))
        driver.find_element(By.ID, "login-submit").click()

        # Wait until the header is visible
        wait.until(EC.visibility_of_element_located((By.XPATH, '//header')))

        # Find the clock button in the header and click it
        clock_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//header//img[@src="/ms/dboxuilibrary/assets/dboxuilib_dist/www/assets/images/Clock.svg"]')))
       

        print("Clock-in/out successful.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

clock_in_or_out()
