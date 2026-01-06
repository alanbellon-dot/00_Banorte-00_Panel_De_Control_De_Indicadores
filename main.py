import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# --- 1. CONFIGURATION & STEALTH SETTINGS ---
chrome_options = Options()

# --- NEW: DISABLE PASSWORD SAVE PROMPTS ---
prefs = {
    "credentials_enable_service": False, 
    "profile.password_manager_enabled": False,
    "profile.password_manager_leak_detection": False
}
chrome_options.add_experimental_option("prefs", prefs)
# ------------------------------------------

# Removes the "Chrome is being controlled by automated software" notification
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

# Disables the blink features that websites use to detect Selenium
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

# Starts the browser maximized
chrome_options.add_argument("--start-maximized")

# --- 2. INITIALIZE THE DRIVER ---
driver = webdriver.Chrome(options=chrome_options)

try:
    # --- 3. THE AUTOMATION STEPS ---
    driver.get("https://aseguradoradigitaldesarrollo.web.app/iniciar-sesion")

    # Small sleep to let the page settle
    time.sleep(2)
    
    # Identify the username field (Using ID as requested, though formcontrolname is safer)
    username_field = driver.find_element(By.ID, "mat-input-0")
    username_field.send_keys("DEVBANORTE")

    # Identify the password field
    password_field = driver.find_element(By.ID, "mat-input-1")
    password_field.send_keys("12345678")

    # Finds the button and click it
    ingresar_login = driver.find_element(By.XPATH, "//button[contains(., 'Ingresar')]")
    ingresar_login.click()

    # The password prompt would normally appear here; with the prefs above, it won't.

    # Finds the burger menu and click it
    time.sleep(5)
    burger_menu = driver.find_element(By.XPATH, "//mat-icon[text()='menu']")
    burger_menu.click()

    # Finds the "Panel de control de Indicadores" button
    time.sleep(2)
    panel_control_indicadores = driver.find_element(By.XPATH, "//span[contains(normalize-space(), 'Panel de Control de Indicadores')]")
    panel_control_indicadores.click()

    # Finds Apertura Siniestro and click it
    time.sleep(2)
    apertura_siniestro = driver.find_element(By.XPATH, "//span[contains(normalize-space(), 'Apertura Siniestro')]")
    apertura_siniestro.click()

    # Fill in the reporter's information
    time.sleep(2)
    name = driver.find_element(By.XPATH, "//input[@data-placeholder='Nombre(s)']")
    name.send_keys("ANA")

    paternal_surname = driver.find_element(By.XPATH, "//input[@data-placeholder='Apellido Paterno']")
    paternal_surname.send_keys("TEST")

    maternal_surname = driver.find_element(By.XPATH, "//input[@data-placeholder='Apellido Materno']")
    maternal_surname.send_keys("TEST")

    phone_fields = driver.find_elements(By.CSS_SELECTOR, "input[formcontrolname='telefono']")
    phone_fields[0].send_keys("1111111111")
    phone_fields[1].send_keys("1111111111")

    
    xpath_policy_clear = "//mat-form-field[descendant::*[contains(text(), 'Número Póliza')]]//mat-icon[text()='clear']"
    xpath_inciso_clear = "//mat-form-field[descendant::*[contains(text(), 'Inciso')]]//mat-icon[text()='clear']"

    wait = WebDriverWait(driver, 10)

    # 1. Clean Póliza fild
    btn_policy = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_policy_clear)))
    btn_policy.click()

    # 2. Clean Inciso fild
    btn_start = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_inciso_clear)))
    btn_start.click() 
    
    without_poliza = driver.find_element(By.XPATH, "//span[contains(normalize-space(), 'Sin Póliza')]")
    without_poliza.click() 


    # Get a list of all inputs named "Nombre(s)"
    save_data_nombres_direction = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//input[@data-placeholder='Nombre(s)']")))
    
    # Select the second one (Python lists start at 0, so 1 is the second)
    save_data_nombres = save_data_nombres_direction[1]    
    save_data_nombres.click()
    save_data_nombres.send_keys("ANA")


    # Get a list of all inputs named "Apellido Paterno"
    save_data_paterno_direction = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//input[@data-placeholder='Apellido Paterno']")))
    
    # Select the second one (Python lists start at 0, so 1 is the second)
    save_data_paterno = save_data_paterno_direction[1]    
    save_data_paterno.click()
    save_data_paterno.send_keys("ANA")


    # Get a list of all inputs named "Apellido Materno"
    save_data_materno_direction = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//input[@data-placeholder='Apellido Materno']")))
    
    # Select the second one (Python lists start at 0, so 1 is the second)
    save_data_materno = save_data_materno_direction[1]    
    save_data_materno.click()
    save_data_materno.send_keys("NANA")




    time.sleep(6)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    print("Closing browser in 5 seconds...")
    time.sleep(5)