import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# ==========================================
# CONSTANTES DE CONFIGURACIÓN Y SELECTORES
# ==========================================

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
BTN_APERTURAR = (By.XPATH, "//button[contains(., 'Aperturar')]")
BTN_BUSCAR = (By.XPATH, "//button[contains(., 'Buscar')]")


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
    def __init__(self):
        """
        Este método se ejecuta automáticamente cuando creas el bot.
        Aquí configuramos todo lo necesario antes de empezar.
        """
        print("Inicializando configuración del Bot...")
        
        # 1. LIMPIEZA DE ZOMBIES (Movemos esto aquí adentro)
        try:
            os.system("taskkill /f /im chromedriver.exe >nul 2>&1")
            time.sleep(3) 
        except:
            pass

        # 2. CONFIGURACIÓN DE CHROME
        chrome_options = Options()
        
        # Desactivar guardar contraseñas
        prefs = {
            "credentials_enable_service": False, 
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False
        }
        chrome_options.add_experimental_option("prefs", prefs)

        # Configuración anti-detección y estabilidad
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--remote-allow-origins=*")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--start-maximized")

        # 3. INICIAR EL DRIVER (Guardamos el driver en 'self' para usarlo en todos lados)
        self.driver = webdriver.Chrome(options=chrome_options)
        
        # También guardamos el 'wait' general en self
        self.wait = WebDriverWait(self.driver, 10)
        
        print("Bot iniciado correctamente.")
    # --- MÉTODOS AYUDANTES (Wrappers) ---
    # Estos métodos nos ahorran escribir WebDriverWait una y otra vez
    
    def _click(self, locator):
        """Espera a que un elemento sea clickeable y le da click"""
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(locator)).click()

    def _escribir(self, locator, texto):
        """Espera a que un elemento sea visible, lo limpia y escribe texto"""
        element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(texto)

    def login(self):
        print("Navegando al login...")
        self.driver.get(URL_BASE)
        
        # Pequeña pausa de seguridad
        time.sleep(2)

        print("Ingresando credenciales...")
        # Usamos las constantes limpias en lugar de los valores sueltos
        self._escribir(INPUT_USER, USUARIO)
        self._escribir(INPUT_PASS, PASSWORD)
        
        print("Dando click en Ingresar...")
        self._click(BTN_INGRESAR)

    def navegar_a_apertura(self):
        """Navega desde el dashboard hasta la apertura de siniestro"""
        print("Navegando al menú de apertura...")
        
        # Damos un pequeño respiro para que la animación del login termine
        time.sleep(3) 
        
        # 1. Menú hamburguesa
        self._click(ICON_MENU)
        
        # 2. Panel de control
        self._click(BTN_PANEL_CONTROL)
        
        # 3. Apertura Siniestro
        self._click(BTN_APERTURA_SINIESTRO)

    def llenar_datos_reportante(self):
        """Llena la información inicial del reportante y limpia pólizas"""
        print("Llenando datos del reportante...")
        
        # Esperamos brevemente a que el formulario aparezca
        time.sleep(2)

        # Usamos las constantes limpias para los inputs
        self._escribir(INPUT_NOMBRE, "ANA")
        self._escribir(INPUT_PATERNO, "TEST")
        self._escribir(INPUT_MATERNO, "TEST")

        # --- CASO ESPECIAL: TELÉFONOS ---
        # Usamos el asterisco (*) para desempaquetar la tupla INPUTS_TELEFONO
        # Es equivalente a poner: find_elements(By.CSS_SELECTOR, "...")
        phones = self.driver.find_elements(*INPUTS_TELEFONO)
        
        if len(phones) >= 2:
            phones[0].send_keys("1111111111")
            phones[1].send_keys("1111111111")

        # --- LIMPIEZA DE CAMPOS ---
        print("Seleccionando opción 'Sin Póliza'...")
        
        # Botones de limpieza
        self._click(BTN_CLEAR_POLIZA)
        self._click(BTN_CLEAR_INCISO)
        self._click(BTN_SIN_POLIZA)

    def llenar_detalle_asegurado(self):
        """Maneja los campos repetidos (Nombre/Apellido) seleccionando el segundo elemento"""
        print("Llenando detalles del asegurado...")
        
        # Helper interno para no repetir la lógica de listas
        # Recibe 'locator' (la constante completa) en vez de solo el string
        def _llenar_segundo_input(locator, texto):
            elementos = self.wait.until(EC.presence_of_all_elements_located(locator))
            
            # Python cuenta desde 0, así que [1] es el segundo elemento
            if len(elementos) > 1:
                elementos[1].click()
                elementos[1].clear()
                elementos[1].send_keys(texto)

        # Ahora usamos las constantes limpias
        _llenar_segundo_input(INPUT_NOMBRE, "ANA")
        _llenar_segundo_input(INPUT_PATERNO, "ANA")
        _llenar_segundo_input(INPUT_MATERNO, "NANA")

    def llenar_info_siniestro(self):
        """Llena causa, vehículo, color y selecciona la fecha en el calendario"""
        print("Llenando información del siniestro...")

        # 1. Causa
        self._click(OPCION_CAUSA)
        self._click(OPCION_CAUSA_VAL)

        # 2. Placas / Inmueble
        self._escribir(INPUT_INMUEBLE, "ZZ11111")

        # 3. Color
        self._click(OPCION_COLOR)
        self._click(OPCION_COLOR_VAL)

        # 4. Calendario (Complejo)
        print("Seleccionando fecha hoy...")
        
        # Construimos el XPath dinámicamente usando la constante del path largo
        xpath_calendar_btn = f"//*[local-name()='path' and @d='{PATH_ICONO_CALENDARIO}']"
        
        # Buscamos el elemento (No usamos _click aquí porque necesitamos pasar el objeto al script JS)
        calendar_btn = self.driver.find_element(By.XPATH, xpath_calendar_btn)
        
        # Ejecutamos el click forzado con JavaScript
        self.driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('click', {bubbles: true}));", calendar_btn)
        
        # Click en la celda "Hoy" (aquí sí podemos usar el helper normal)
        self._click(BTN_CALENDARIO_HOY)
        self._escribir(INPUT_QUE_OCURRIO, "Choco muy feo")

    def llenar_ubicacion_y_finalizar(self):
        """Maneja el mapa, la dirección compleja y el botón final"""
        print("Configurando ubicación y mapa...")
        
        # 1. Tipo de Vialidad (Hover + Click)
        # Usamos * para desempaquetar la constante LBL_TIPO_VIALIDAD
        element = self.driver.find_element(*LBL_TIPO_VIALIDAD)
        ActionChains(self.driver).move_to_element(element).click().perform()
        
        self._click(OPCION_AVENIDA)

        # 2. Tipo Ubicación y Carretera
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

        time.sleep(4) # Pausa visual necesaria para que el mapa se acomode

        # 4. CLICK FINAL (APERTURAR)
        print("Finalizando apertura...")
        # Esperamos a que sea visible usando la constante
        boton_aperturar = self.wait.until(EC.visibility_of_element_located(BTN_APERTURAR))
        
        # Usamos ActionChains para asegurar que no lo tape el footer
        ActionChains(self.driver).move_to_element(boton_aperturar).click().perform()
        # 5. BUSCAR
        self._click(BTN_BUSCAR)



    def asignacion_manual(self):
        self._click(BTN_ESCOGER_SINIESTRO)

        print("Dando click en buscar persona...")
        self._click(BTN_ICONO_BUSCAR_PERSONA)

        print("Confirmando selección...")
        self._click(BTN_ACEPTAR)

        print("Dando click en el ícono de búsqueda de persona...")
        self._click(BTN_BUSCAR_PERSONA)

        """
        Busca todos los elementos con clase 'id-proveedor',
        elige uno aleatoriamente y le da click.
        """
        import random  # Importamos la librería para elegir al azar

        print("Buscando lista de proveedores disponibles...")
        
        try:
            # 1. Buscamos TODOS los elementos (nota el plural: presence_of_ALL_elements)
            # Esto devuelve una lista: [elemento1, elemento2, elemento3...]
            proveedores = self.wait.until(EC.presence_of_all_elements_located(LISTA_PROVEEDORES))

            if len(proveedores) > 0:
                # 2. Elegimos uno al azar de la lista
                elegido = random.choice(proveedores)
                
                # Obtenemos su texto para saber cuál fue (ej: "1769")
                id_texto = elegido.text
                print(f"I found {len(proveedores)} opciones. Seleccioné al azar el ID: {id_texto}")
                
                # 3. Damos el click
                # A veces es mejor dar click al padre si el span es muy pequeño, 
                # pero intentaremos directo primero.
                self.driver.execute_script("arguments[0].click();", elegido)
                # Nota: Usé execute_script porque a veces los elementos en tablas 
                # son difíciles de clickear con el .click() normal.
                
            else:
                print("Alerta: No se encontraron proveedores en la lista.")

        except Exception as e:
            print(f"Error al intentar seleccionar un proveedor: {e}")


        print("Dando click en 'Seleccionar ajustador'...")
        self._click(BTN_SELECCIONAR_AJUSTADOR)

        print("Finalizando asignación...")
        self._click(BTN_ASIGNAR_FINAL)





    def clic_asignar_siniestro(self):
        """
        Espera a que cargue la tabla y lee ÚNICAMENTE la primera fila.
        """
        print("Esperando a que la tabla de resultados cargue...")
        
        # 1. ESPERA DE SEGURIDAD (CRUCIAL)
        # Damos 10 segundos fijos para asegurar que la animación de carga termine
        # y la tabla vieja desaparezca si había una.
        time.sleep(10) 

        try:
            print("Buscando el primer registro...")
            
            # 2. Usamos WebDriverWait para esperar hasta que el elemento sea VISIBLE
            # Esto esperará hasta 10 segundos adicionales si el internet está lento
            celda_primer_siniestro = self.wait.until(EC.visibility_of_element_located(LBL_ESTATUS_SINIESTRO))
            
            # 3. Obtenemos el texto
            texto_estatus = celda_primer_siniestro.text.strip()
            
            print(f"Estatus encontrado en la fila 1: '{texto_estatus}'")

            # 4. Lógica de decisión
            if "Registrada" in texto_estatus:
                print(">>> Estatus: 'Registrada'. Procediendo a asignar...")
                self.asignacion_manual()
                
            elif "Asignada" in texto_estatus:
                print(">>> Estatus: 'Asignada'. El siniestro ya fue tomado. No hago nada.")
                
            else:
                print(f"Alerta: El estatus es '{texto_estatus}', no coincide con lo esperado.")

        except Exception as e:
            # Si cae aquí, es porque pasaron 15 segundos (5 del sleep + 10 del wait) y la tabla nunca salió.
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
    # --- CONFIGURACIÓN DE REPETICIONES ---
    CANTIDAD_VECES = int(input("Ingresa las veces que quieres ejecutar el proceso: "))  # <--- Cambia este número por las veces que quieras ejecutarlo
    
    bot = BanorteBot()
    try:
        # 1. LOGIN (Se ejecuta SOLO UNA VEZ al principio)
        bot.login()

        # 2. BUCLE DE EJECUCIÓN
        for i in range(CANTIDAD_VECES):
            print(f"\n>>> INICIANDO EJECUCIÓN NÚMERO: {i + 1} de {CANTIDAD_VECES} <<<")
            
            # Aquí inicia el ciclo repetitivo
            # Al llamar a navegar_a_apertura, el bot "resetea" la vista volviendo al menú
            bot.navegar_a_apertura()
            
            bot.llenar_datos_reportante()
            bot.llenar_detalle_asegurado()
            bot.llenar_info_siniestro()
            bot.llenar_ubicacion_y_finalizar()
            bot.clic_asignar_siniestro()
            
            print(f">>> Ejecución {i + 1} terminada con éxito.")
            
            # Una pequeña pausa para dar tiempo al sistema antes de volver al menú
            time.sleep(3)

        print("\n¡Todas las iteraciones han finalizado!")
        time.sleep(5)
        
    except Exception as e:
        print(f"Ocurrió un error durante la ejecución: {e}")
        # bot.driver.save_screenshot(f"error_iteracion.png")
        
    finally:
        bot.cerrar()