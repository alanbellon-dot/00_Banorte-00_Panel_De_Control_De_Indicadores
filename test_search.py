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
    driver.get("https://aseguradoradigitaldesarrollo.web.app/iniciar-sesion")

    # Handle the 'No soy un robot' / Cookies if they appear
    # On many Google versions, you might need to click "Accept all"
    # We add a small sleep just to let the page settle
    time.sleep(2)
    
    # Indentify the usernamename button
    username_field = driver.find_element(By.ID, "mat-input-0")

    # Typing usernamename button
    username_field.send_keys("DEVBANORTE")

    # Indentify the password button
    password_field = driver.find_element(By.ID, "mat-input-1")

    # Typing password button
    password_field.send_keys("12345678")

    # Click in login
    ingresar_login = driver.find_element(By.CSS_SELECTOR, "button.mat-flat-button.w-100")
    ingresar_login.click()

    
    time.sleep(6)



except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # --- 5. CLEANUP ---
    # Keeps the browser open for 5 seconds before closing so you can see the result
    print("Closing browser in 5 seconds...")
    time.sleep(5)
    driver.quit()