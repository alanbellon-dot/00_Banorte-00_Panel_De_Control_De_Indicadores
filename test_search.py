import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# --- 1. CONFIGURATION & STEALTH SETTINGS ---
chrome_options = Options()

# Removes the "Chrome is being controlled by automated software" notification
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

# Disables the blink features that websites use to detect Selenium
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

# Starts the browser maximized
chrome_options.add_argument("--start-maximized")

# --- 2. INITIALIZE THE DRIVER ---
# Selenium Manager (in Selenium 4.x) will automatically download the driver for you
driver = webdriver.Chrome(options=chrome_options)

try:
    # --- 3. THE AUTOMATION STEPS ---
    print("Navigating to Google...")
    driver.get("https://www.google.com")

    # Handle the 'No soy un robot' / Cookies if they appear
    # On many Google versions, you might need to click "Accept all"
    # We add a small sleep just to let the page settle
    time.sleep(2)

    print("Locating search box...")
    # 'q' is the name attribute for the Google search input
    search_box = driver.find_element(By.NAME, "q")

    print("Typing search query...")
    search_text = "Selenium Python automation is working!"
    
    # Typing one by one to look more human
    for char in search_text:
        search_box.send_keys(char)
        time.sleep(0.1) 
    
    # Press Enter
    search_box.send_keys(Keys.RETURN)

    # Wait for results to load
    time.sleep(3)

    # --- 4. VERIFICATION ---
    print(f"Test Finished! Page title is: {driver.title}")
    
    # Save a screenshot as proof of work
    driver.save_screenshot("test_result.png")
    print("Screenshot saved as 'test_result.png'")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # --- 5. CLEANUP ---
    # Keeps the browser open for 5 seconds before closing so you can see the result
    print("Closing browser in 5 seconds...")
    time.sleep(5)
    driver.quit()