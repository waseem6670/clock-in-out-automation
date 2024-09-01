import os
import logging
import time
from playwright.sync_api import sync_playwright

# Setup logging
logging.basicConfig(level=logging.INFO)

def clock_in_or_out(action):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=True for CI environments
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()
        
        try:
            page.goto('https://rochem.darwinbox.in/user/login')
            
            # Perform login
            page.fill('#UserLogin_username', os.getenv('EMAIL'))
            page.fill('#UserLogin_password', os.getenv('PASSWORD'))
            page.click('#login-submit')
            logging.info("Logging-in successful.")
            
            # Wait for the page to fully load (can be optimized)
            time.sleep(10)  # You might want to replace this with a more specific wait condition
            
            # Wait for the top bar to appear after login
            page.wait_for_selector('#dbox-top-bar')
            
            # Locate the element at the specified coordinates (927, 20)
            element = page.evaluate("document.elementFromPoint(927, 20);")
            
            if element:
                # Log information about the element
                logging.info(f"Element found at (927, 20): {element}")
                logging.info(f"Tag Name: {element.get('tagName', 'N/A')}")
                logging.info(f"Text: {element.get('innerText', '').strip()}")
                logging.info(f"Is Connected: {element.get('isConnected', False)}")
            else:
                logging.error("No element found at the specified coordinates.")
        except Exception as e:
            logging.error(f"An error occurred during {action}: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    clock_in_or_out("clockin")
