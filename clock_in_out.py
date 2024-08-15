from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# Set up Chrome options to run with a visible browser window
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Comment this line out to disable headless mode
chrome_options.add_argument("--start-maximized")  # Optionally start maximized

# Specify the path to the chromedriver executable
service = Service('/path/to/chromedriver')

# Set up the WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

# Navigate to the Darwinbox login page
driver.get("https://your-darwinbox-url.com")

# Perform login
username = driver.find_element(By.ID, "username")
password = driver.find_element(By.ID, "password")
login_button = driver.find_element(By.ID, "loginButton")

username.send_keys("your_username")
password.send_keys("your_password")
login_button.click()
print("Logged in sucessfully")

# Add a delay to ensure the page has loaded completely
time.sleep(5)

# Attempt to find the clock-in/clock-out button
clock_button = driver.find_element(By.CSS_SELECTOR, "img[src='/ms/dboxuilibrary/assets/dboxuilib_dist/www/assets/images/Clock.svg']")

# Check if the button was found and interact with it
if clock_button:
    clock_button.click()
else:
    print("Clock-in/clock-out button not found")

# Optionally, close the browser
driver.quit()
