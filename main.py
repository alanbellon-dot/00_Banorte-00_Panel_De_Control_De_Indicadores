import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

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
# Fix WinError 10054 and connection problems
chrome_options.add_argument("--remote-allow-origins=*")
# Disables the blink features that websites use to detect Selenium
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

# Starts the browser maximized
chrome_options.add_argument("--start-maximized")



# --- ZOMBIE CLEANUP ---
try:
    os.system("taskkill /f /im chromedriver.exe >nul 2>&1")
    # We give the system time to release the resources
    time.sleep(3) 
except:
    pass
# ---------------------------


# --- 2. INITIALIZE THE DRIVER ---
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 10)

try:
    def login():
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

    def claim_open():
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

    def consult_policies():
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


        # 1. Clean Póliza fild
        btn_policy = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_policy_clear)))
        btn_policy.click()

        # 2. Clean Inciso fild
        btn_start = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_inciso_clear)))
        btn_start.click()
        
        without_poliza = driver.find_element(By.XPATH, "//span[contains(normalize-space(), 'Sin Póliza')]")
        without_poliza.click() 

    def insured_detail():
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

    def accident_information():
        # Información del siniestro
        # Cause
        dropdown = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "mat-select[placeholder='Causa']")))
        dropdown.click()

        automotive_collition = driver.find_element(By.XPATH, "//span[contains(normalize-space(), 'Colisión Automotriz')]")
        automotive_collition.click()
    
        vehicle_plates = driver.find_element(By.XPATH, "//input[@data-placeholder='Tipo de inmueble']")
        vehicle_plates.send_keys("ZZ11111")
        
        color_click =  WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "mat-select[placeholder='Color']")))
        color_click.click()

        color_car = driver.find_element(By.XPATH, "//span[contains(normalize-space(), 'BLUE ALASKA')]")
        color_car.click()

        # Locate the element
        calendar_button_path = "M19 3h-1V1h-2v2H8V1H6v2H5c-1.11 0-1.99.9-1.99 2L3 19c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V8h14v11zM7 10h5v5H7z"
        calendar_button = driver.find_element(By.XPATH, f"//*[local-name()='path' and @d='{calendar_button_path}']")

        # Execute JavaScript to click it
        driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('click', {bubbles: true}));", calendar_button)
        
        # Click today
        # Wait for the "Today" cell to be clickable
        today_cell = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".mat-calendar-body-today")))
        today_cell.click()

    def accident_location():
        # Ubicación del siniestro
        # 1. Find the text element like you did before
        element = driver.find_element(By.XPATH, "//span[normalize-space()='Tipo Vialidad']")

        # 2. Use ActionChains to move to it and click
        # This is more robust than a simple .click() for complex UI
        ActionChains(driver).move_to_element(element).click().perform()

        # Click "Avenida"
        type_of_road = driver.find_element(By.XPATH, "//span[contains(normalize-space(), 'Avenida')]")
        type_of_road.click()


        type_location = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "mat-select[formcontrolname='tipo_ubicacion']")))
        type_location.click()

        type_location_option = driver.find_element(By.XPATH, "//span[contains(normalize-space(), 'Tramo Carretera')]")
        type_location_option.click()

        road_type = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "mat-select[formcontrolname='tipo_carretera']")))
        road_type.click()

        road_type_option = driver.find_element(By.XPATH, "//span[contains(normalize-space(), 'Cuota')]")
        road_type_option.click()

        road_name = driver.find_element(By.XPATH, "//input[@data-placeholder='Nombre carretera']")
        road_name.send_keys("MEXICO-PUEBLA")

        road_km = driver.find_element(By.XPATH, "//input[@data-placeholder='Km']")
        road_km.send_keys("123")

        search_address = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "pac-target-input")))
        search_address.send_keys("Metrobús Nápoles, Avenida Insurgentes Sur, Colonia Nápoles, Mexico City, CDMX, Mexico" + Keys.ENTER)

        element = driver.find_element(By.CSS_SELECTOR, "mat-select[placeholder='Tipo Zona']")
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()

        time.sleep(4)  # Small pause to ensure the element is in view

        zone_type = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "mat-select[placeholder='Tipo Zona']")))
        zone_type.click()

        zone_type_option = driver.find_element(By.XPATH, "//span[contains(normalize-space(), 'Amarillo')]")
        zone_type_option.click()

        maximum_radius = driver.find_element(By.XPATH, "//input[@data-placeholder='Radio máximo']")
        maximum_radius.send_keys("200")

        number_photos = driver.find_element(By.XPATH, "//input[@data-placeholder='No. fotos máximo']")
        number_photos.send_keys("2")

    def opening_button():
        # Aperturar button
        button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//button[contains(., 'Aperturar')]")))

        #If you get an error saying ElementClickInterceptedException, it means a sticky header, 
        # footer, or popup is covering the button. We need to scroll to it first.

        # Scroll to element and click
        apertura_button = ActionChains(driver)
        apertura_button.move_to_element(button).click().perform()

    
    def search_button_click():
        search_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Buscar')]")))
        search_button.click()

    login()
    claim_open()
    consult_policies()
    insured_detail()
    accident_information()
    accident_location()
    opening_button()
    search_button_click()

    time.sleep(6)

except Exception as e:
    print(f"An error occurred: {e}")


finally:
    print("Closing browser in 5 seconds...")
    try:
        time.sleep(5)
    except KeyboardInterrupt:
        print("Interruption detected, closing immediately.")
    
    # It is recommended to add this line to free up Chrome memory.
    driver.quit()