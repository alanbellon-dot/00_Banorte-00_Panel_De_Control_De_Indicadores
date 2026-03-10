from playwright.sync_api import Page, expect
import time
class AperturaPage:
    def __init__(self, page: Page):
        self.page = page

        # --- NAVEGACIÓN ---
        self.icon_menu = page.locator("mat-icon:text('menu')")
        self.btn_panel = page.locator("span", has_text="Panel de Control de Indicadores")
        self.btn_apertura_menu = page.locator("span", has_text="Apertura Siniestro")

        # --- REPORTANTE ---
        self.input_nombre = page.locator("//input[@data-placeholder='Nombre(s)']")
        self.input_paterno = page.locator("//input[@data-placeholder='Apellido Paterno']")
        self.input_materno = page.locator("//input[@data-placeholder='Apellido Materno']")
        self.inputs_telefono = page.locator("input[formcontrolname='telefono']")
        self.select_genero = page.locator("mat-select[formcontrolname='genero']")
        self.opcion_genero = page.locator("mat-option:has-text('FEMENINO')")

        # --- PÓLIZA (BASICA) ---
        self.btn_clear_poliza = page.locator("//mat-form-field[descendant::*[contains(text(), 'Número Póliza')]]//mat-icon[text()='clear']")
        self.btn_clear_inciso = page.locator("//mat-form-field[descendant::*[contains(text(), 'Inciso')]]//mat-icon[text()='clear']")
        self.btn_sin_poliza = page.locator("//span[contains(normalize-space(), 'Sin Póliza')]")

        # --- PÓLIZA (AVANZADA) ---
        self.input_poliza_buscar = page.locator("//input[@formcontrolname='poliza']")
        self.btn_buscar_especifico = page.locator("//button[contains(., 'Buscar') and contains(@class, 'mat-flat-button')]")
        self.btn_aceptar_modal = page.locator("button.btn-aceptar")
        self.btn_guardar = page.locator("//button[contains(normalize-space(), 'Guardar')]")
        self.btn_seleccionar_aperturar = page.locator("span", has_text="Seleccionar y aperturar")   
        self.dropdown_producto = self.page.locator("mat-select[formcontrolname='producto']")
        self.opcion_a003 = self.page.get_by_role("option", name="A003")
        self.select_oficina = page.locator("mat-select[formcontrolname='oficina']")
        self.opcion_oficina = page.get_by_role("option", name="80E")
        self.input_endoso = page.locator("input[formcontrolname='endoso']")

        # --- INFO SINIESTRO ---
        self.select_causa = page.locator('.mat-select-value:has-text("Causa")').first
        self.opcion_causa = page.locator("//span[contains(normalize-space(), 'Colisión Automotriz')]")
        self.input_placas = page.locator("//input[@data-placeholder='Placas Vehículo']")
        self.select_color = page.locator('mat-select[placeholder="Color"]:not([formcontrolname="cCveColor"])')
        self.opcion_color = page.get_by_role("option", name="AMARILLO", exact=True)
        self.btn_calendario_icon = page.locator("mat-datepicker-toggle button") 
        self.btn_dia_hoy = page.locator(".mat-calendar-body-today")
        self.input_que_ocurrio = page.locator("textarea[formcontrolname='que_ocurrio']")

        
        # --- INFO POLIZA ---
        self.select_causa_poliza = page.locator('mat-select[formcontrolname="cCveCausa"]')
        self.opcion_causa_poliza = page.locator("mat-option", has_text="COLISI")
        self.select_relacion = page.locator("mat-select[placeholder='Relación']").first
        self.opcion_conductor = page.locator("mat-option", has_text="CONDUCTOR")
        self.select_cve_color = page.locator('mat-select[formcontrolname="cCveColor"]')
        self.opcion_anaranjado = page.locator("mat-option", has_text="ANARANJADO")
        self.select_estado = page.locator('mat-select[formcontrolname="cCodEstado"]')
        self.opcion_cdmx = page.locator("mat-option", has_text="CIUDAD DE MÉXICO")
        self.select_ciudad = page.locator('mat-select[formcontrolname="cCodCiudad"]')
        self.opcion_benito_juarez = page.locator("mat-option", has_text="BENITO JUÁREZ")
        self.select_tipo_siniestro = page.locator("span.mat-select-placeholder", has_text="Tipo de siniestro")
        self.opcion_local = page.locator("mat-option", has_text="Local")

        # --- UBICACIÓN ---
        self.select_vialidad = page.locator("//span[normalize-space()='Tipo Vialidad']").first
        self.opcion_avenida = page.locator("//span[contains(normalize-space(), 'Avenida')]")
        self.select_tipo_ubicacion = page.locator("mat-select[formcontrolname='tipo_ubicacion']")
        self.opcion_tramo = page.locator("//span[contains(normalize-space(), 'Tramo Carretera')]")
        self.select_tipo_carretera = page.locator("mat-select[formcontrolname='tipo_carretera']")
        self.opcion_cuota = page.locator("//span[contains(normalize-space(), 'Cuota')]")
        self.input_nom_carretera = page.locator("//input[@data-placeholder='Nombre carretera']")
        self.input_km = page.locator("//input[@data-placeholder='Km']")
        self.input_google_maps = page.locator(".pac-target-input")

        # --- FINALIZAR ---
        self.btn_aperturar = page.locator("//button[contains(., 'Aperturar') and not(contains(., 'Seleccionar'))]")
        self.btn_buscar_final = page.locator("//button[contains(., 'Buscar') and not(contains(., 'person_search'))]")

    
    def navegar_al_modulo(self):
        print("Navegando al menú Apertura...")
        self.icon_menu.click()
        self.btn_panel.click()
        self.btn_apertura_menu.click()

    def llenar_reportante(self):
        print("Llenando reportante...")
        # Llenado en una sola pasada
        datos = [
            (self.input_nombre, "ANA"),
            (self.input_paterno, "TEST"),
            (self.input_materno, "TEST")
        ]
        for input_field, valor in datos:
            input_field.nth(0).fill(valor)
        
        # Llenado de teléfonos (si existen)
        if self.inputs_telefono.count() >= 2:
            self.inputs_telefono.nth(0).fill("1111111111")
            self.inputs_telefono.nth(1).fill("1111111111")

    def gestionar_poliza(self, usar_logica_avanzada=False):
        # Si es avanzada, ejecutamos y salimos (Return Anticipado)
        if usar_logica_avanzada:
            print(">>> Usando lógica AVANZADA...")
            self._flujo_avanzado_poliza()
            return

        print(">>> Usando limpieza ESTÁNDAR...")
        # Iteramos los botones de limpieza para ahorrar líneas
        for btn in [self.btn_clear_poliza, self.btn_clear_inciso]:
            if btn.is_visible():
                btn.click()
        
        self.btn_sin_poliza.click()

    def _flujo_avanzado_poliza(self):
        print("--- Iniciando búsqueda avanzada ---")
        self.input_poliza_buscar.fill("1000007") 
        self.input_endoso.fill("1")
        self.dropdown_producto.click()
        self.opcion_a003.click()
        self.select_oficina.click()
        self.opcion_oficina.click()
        self.btn_buscar_especifico.click()

        print("Esperando a que aparezca la póliza ACTIVA en la tabla...")
        
        # Definimos qué estamos buscando: Una fila (tr) que tenga texto "ACTIVA"
        # Usamos .first para evitar el error de múltiples elementos
        fila_activa = self.page.locator("tr").filter(has_text="ACTIVA").first
        
        try:
            # --- CAMBIO CRÍTICO ---
            # En lugar de preguntar "si es visible" (que no espera),
            # le ordenamos: "ESPERA hasta 15 segundos a que aparezca"
            fila_activa.wait_for(state="visible", timeout=150000)
            
            print(">>> Póliza ACTIVA aparecio. Dando click en Seleccionar...")
            
            # Una vez visible, buscamos el botón dentro de esa fila
            fila_activa.locator("button", has_text="Seleccionar").click()
            
        except Exception as e:
            # Si falla, tomamos foto para ver qué había en la tabla
            print("❌ Error: No apareció la fila ACTIVA a tiempo.")
            self.page.screenshot(path="debug_tabla_error.png")
            raise e

        # --- RESTO DEL FLUJO (Modales y Formulario Masivo) ---
        print("Manejando modales...")
        try:
            self.btn_aceptar_modal.click(timeout=3000)
        except:
            print("Modal inicial no apareció, continuamos.")

        print("Llenando formulario masivo de póliza...")
        self.page.wait_for_timeout(1000) 
        
        
        print("Seleccionando y aperturando...")
        # Esperamos botón final
        self.btn_seleccionar_aperturar.click()
        
        # Confirmación final
        self.btn_aceptar_modal.click()
        
        # Espera para volver al formulario principal
        self.page.wait_for_timeout(2000)


    def datos_asegurado(self):
        print("Llenando datos asegurado...")
        
        # Hacemos scroll al título para asegurar que la sección cargue
        self.page.locator("text=Datos asegurado").first.scroll_into_view_if_needed()
        
        # --- HELPER BLINDADO ---
        def llenar(campo, valor):
            # Construimos el selector
            xpath = f"//*[contains(text(), 'Datos asegurado')]/following::input[@data-placeholder='{campo}']"
            loc = self.page.locator(xpath).first
            
            # 1. Intentamos llenar y salir del campo (Tab)
            loc.fill(valor)
            loc.press("Tab")
            
            # 2. VERIFICACIÓN DE SEGURIDAD
            # Si el campo está vacío después de llenarlo, lo hacemos de nuevo más lento
            if loc.input_value() != valor:
                print(f"⚠️ El campo '{campo}' no agarró el dato. Reintentando...")
                self.page.wait_for_timeout(500) # Pequeña pausa
                loc.click() # Enfocamos
                loc.fill(valor)
                loc.press("Tab")

        # Ejecutamos el llenado seguro
        llenar("Nombre(s)", "ANA")
        llenar("Apellido Paterno", "ANA")
        llenar("Apellido Materno", "NANA")

        print("Seleccionando género...")
        self.select_genero.click()
        self.page.wait_for_timeout(500) # Pausa breve para que Angular abra la lista animada
        self.opcion_genero.click()

    def llenar_siniestro_y_ubicacion(self):
        print("Llenando info siniestro y ubicación...")
        self.page.wait_for_timeout(500)
        
        # --- BLOQUE 1: Siniestro ---
        for selector, opcion in [
            (self.select_causa, self.opcion_causa),
            (self.select_color, self.opcion_color)
        ]:
            selector.click()
            opcion.click()

        self.input_placas.fill("ZZ11111")
        self.input_que_ocurrio.fill("Choco muy feo")

        # --- CORRECCIÓN CALENDARIO ---
        print("Seleccionando fecha...")
        # 1. Aseguramos que el icono del calendario esté visible
        self.btn_calendario_icon.scroll_into_view_if_needed()
        self.btn_calendario_icon.click()

        # 2. Esperamos un poco a que la animación del calendario termine
        self.page.wait_for_timeout(500)

        # 3. Usamos force=True para ignorar si se sigue moviendo un poco o si está medio tapado
        self.btn_dia_hoy.click(force=True)

        # 4. Presionamos ESC por si acaso el calendario no se cerró solo (buena práctica)
        self.page.keyboard.press("Escape")

        # Info poliza

        print("Seleccionando la causa del siniestro...")
        self.select_causa_poliza.scroll_into_view_if_needed()
        self.page.wait_for_timeout(300) # Mini pausa para que la cámara se estabilice

        # 1. Clic para abrir el dropdown
        self.select_causa_poliza.click()
        
        # 2. Pausa breve para que Angular despliegue las opciones visualmente
        self.page.wait_for_timeout(300) 
        
        # 3. Clic en la opción COLISION
        self.opcion_causa_poliza.click()
        
        print("Seleccionando Relación...")
        
        # 1. Abrimos el dropdown de Relación
        self.select_relacion.click()
        
        # 2. Esperamos a que la animación de Angular despliegue la lista
        self.page.wait_for_timeout(300)
        
        # 3. Damos clic en CONDUCTOR
        self.opcion_conductor.click()

        print("Seleccionando el segundo Color (cCveColor)...")
        
        # 1. Clic para desplegar la lista de colores
        self.select_cve_color.click()
        
        # 2. Pausa obligatoria de Angular para que termine la animación
        self.page.wait_for_timeout(300)
        
        # 3. Clic en ANARANJADO
        self.opcion_anaranjado.click()

        print("Seleccionando el Código de Estado...")
        
        # 1. Abrir la lista de estados
        self.select_estado.click()
        
        # 2. Pausa para la animación de Angular Material
        self.page.wait_for_timeout(300)
        
        # 3. Seleccionar Ciudad de México
        self.opcion_cdmx.click()

        print("Seleccionando el Código de Ciudad...")
        
        # 1. Clic para abrir la lista de ciudades
        self.select_ciudad.click()
        
        # 2. Pausa obligatoria para la animación de Angular
        self.page.wait_for_timeout(300)
        
        # 3. Seleccionar Benito Juárez
        self.opcion_benito_juarez.click()

        # 4. Tipo de siniestro
        self.select_tipo_siniestro.click()

        # 5. Escogemos el siniestro
        self.opcion_local.click()


        # --- BLOQUE 2: Ubicación ---
        selects_ubicacion = [
            (self.select_vialidad, self.opcion_avenida),
            (self.select_tipo_ubicacion, self.opcion_tramo),
            (self.select_tipo_carretera, self.opcion_cuota)
        ]
        
        for selector, opcion in selects_ubicacion:
            # Scroll al elemento antes de clickearlo para evitar errores de viewport
            selector.scroll_into_view_if_needed() 
            selector.click()
            opcion.click()

        self.input_nom_carretera.fill("MEXICO-PUEBLA")
        self.input_km.fill("123")

        # --- BLOQUE 3: Mapa ---
        self._buscar_en_mapa("Metrobús Nápoles, Avenida Insurgentes Sur, Colonia Nápoles, Mexico City, CDMX, Mexico")

    def _buscar_en_mapa(self, direccion):
        """Lógica blindada para Google Maps aislada"""
        print(f"Buscando en Maps: {direccion[:20]}...")
        
        self.input_google_maps.click()
        self.input_google_maps.press_sequentially(direccion, delay=10)
        
        try:
            self.page.wait_for_selector(".pac-item", timeout=5000)
            self.page.keyboard.press("ArrowDown")
            self.page.wait_for_timeout(200)
            self.page.keyboard.press("Enter")
        except:
            print("⚠️ Sin sugerencias, usando Enter directo.")
            self.page.keyboard.press("Enter")

        # Espera vital para que se llenen los campos
        self.page.wait_for_timeout(2000)

    def enviar_apertura(self):
        print("Finalizando apertura...")
        
        # 1. Intentamos dar clic en Aperturar
        # A veces es necesario hacer scroll para asegurar que el botón esté en vista
        self.btn_aperturar.scroll_into_view_if_needed()
        self.page.wait_for_timeout(500) # Pequeña pausa de estabilidad
        
        print(">>> Haciendo CLICK en Aperturar...")
        self.btn_aperturar.click(force=True)
        
        # 2. Esperamos inteligentemente: O aparece el botón "Buscar" O aparece un error
        try:
            # Esperamos máximo 5 segundos a que aparezca el botón de éxito (Buscar)
            self.btn_buscar_final.wait_for(state="visible", timeout=5000)
            print("✅ ¡Apertura exitosa! Botón Buscar detectado.")
            
            # Si apareció, le damos click para terminar el flujo
            self.btn_buscar_final.click()
            
        except:
            # 3. SI FALLA (No apareció el botón Buscar en 5 segs): DIAGNÓSTICO
            print("⚠️ ADVERTENCIA: No se detectó avance. Buscando errores en el formulario...")
            
            # Buscamos mensajes de error comunes de Angular Material (mat-error)
            errores = self.page.locator("mat-error").all_inner_texts()
            if errores:
                print(f"❌ ERRORES ENCONTRADOS EN EL FORMULARIO: {errores}")
            else:
                print("❌ No veo errores de texto explícitos, pero el formulario no avanza.")

            # TOMA UNA CAPTURA DE PANTALLA
            nombre_foto = f"error_apertura_{self.page.context.pages.index(self.page)}.png"
            self.page.screenshot(path=nombre_foto, full_page=True)
            print(f"📸 Captura de pantalla guardada como: {nombre_foto} (Revisa la carpeta del proyecto)")
            
            # Lanzamos el error para que el script sepa que falló esta iteración
            raise Exception("El formulario no avanzó. Revisa la captura de pantalla.")