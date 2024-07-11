import os
from datetime import datetime, timedelta
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup logging
# Remove logging configuration since we are not using logging for all image elements anymore

# Function to perform clock in/out
def clock_in_or_out(action, driver):
    # Perform clock-in or clock-out action based on 'action' parameter
    try:
        # Find the <img> tag with Clock.svg
        clock_img = driver.find_element(By.CSS_SELECTOR, 'img[src="/ms/dboxuilibrary/assets/dboxuilib_dist/www/assets/images/Clock.svg"]')

        # Navigate up to the parent element or identify the correct element containing the clock-in/clock-out functionality
        clock_parent_element = clock_img.find_element(By.XPATH, './parent::*')

        # Perform click action on the identified clock-in/clock-out element
        clock_parent_element.click()

        # Optionally, add a wait to ensure the click action completes before continuing
        time.sleep(2)  # Adjust the delay as needed

        # Log success
        print(f"{action.capitalize()} successful.")

    except Exception as e:
        print(f"Error occurred during {action}: {str(e)}")

def main():
    now = datetime.utcnow() + timedelta(hours=5, minutes=30)  # Convert to IST
    current_time = now.strftime("%H:%M")
    
    # Define clock-in and clock-out time ranges
    clock_in_start = "08:30"
    clock_in_end = "09:00"
    clock_out_start = "17:30"
    clock_out_end = "23:00"

    print(f"Current IST time: {current_time}")
    print(f"Clock-in time range: {clock_in_start} - {clock_in_end}")
    print(f"Clock-out time range: {clock_out_start} - {clock_out_end}")

    # Check if today is a leave day or Sunday
    leave = os.getenv('LEAVE', 'false').lower() == 'true'
    if leave or now.weekday() == 6:  # 6 represents Sunday
        print("Today is a leave day or Sunday. No clock-in required.")
        return
    
    # Random delay within the time range
    if clock_in_start <= current_time <= clock_in_end:
        delay = random.randint(0, 30) * 60  # Random delay between 0 and 30 minutes
        print(f"Waiting for {delay // 60} minutes before clocking in.")
        time.sleep(delay)
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
        
        time.sleep(2)  # Wait for login to complete
        print(f"Logging-in successful.")
        clock_in_or_out("clockin", driver)
        driver.quit()
    elif clock_out_start <= current_time <= clock_out_end:
        delay = random.randint(0, 3) * 60  # Random delay between 0 and 30 minutes
        print(f"Waiting for {delay // 60} minutes before clocking out.")
        time.sleep(delay)
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
        
        time.sleep(2)  # Wait for login to complete
        print(f"Logging-in successful.")
        clock_in_or_out("clockout", driver)
        driver.quit()
    else:
        print("Current time is not within the clock-in/out range.")

if __name__ == "__main__":
    main()
