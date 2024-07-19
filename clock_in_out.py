from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def locate_clock_button():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920x1080')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get('https://rochem.darwinbox.in/dashboard')
        print("Opened dashboard page.")
        
        # Debug: Save page source to check content
        with open('page_source.html', 'w') as file:
            file.write(driver.page_source)
        print("Page source saved as 'page_source.html'. Check this file to verify element structure.")

        # Wait for the page to load properly
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//div/header'))
        )

        # Locate the clock button using the correct XPath
        clock_button_xpath = '//div/header//div//div[@class="section__right"]//ul//li[@class="clockinout_btn prevent-close"]//span//img[contains(@src, "Clock.svg")]'
        
        clock_button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, clock_button_xpath))
        )

        print("Clock button located successfully.")
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    locate_clock_button()
