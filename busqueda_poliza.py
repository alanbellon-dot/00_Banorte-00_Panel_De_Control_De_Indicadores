from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# --- SELECTORES ---
INPUT_POLIZA_VAL = (By.XPATH, "//input[@formcontrolname='poliza']")
BTN_BUSCAR_ESPECIFICO = (By.XPATH, "//button[contains(., 'Buscar') and contains(@class, 'mat-flat-button')]")
BTN_ACEPTAR_MODAL = (By.CSS_SELECTOR, "button.btn-aceptar")
INPUT_ID_CLIENTE = (By.XPATH, "//input[@data-placeholder='Asegurado.IdClienteUnico']")
INPUT_LIGA_CONSULTA = (By.XPATH, "//input[@data-placeholder='LigaConsulta']")
INPUT_VEHICULO_MODELO = (By.XPATH, "//input[@data-placeholder='Vehiculo.Modelo']")
INPUT_VEHICULO_USO = (By.XPATH, "//input[@data-placeholder='Vehiculo.Uso']")
INPUT_CONTRATANTE_NOMBRE = (By.XPATH, "//input[@data-placeholder='contratante.nombre']")
INPUT_CONTRATANTE_MATERNO = (By.XPATH, "//input[@data-placeholder='contratante.apellidoMaterno']")
INPUT_CONTRATANTE_PATERNO = (By.XPATH, "//input[@data-placeholder='contratante.apellidoPaterno']")
INPUT_PERSONA_NOMBRE = (By.XPATH, "//input[@data-placeholder='persona.nombre']")
INPUT_PERSONA_MATERNO = (By.XPATH, "//input[@data-placeholder='persona.apellidoMaterno']")
INPUT_PERSONA_PATERNO = (By.XPATH, "//input[@data-placeholder='persona.apellidoPaterno']")
INPUT_VEHICULO_COLOR_CLAVE = (By.XPATH, "//input[@data-placeholder='vehiculo.color.clave']")
INPUT_VEHICULO_MARCA_CLAVE = (By.XPATH, "//input[@data-placeholder='vehiculo.marca.clave']")
INPUT_VEHICULO_MODELO_MINUS = (By.XPATH, "//input[@data-placeholder='vehiculo.modelo']")
INPUT_VEHICULO_TIPO_CLAVE = (By.XPATH, "//input[@data-placeholder='vehiculo.tipo.clave']")
INPUT_VEHICULO_TIPO_VEHICULO_CLAVE = (By.XPATH, "//input[@data-placeholder='vehiculo.tipoVehiculo.clave']")
INPUT_VEHICULO_USO_CLAVE = (By.XPATH, "//input[@data-placeholder='vehiculo.uso.clave']")
BTN_GUARDAR = (By.XPATH, "//button[contains(normalize-space(), 'Guardar')]")
BTN_SELECCIONAR_APERTURAR = (By.XPATH, "//button[contains(., 'Seleccionar y aperturar')]")
BTN_ACEPTAR = (By.CSS_SELECTOR, "button.btn-aceptar")

class GestorPoliza:
    def __init__(self, bot_principal):
        # Recibimos el 'bot_principal'
        self.bot = bot_principal
        self.driver = bot_principal.driver 
        
        # CORRECCIÓN 1: Definimos 'self.wait' aquí para que funcione abajo
        self.wait = WebDriverWait(self.driver, 10)

    def seleccionar_poliza_activa(self):
        """
        Recorre la tabla, busca 'ACTIVA' y da click.
        """
        print("--- Buscando póliza ACTIVA en la tabla ---")
        
        xpath_filas = "//tbody/tr"
        
        try:
            # Esperamos filas
            self.wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath_filas)))
            filas = self.driver.find_elements(By.XPATH, xpath_filas)
            
            encontrada = False

            for indice, fila in enumerate(filas):
                # Buscamos estatus dentro de la fila
                celda_estatus = fila.find_element(By.XPATH, ".//td[contains(@class, 'cdk-column-estatus')]")
                texto_estatus = celda_estatus.text.strip().upper()
                
                print(f"Fila {indice + 1}: Estatus -> '{texto_estatus}'")

                if "ACTIVA" in texto_estatus:
                    print(">>> ¡Encontrada! Seleccionando póliza ACTIVA...")
                    
                    boton_seleccionar = fila.find_element(By.XPATH, ".//button[contains(., 'Seleccionar')]") # Nota: corregí 'SELECCIONAR' a 'Seleccionar' o case-insensitive por si acaso, aunque tu HTML dice 'Seleccionar'
                    
                    # Click JS
                    self.driver.execute_script("arguments[0].click();", boton_seleccionar)
                    
                    encontrada = True
                    break 
                
            if not encontrada:
                print("Alerta: Se recorrió toda la lista y ninguna póliza estaba ACTIVA.")

        except Exception as e:
            print(f"Error al intentar seleccionar la póliza: {e}")

    def consultar_poliza(self):
        print("--- Iniciando secuencia externa de consulta de póliza ---")
        
        # 1. Usamos funciones del bot principal para llenar datos
        self.bot._escribir(INPUT_POLIZA_VAL, "3104255")
        
        # Nota: Asegúrate de que este botón no esté tapado, si falla usa JS click
        self.bot._click(BTN_BUSCAR_ESPECIFICO)
        
        # 2. Ejecutamos la lógica de la tabla
        self.seleccionar_poliza_activa()

        btn_aceptar = self.wait.until(EC.element_to_be_clickable(BTN_ACEPTAR_MODAL))
        btn_aceptar.click()

        time.sleep(5)
        self.bot._escribir(INPUT_ID_CLIENTE, "1")

        self.bot._escribir(INPUT_LIGA_CONSULTA, "1")

        self.bot._escribir(INPUT_VEHICULO_MODELO, "1")

        self.bot._escribir(INPUT_VEHICULO_USO, "1")

        self.bot._escribir(INPUT_CONTRATANTE_NOMBRE, "1")

        self.bot._escribir(INPUT_CONTRATANTE_MATERNO, "1")

        self.bot._escribir(INPUT_CONTRATANTE_PATERNO, "1")
        
        self.bot._escribir(INPUT_PERSONA_NOMBRE, "1")

        self.bot._escribir(INPUT_PERSONA_MATERNO, "1")

        self.bot._escribir(INPUT_PERSONA_PATERNO, "1")

        self.bot._escribir(INPUT_VEHICULO_COLOR_CLAVE, "1")

        self.bot._escribir(INPUT_VEHICULO_MARCA_CLAVE, "1")

        self.bot._escribir(INPUT_VEHICULO_MODELO_MINUS, "1")

        self.bot._escribir(INPUT_VEHICULO_TIPO_CLAVE, "1")

        self.bot._escribir(INPUT_VEHICULO_TIPO_VEHICULO_CLAVE, "1")

        self.bot._escribir(INPUT_VEHICULO_USO_CLAVE, "1")

        self.bot._click(BTN_GUARDAR)

        time.sleep(6)

        self.bot._click(BTN_SELECCIONAR_APERTURAR)

        time.sleep(1)

        self.bot._click(BTN_ACEPTAR)



        print("--- Fin de secuencia externa ---")