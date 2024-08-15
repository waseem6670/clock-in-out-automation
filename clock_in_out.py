import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# Function to login and list actionable elements
def list_actionable_elements():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920x1080')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    # Go to Darwinbox login page
    driver.get('https://rochem.darwinbox.in/user/login')
    
    # Perform login
    driver.find_element(By.ID, "UserLogin_username").send_keys(os.getenv('EMAIL'))
    driver.find_element(By.ID, "UserLogin_password").send_keys(os.getenv('PASSWORD'))
    driver.find_element(By.ID, "login-submit").click()
    
    # Give time for login to complete
    driver.implicitly_wait(10)
    
    # List all actionable elements (buttons, links, images with onclick events)
    print("Listing all actionable elements:")
    
    elements = driver.find_elements(By.XPATH, "//*[@href] | //*[@onclick] | //button | //input[@type='button'] | //img[@src]")
    for i, element in enumerate(elements, start=1):
        print(f"{i}: Tag: {element.tag_name}, Text: {element.text}, Attributes: {element.get_attribute('outerHTML')[:100]}...")

    driver.quit()

if __name__ == "__main__":
    list_actionable_elements()
