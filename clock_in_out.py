import os
import logging
import time
from playwright.sync_api import sync_playwright

# Setup logging
logging.basicConfig(level=logging.INFO)

def clock_in_or_out(action):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False for debugging
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
            
            # Wait for the hydrated topbar to appear after login
            page.wait_for_selector('#dbox-top-bar')  # Replace with actual selector
            
            # Locate the clock-in/out button within the hydrated topbar
            element = page.evaluate("document.elementFromPoint(927, 20);")
            
            if element:
                logging.info(f"Element found at (927, 20): {element['tagName']}")
                logging.info(f"Text: {element['innerText'].strip()}")
                
                # Ensure the element is interactable
                if page.is_visible(f"{element['tagName']}") and page.is_enabled(f"{element['tagName']}"):
                    # page.click(f"{element['tagName']}")
                    logging.info("Click action performed on the element.")
                else:
                    logging.error("Element at the specified coordinates is not interactable.")
            else:
                logging.error("No element found at the specified coordinates.")
        except Exception as e:
            logging.error(f"An error occurred during {action}: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    clock_in_or_out("clockin")
