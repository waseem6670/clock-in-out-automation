# Function to find the clock button with additional debugging
def find_clock_button(driver):
    # Log the page title to confirm we're on the correct page
    logging.info(f"Page title: {driver.title}")

    # Attempt to find the clock button by inspecting the header
    try:
        # This assumes the header contains the button with an 'img' tag and a unique 'src' attribute
        clock_button = driver.find_element(By.CSS_SELECTOR, "header img[src*='clock']")
        if clock_button:
            logging.info("Clock button found using CSS selector.")
            return clock_button
    except Exception as e:
        logging.warning(f"Clock button not found with CSS selector: {e}")

    # If the above fails, attempt to find the button by iterating through images
    elements = driver.find_elements(By.TAG_NAME, 'img')
    logging.info(f"Found {len(elements)} image elements. Attempting to locate clock button...")

    for element in elements:
        src = element.get_attribute('src')
        logging.info(f"Inspecting image with src: {src}")
        if 'clockin' in src or 'clockout' in src:
            logging.info("Clock button found by inspecting image elements.")
            return element

    logging.error("Clock button not found after inspecting all image elements.")
    return None

# Function to perform clock in/out
def clock_in_or_out(action):
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920x1080')
    
    # Optional: Uncomment this line to see the browser
    # options.add_argument('--headless')
    
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
        time.sleep(10)  # Wait for 10 seconds after successful login

        # Ensure the page is fully loaded and the header is visible
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "header")))

        # Try finding the clock button
        clock_button = find_clock_button(driver)
        if not clock_button:
            logging.error("Could not find the clock button. Aborting.")
            return
        
        clock_button.click()
        logging.info(f"{action.capitalize()} successful.")
    except Exception as e:
        logging.error(f"An error occurred during {action}: {e}")
    finally:
        driver.quit()

def main():
    now = datetime.utcnow() + timedelta(hours=5, minutes=30)  # Convert to IST
    current_time = now.strftime("%H:%M")

    logging.info(f"Current IST time: {current_time}")

    # Check if today is a leave day or Sunday
    leave = os.getenv('LEAVE', 'false').lower() == 'true'
    if leave or now.weekday() == 6:  # 6 represents Sunday
        logging.info("Today is a leave day or Sunday. No clock-in required.")
        return

    # Perform clock-in or clock-out
    clock_in_or_out("clockin")
    clock_in_or_out("clockout")

if __name__ == "__main__":
    main()
