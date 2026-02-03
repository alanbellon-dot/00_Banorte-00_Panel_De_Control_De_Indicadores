import time
import os
from busqueda_poliza import GestorPoliza
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# --- DATOS DE ACCESO ---
URL_BASE = "https://aseguradoradigitaldesarrollo.web.app/iniciar-sesion"
USUARIO = "DEVBANORTE"
PASSWORD = "12345678"

# --- SELECTORES: LOGIN ---
INPUT_USER = (By.ID, "mat-input-0")
INPUT_PASS = (By.ID, "mat-input-1")
BTN_INGRESAR = (By.XPATH, "//button[contains(., 'Ingresar')]")

# --- SELECTORES: MENÚ NAVEGACIÓN ---
ICON_MENU = (By.XPATH, "//mat-icon[text()='menu']")
BTN_PANEL_CONTROL = (By.XPATH, "//span[contains(normalize-space(), 'Panel de Control de Indicadores')]")
BTN_APERTURA_SINIESTRO = (By.XPATH, "//span[contains(normalize-space(), 'Apertura Siniestro')]")

# --- SELECTORES: DATOS REPORTANTE ---
INPUT_NOMBRE = (By.XPATH, "//input[@data-placeholder='Nombre(s)']")
INPUT_PATERNO = (By.XPATH, "//input[@data-placeholder='Apellido Paterno']")
INPUT_MATERNO = (By.XPATH, "//input[@data-placeholder='Apellido Materno']")
INPUTS_TELEFONO = (By.CSS_SELECTOR, "input[formcontrolname='telefono']")

# --- SELECTORES: LIMPIEZA PÓLIZA ---
BTN_CLEAR_POLIZA = (By.XPATH, "//mat-form-field[descendant::*[contains(text(), 'Número Póliza')]]//mat-icon[text()='clear']")
BTN_CLEAR_INCISO = (By.XPATH, "//mat-form-field[descendant::*[contains(text(), 'Inciso')]]//mat-icon[text()='clear']")
BTN_SIN_POLIZA = (By.XPATH, "//span[contains(normalize-space(), 'Sin Póliza')]")

# --- SELECTORES: INFO SINIESTRO ---
OPCION_CAUSA = (By.CSS_SELECTOR, "mat-select[placeholder='Causa']")
OPCION_CAUSA_VAL = (By.XPATH, "//span[contains(normalize-space(), 'Colisión Automotriz')]")
INPUT_INMUEBLE = (By.XPATH, "//input[@data-placeholder='Tipo de inmueble']")
OPCION_COLOR = (By.CSS_SELECTOR, "mat-select[placeholder='Color']")
OPCION_COLOR_VAL = (By.XPATH, "//span[contains(normalize-space(), 'BLUE ALASKA')]")
BTN_CALENDARIO_HOY = (By.CSS_SELECTOR, ".mat-calendar-body-today")
# El path SVG es muy largo, lo dejamos aquí para no ensuciar la lógica
PATH_ICONO_CALENDARIO = "M19 3h-1V1h-2v2H8V1H6v2H5c-1.11 0-1.99.9-1.99 2L3 19c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V8h14v11zM7 10h5v5H7z"

# --- SELECTORES: UBICACIÓN ---
LBL_TIPO_VIALIDAD = (By.XPATH, "//span[normalize-space()='Tipo Vialidad']")
OPCION_AVENIDA = (By.XPATH, "//span[contains(normalize-space(), 'Avenida')]")
SELECT_TIPO_UBICACION = (By.CSS_SELECTOR, "mat-select[formcontrolname='tipo_ubicacion']")
OPCION_TRAMO = (By.XPATH, "//span[contains(normalize-space(), 'Tramo Carretera')]")
SELECT_TIPO_CARRETERA = (By.CSS_SELECTOR, "mat-select[formcontrolname='tipo_carretera']")
OPCION_CUOTA = (By.XPATH, "//span[contains(normalize-space(), 'Cuota')]")
INPUT_NOM_CARRETERA = (By.XPATH, "//input[@data-placeholder='Nombre carretera']")
INPUT_KM = (By.XPATH, "//input[@data-placeholder='Km']")
INPUT_GOOGLE_MAPS = (By.CLASS_NAME, "pac-target-input")
INPUT_QUE_OCURRIO = (By.CSS_SELECTOR, "textarea[formcontrolname='que_ocurrio']")

# --- BOTONES FINALES ---
BTN_APERTURAR = (By.XPATH, "//button[contains(., 'Aperturar') and not(contains(., 'Seleccionar'))]")
BTN_BUSCAR = (By.XPATH, "//button[contains(., 'Buscar') and not(contains(., 'person_search'))]")


# -- SELECTORES ASIGNAR --
BTN_ESCOGER_SINIESTRO = (By.XPATH, "//mat-icon[normalize-space()='more_vert']")
LBL_ESTATUS_SINIESTRO = (By.XPATH, "(//td[contains(@class, 'mat-column-estatus')])[1]")
BTN_ICONO_BUSCAR_PERSONA = (By.XPATH, "//mat-icon[normalize-space()='person_search']")
BTN_ACEPTAR = (By.CSS_SELECTOR, "button.btn-aceptar")
BTN_BUSCAR_PERSONA = (By.XPATH, "//mat-icon[normalize-space()='person_search']")
LISTA_PROVEEDORES = (By.CSS_SELECTOR, "span.id-proveedor")
BTN_SELECCIONAR_AJUSTADOR = (By.XPATH, "//button[contains(normalize-space(), 'Seleccionar ajustador')]")
BTN_ASIGNAR_FINAL = (By.XPATH, "//button[contains(normalize-space(), 'Asignar')]")

class BanorteBot:
    def __init__(self, usar_logica_avanzada=False):

        self.usar_logica_avanzada = usar_logica_avanzada
        """
        Este método se ejecuta automáticamente cuando creas el bot.
        Aquí configuramos todo lo necesario antes de empezar.
        """
        print("Inicializando configuración del Bot...")
        
        try:
            os.system("taskkill /f /im chromedriver.exe >nul 2>&1")
            time.sleep(3) 
        except:
            pass

        chrome_options = Options()

        prefs = {
            "credentials_enable_service": False, 
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False
        }
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--remote-allow-origins=*")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--start-maximized")

        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
        
        print("Bot iniciado correctamente.")
    
    def _click(self, locator, timeout=20):
        """
        Intenta dar click con espera explícita.
        Si falla por 'StaleElementReferenceException', reintenta una vez.
        """
        try:
            WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator)).click()
        except Exception:
            # Si falla el click normal (por ejemplo, algo lo tapa), intentamos con JS
            try:
                element = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
                self.driver.execute_script("arguments[0].click();", element)
            except Exception as e:
                print(f"No se pudo dar click al elemento {locator}: {e}")
                raise e

    def _escribir(self, locator, texto):
        element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(texto)

    def login(self):
        print("Navegando al login...")
        self.driver.get(URL_BASE)
        
        time.sleep(2)

        print("Ingresando credenciales...")
        self._escribir(INPUT_USER, USUARIO)
        self._escribir(INPUT_PASS, PASSWORD)
        
        print("Dando click en Ingresar...")
        self._click(BTN_INGRESAR)

    def navegar_a_apertura(self):
        print("Navegando al menú de apertura...")
        time.sleep(3) 
        self._click(ICON_MENU)
        self._click(BTN_PANEL_CONTROL)
        self._click(BTN_APERTURA_SINIESTRO)

    def llenar_datos_reportante(self):
        """Llena la información inicial del reportante y limpia pólizas"""
        print("Llenando datos del reportante...")
        
        time.sleep(2)
        self._escribir(INPUT_NOMBRE, "ANA")
        self._escribir(INPUT_PATERNO, "TEST")
        self._escribir(INPUT_MATERNO, "TEST")

        phones = self.driver.find_elements(*INPUTS_TELEFONO)
        
        if len(phones) >= 2:
            phones[0].send_keys("1111111111")
            phones[1].send_keys("1111111111")

        # --- CORRIGE LA INDENTACIÓN AQUÍ ---
        if self.usar_logica_avanzada:
            print(">>> Usando SECUENCIA PERSONALIZADA (Clase Externa)...")
            gestor = GestorPoliza(self)
            gestor.consultar_poliza()
        else:
            print(">>> Usando limpieza ESTÁNDAR (Original)...")
            self._click(BTN_CLEAR_POLIZA)
            # ESTAS LÍNEAS DEBEN ESTAR DENTRO DEL ELSE (MÁS A LA DERECHA)
            self._click(BTN_CLEAR_INCISO)
            self._click(BTN_SIN_POLIZA)

    def datos_asegurado(self):
        print("Llenando datos del asegurado...")
        
        def _llenar_segundo_input(locator, texto):
            elementos = self.wait.until(EC.presence_of_all_elements_located(locator))
            
            if len(elementos) > 1:
                elementos[1].click()
                elementos[1].clear()
                elementos[1].send_keys(texto)

        _llenar_segundo_input(INPUT_NOMBRE, "ANA")
        _llenar_segundo_input(INPUT_PATERNO, "ANA")
        _llenar_segundo_input(INPUT_MATERNO, "NANA")

    def llenar_info_siniestro(self):
        print("Llenando información del siniestro...")

        self._click(OPCION_CAUSA)
        self._click(OPCION_CAUSA_VAL)
        self._escribir(INPUT_INMUEBLE, "ZZ11111")
        self._click(OPCION_COLOR)
        self._click(OPCION_COLOR_VAL)

        print("Seleccionando fecha hoy...")
        
        xpath_calendar_btn = f"//*[local-name()='path' and @d='{PATH_ICONO_CALENDARIO}']"
        
        calendar_btn = self.driver.find_element(By.XPATH, xpath_calendar_btn)
        
        self.driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('click', {bubbles: true}));", calendar_btn)
        
        self._click(BTN_CALENDARIO_HOY)
        self._escribir(INPUT_QUE_OCURRIO, "Choco muy feo")

    def llenar_ubicacion_y_finalizar(self):
        """Maneja el mapa, la dirección compleja y el botón final"""
        print("Configurando ubicación y mapa...")
        
        element = self.driver.find_element(*LBL_TIPO_VIALIDAD)
        ActionChains(self.driver).move_to_element(element).click().perform()
        
        self._click(OPCION_AVENIDA)

        self._click(SELECT_TIPO_UBICACION)
        self._click(OPCION_TRAMO)

        self._click(SELECT_TIPO_CARRETERA)
        self._click(OPCION_CUOTA)

        self._escribir(INPUT_NOM_CARRETERA, "MEXICO-PUEBLA")
        self._escribir(INPUT_KM, "123")

        # 3. Búsqueda de dirección (Google Maps)
        print("Buscando dirección en mapa...")
        direc_completa = "Metrobús Nápoles, Avenida Insurgentes Sur, Colonia Nápoles, Mexico City, CDMX, Mexico" + Keys.ENTER
        self._escribir(INPUT_GOOGLE_MAPS, direc_completa)

        time.sleep(4) 

        print("Finalizando apertura...")

        # --- CAMBIO: Lógica robusta para dar click ---
        try:
            # 1. Esperamos a que el botón exista en el DOM (aunque esté oculto o deshabilitado)
            boton_aperturar = self.wait.until(EC.presence_of_element_located(BTN_APERTURAR))
            
            # 2. Hacemos scroll hasta el botón por si acaso
            self.driver.execute_script("arguments[0].scrollIntoView(true);", boton_aperturar)
            time.sleep(1)

            # 3. Forzamos el click con JavaScript (ignora bloqueos)
            print(">>> Intentando click forzado en Aperturar...")
            self.driver.execute_script("arguments[0].click();", boton_aperturar)
            
        except Exception as e:
            print(f"Error al intentar dar click en Aperturar: {e}")

        # --- MEJORA AQUÍ ---
        print("Esperando procesar apertura...")
        time.sleep(3) # Pequeña pausa de seguridad para que el backend procese
        
        # Usamos el nuevo _click robusto (que espera hasta 20s)
        print("Buscando botón 'Buscar'...")
        self._click(BTN_BUSCAR, timeout=20)



    def asignacion_manual(self):
        self._click(BTN_ESCOGER_SINIESTRO)

        print("Dando click en buscar persona...")
        self._click(BTN_ICONO_BUSCAR_PERSONA)

        print("Confirmando selección...")
        self._click(BTN_ACEPTAR)

        print("Dando click en el ícono de búsqueda de persona...")
        self._click(BTN_BUSCAR_PERSONA)

        import random 

        print("Buscando lista de proveedores disponibles...")
        
        try:

            proveedores = self.wait.until(EC.presence_of_all_elements_located(LISTA_PROVEEDORES))

            if len(proveedores) > 0:
                elegido = random.choice(proveedores)
                
                id_texto = elegido.text
                print(f"I found {len(proveedores)} opciones. Seleccioné al azar el ID: {id_texto}")

                self.driver.execute_script("arguments[0].click();", elegido)
                
            else:
                print("Alerta: No se encontraron proveedores en la lista.")

        except Exception as e:
            print(f"Error al intentar seleccionar un proveedor: {e}")

        time.sleep(1)
        print("Dando click en 'Seleccionar ajustador'...")
        self._click(BTN_SELECCIONAR_AJUSTADOR)
        time.sleep(1)
        print("Finalizando asignación...")
        self._click(BTN_ASIGNAR_FINAL)

    def clic_asignar_siniestro(self):
        print("Esperando a que la tabla de resultados cargue...")
        time.sleep(10) 
        try:
            print("Buscando el primer registro...")

            celda_primer_siniestro = self.wait.until(EC.visibility_of_element_located(LBL_ESTATUS_SINIESTRO))
            
            texto_estatus = celda_primer_siniestro.text.strip()
            
            print(f"Estatus encontrado en la fila 1: '{texto_estatus}'")

            if "Registrada" in texto_estatus:
                print(">>> Estatus: 'Registrada'. Procediendo a asignar...")
                self.asignacion_manual()
                
            elif "Asignada" in texto_estatus:
                print(">>> Estatus: 'Asignada'. El siniestro ya fue tomado. No hago nada.")
                
            else:
                print(f"Alerta: El estatus es '{texto_estatus}', no coincide con lo esperado.")

        except Exception as e:
            print("ERROR: No se encontró la tabla de resultados.")
            print("Posibles causas: La búsqueda no trajo resultados o el internet está muy lento.")
            print(f"Detalle técnico: {e}")

    def cerrar(self):
        """Método seguro para cerrar el navegador"""
        print("Cerrando navegador en 5 segundos...")
        try:
            time.sleep(5)
            self.driver.quit()
        except Exception as e:
            print(f"Error al cerrar: {e}")

if __name__ == "__main__":
    CANTIDAD_VECES = int(input("Ingresa las veces que quieres ejecutar el proceso: "))
    
    resp_menu = input("¿Deseas hacer busqueda de poliza? (si/no): ").lower().strip()
    activar_custom = (resp_menu == 'si' or resp_menu == 's')

    bot = BanorteBot(usar_logica_avanzada=activar_custom)
    
    try:
        bot.login()

        for i in range(CANTIDAD_VECES):
            print(f"\n>>> INICIANDO EJECUCIÓN NÚMERO: {i + 1} de {CANTIDAD_VECES} <<<")
            
            # --- BLOQUE TRY/EXCEPT DENTRO DEL CICLO ---
            try:
                bot.navegar_a_apertura()
                bot.llenar_datos_reportante()
                bot.datos_asegurado()
                bot.llenar_info_siniestro()
                bot.llenar_ubicacion_y_finalizar()
                bot.clic_asignar_siniestro()
                print(f">>> Ejecución {i + 1} terminada con éxito.")

            except Exception as e:
                # Si algo falla, lo atrapamos aquí para que el ciclo continúe
                print(f"!!! ERROR CRÍTICO EN LA ITERACIÓN {i + 1}: {e}")
                print("Intentando recuperar el navegador refrescando la página...")
                
                try:
                    bot.driver.refresh()
                    time.sleep(5) # Espera a que recargue
                except:
                    pass # Si falla el refresh, la siguiente iteración intentará navegar de todas formas
            
            time.sleep(3)
            
        print("\n¡Todas las iteraciones han finalizado!")
        time.sleep(5)
        
    except Exception as e:
        print(f"Error fatal fuera del ciclo (posiblemente login): {e}")
        
    finally:
        bot.cerrar()