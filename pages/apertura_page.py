from playwright.sync_api import Page, expect
import time
class AperturaPage:
    def __init__(self, page: Page):
        self.page = page

        # --- NAVEGACIÓN ---
        self.icon_menu = page.locator("mat-icon:text('menu')")
        self.btn_panel = page.locator("span", has_text="Panel de Control de Indicadores")
        self.btn_apertura_menu = page.locator("span", has_text="Apertura Siniestro")

        # --- DATOS ASEGURADO ---
        self.input_email = page.locator("input[formcontrolname='email']") # Este es el correo
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
        self.input_poliza_buscar = page.locator("input[formcontrolname='poliza']")
        self.input_endoso = page.locator("input[formcontrolname='endoso']")

        # Campo Oficina con autocompletado
        self.select_oficina = page.locator("input[formcontrolname='oficina']")
        self.opcion_oficina = page.get_by_role("option", name="80E")

        # Selector de producto (mat-select) y su opción específica
        self.dropdown_producto = page.locator("mat-select[formcontrolname='producto']")
        self.opcion_a000 = page.get_by_role("option", name="A000 - AUTOS GFNORTE")

        # Botón Buscar dentro del modal (usamos .last para evitar el de la página principal)
        self.btn_buscar_especifico = page.locator("button:has-text('Buscar')").last

        # Botón Seleccionar que aparece en la tabla de resultados
        self.btn_seleccionar_tabla = page.locator("button", has_text="Seleccionar").first

        # --- FORMULARIO DE ASEGURADO (DENTRO DEL MODAL) ---
        self.input_nombre_modal = page.locator("input[formcontrolname='nombre']")
        self.input_paterno_modal = page.locator("input[formcontrolname='apellido_paterno']")
        self.input_materno_modal = page.locator("input[formcontrolname='apellido_materno']")
        self.inputs_telefono_modal = page.locator("input[formcontrolname='telefono']")

        # Botones de cierre y confirmación
        self.btn_seleccionar_aperturar = page.locator("button:has-text('Seleccionar y aperturar')")
        self.btn_aceptar_modal_final = page.locator("button.btn-aceptar") # Selector específico para el botón rojo 'Aceptar'
                
                # Otros botones del flujo
        self.btn_aceptar_modal = page.locator("button.btn-accept, button.btn-aceptar").first
        self.btn_guardar = page.locator("button:has-text('Guardar')")
        self.btn_seleccionar_aperturar = page.locator("button:has-text('Seleccionar y aperturar')")

        # --- INFO SINIESTRO ---
        self.select_causa = page.locator('.mat-select-value:has-text("Causa")').first
        self.opcion_causa = page.locator("//span[contains(normalize-space(), 'Colisión Automotriz')]")
        self.input_placas = page.locator("//input[@data-placeholder='Placas Vehículo']")
        # ---Agregamos el selector de Descripción Vehículo ---
        self.input_desc_vehiculo = page.locator("//input[@data-placeholder='Descripción Vehículo']")
        self.select_color = page.locator('mat-select[placeholder="Color"]:not([formcontrolname="cCveColor"])')
        self.select_color = page.locator('mat-select[placeholder="Color"]:not([formcontrolname="cCveColor"])')
        self.opcion_color = page.get_by_role("option", name="AMARILLO", exact=True)
        self.btn_calendario_icon = page.locator("mat-datepicker-toggle button") 
        self.btn_dia_hoy = page.locator(".mat-calendar-body-today")
        self.input_que_ocurrio = page.locator("textarea[formcontrolname='que_ocurrio']")

        
        # --- INFO POLIZA ---
        self.select_causa = page.locator('.mat-select-value:has-text("Causa")').first
        self.opcion_colision = page.locator("mat-option", has_text="COLISION")
        self.select_color = page.locator('.mat-select-value:has-text("Color")').first
        self.opcion_color = page.get_by_role("option", name="AMARILLO", exact=True)
        self.select_relacion = page.locator("mat-select[formcontrolname='cCveRelacion']")
        self.opcion_relacion = page.locator("mat-option", has_text="PADRE")
        self.select_tipo_siniestro = page.locator("span.mat-select-placeholder", has_text="Tipo de siniestro")
        self.opcion_tipo_siniestro = page.locator("mat-option", has_text="Local")
        self.select_cve_color = page.locator('mat-select[formcontrolname="cCveColor"]')
        self.opcion_anaranjado = page.locator("mat-option", has_text="ANARANJADO")
        

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
         # Llenamos el correo aquí 
        print("Llenando correo del reportante...")
        self.input_email.fill("josemanuel@gmail.com")


    def _flujo_avanzado_poliza(self):
        print(">>> Iniciando flujo de Póliza AVANZADA...")
    
        # 1. Esperar modal y llenar Póliza/Endoso
        self.input_poliza_buscar.wait_for(state="visible", timeout=10000)
        self.input_poliza_buscar.fill("1000009")
        self.input_endoso.fill("1")

        # 2. Selección de Oficina '80E'
        print("Seleccionando Oficina 80E...")
        self.select_oficina.click()
        self.select_oficina.fill("80E")
        self.page.wait_for_timeout(1000) # Tiempo para que Angular cargue la lista
        self.opcion_oficina.click()

        # 3. Selección de Producto 'A000 - AUTOS GFNORTE'
        print("Seleccionando Producto...")
        self.dropdown_producto.click()
        self.page.wait_for_timeout(600)
        self.opcion_a000.click()

        # 4. Ejecutar Búsqueda
        print("Buscando póliza...")
        self.btn_buscar_especifico.click()

        # 5. Seleccionar de la tabla
        print("Esperando resultados...")
        try:
            self.btn_seleccionar_tabla.wait_for(state="visible", timeout=12000)
            self.btn_seleccionar_tabla.click()
        except Exception as e:
            print("❌ La tabla no mostró resultados o la póliza no es seleccionable.")
            self.page.screenshot(path="error_tabla.png")
            raise e

        # 6. Llenar datos del Asegurado (RAUL TEST TEST)
        print("Llenando datos personales en el modal...")
        self.page.wait_for_timeout(800)
        self.input_nombre_modal.fill("RAUL")
        self.input_paterno_modal.fill("TEST")
        self.input_materno_modal.fill("TEST")

        # 7. Llenar Teléfonos (5555555555)
        if self.inputs_telefono_modal.count() >= 2:
            self.inputs_telefono_modal.nth(0).fill("5555555555")
            self.inputs_telefono_modal.nth(1).fill("5555555555")
        
        # 8. Seleccionar y aperturar
        print("Finalizando selección...")
        self.btn_seleccionar_aperturar.scroll_into_view_if_needed()
        self.btn_seleccionar_aperturar.click()
        
        # 9. Botón Aceptar (Confirmación final del modal)
        self.btn_aceptar_modal_final.wait_for(state="visible", timeout=5000)
        self.btn_aceptar_modal_final.click()
        
        self.page.wait_for_timeout(2000)
        print("✅ Póliza avanzada configurada correctamente.")

    def datos_asegurado(self):
        print("Llenando datos del conductor...")
        
        # --- CAMBIO 1: El scroll ahora busca 'Datos del conductor' ---
        self.page.locator("text=Datos del conductor").first.scroll_into_view_if_needed()
        
        # --- HELPER BLINDADO ---
        def llenar(campo, valor):
            # --- CAMBIO 2: El xpath ahora busca 'Datos del conductor' ---
            xpath = f"//*[contains(text(), 'Datos del conductor')]/following::input[@data-placeholder='{campo}']"
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

                # --- NUEVO: Llenado blindado del correo ---
        print("Llenando correo del reportante de forma blindada...")
        
        # Buscamos el campo específicamente por cómo se ve en pantalla (su placeholder)
        input_correo = self.page.locator("input[data-placeholder='Email']").first
        
        # Hacemos scroll por si acaso
        input_correo.scroll_into_view_if_needed()
        self.page.wait_for_timeout(300)
        
        # 1. Clic, Llenar y Salir (Tab)
        input_correo.click()
        input_correo.fill("josemanuel@gmail.com")
        input_correo.press("Tab")
        
        # 2. Verificación de seguridad
        self.page.wait_for_timeout(500)
        if input_correo.input_value() != "josemanuel@gmail.com":
            print("⚠️ El correo no se guardó a la primera. Reintentando...")
            input_correo.click()
            input_correo.fill("josemanuel@gmail.com")
            input_correo.press("Tab")

        # Ejecutamos el llenado seguro
        llenar("Nombre(s)", "ANA")
        llenar("Apellido Paterno", "ANA")
        llenar("Apellido Materno", "NANA")

        print("Seleccionando género...")
        self.select_genero.scroll_into_view_if_needed()
        self.select_genero.click()
        self.page.wait_for_timeout(500) # Pausa breve para que Angular abra la lista animada
        self.opcion_genero.click()

    def llenar_siniestro_y_ubicacion(self, direccion_mapa):
        print("Llenando info siniestro y ubicación...")
        self.page.wait_for_timeout(500)
        
        # --- BLOQUE 1: Siniestro ---
        for selector, opcion in [
            (self.select_causa, self.opcion_colision),
            (self.select_color, self.opcion_color)
        ]:
            selector.click()
            opcion.click()

        self.input_placas.fill("ZZ11111")
        self.input_desc_vehiculo.fill("Auto bonito")
        self.input_que_ocurrio.fill("Choco muy feo")

        # --- CORRECCIÓN CALENDARIO ---
        print("Seleccionando fecha...")
        self.btn_calendario_icon.scroll_into_view_if_needed()
        self.btn_calendario_icon.click()
        self.page.wait_for_timeout(500)
        self.btn_dia_hoy.click(force=True)
        self.page.keyboard.press("Escape")

        # --- INFO POLIZA / CAUSA ---
        print("Seleccionando la causa del siniestro...")
        self.select_relacion.scroll_into_view_if_needed()
        self.page.wait_for_timeout(300) 
        self.select_relacion.click()
        self.page.wait_for_timeout(300) 
        self.opcion_relacion.click()
        
        print("Seleccionando Relación...")
        self.select_tipo_siniestro.click()
        self.page.wait_for_timeout(300)
        self.opcion_tipo_siniestro.click()

        # --- BLOQUE 2: Ubicación ---
        selects_ubicacion = [
            (self.select_vialidad, self.opcion_avenida),
            (self.select_tipo_ubicacion, self.opcion_tramo),
            (self.select_tipo_carretera, self.opcion_cuota)
        ]
        
        for selector, opcion in selects_ubicacion:
            selector.scroll_into_view_if_needed() 
            selector.click()
            opcion.click()

        self.input_nom_carretera.fill("MEXICO-PUEBLA")
        self.input_km.fill("123")

        # --- BLOQUE 3: Mapa ---
        self._buscar_en_mapa(direccion_mapa)

        # --- LÓGICA INTELIGENTE DE COLONIA Y C.P. ---
        print("Verificando si los datos postales ya fueron cargados por el mapa...")
        # Espera vital para que Angular propague los datos del mapa a los selectores
        self.page.wait_for_timeout(2000) 
        
        try:
            # Localizamos el contenedor del valor del C.P.
            select_cp = self.page.locator("mat-form-field").filter(has_text="C.P.").locator("mat-select").first
            
            # Extraemos el texto que está seleccionado actualmente en el C.P.
            # (En Angular Material, el texto visible suele estar en esta clase)
            valor_cp_actual = select_cp.locator(".mat-select-value-text").inner_text().strip()
            
            # Si el valor está vacío o es el placeholder, procedemos al llenado manual
            if not valor_cp_actual or valor_cp_actual == "":
                print("⚠️ El C.P. está vacío. Iniciando selección manual...")
                
                # 1. SELECCIONAR COLONIA
                print("Abriendo opciones de Colonia...")
                select_colonia = self.page.locator("mat-form-field").filter(has_text="Colonia").locator("mat-select").first
                select_colonia.scroll_into_view_if_needed()
                select_colonia.click(timeout=3000)
                self.page.wait_for_timeout(500)
                self.page.locator("mat-option").first.click()
                print("Colonia seleccionada.")

                self.page.wait_for_timeout(500)

                # 2. SELECCIONAR C.P.
                print("Abriendo opciones de C.P....")
                select_cp.scroll_into_view_if_needed()
                select_cp.click(timeout=3000)
                self.page.wait_for_timeout(500)
                self.page.locator("mat-option").first.click()
                print("C.P. seleccionado con éxito.")
            else:
                print(f"✅ Los datos ya están presentes (C.P. detectado: {valor_cp_actual}). No se requiere intervención.")

        except Exception as e:
            print(f"⚠️ Nota: Error al validar o llenar Colonia/C.P.: {e}")
            
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
        
        # 1. Hacemos scroll al botón
        self.btn_aperturar.scroll_into_view_if_needed()
        
        # --- CAMBIO 1: Le damos 3 segunditos a la página para que termine de decir "Cargando..." ---
        print("Esperando a que la página procese la ubicación...")
        self.page.wait_for_timeout(3000) 
        
        print(">>> Haciendo CLICK en Aperturar...")
        # --- CAMBIO 2: Quitamos el force=True. 
        # Ahora Playwright escaneará el botón y no le dará clic hasta que esté 100% habilitado.
        self.btn_aperturar.click()
        
        # 2. Esperamos inteligentemente: O aparece el botón "Buscar" O aparece un error
        try:
            # Aumentamos un poco el tiempo de espera por si la red está lenta
            self.btn_buscar_final.wait_for(state="visible", timeout=10000)
            print("✅ ¡Apertura exitosa! Botón Buscar detectado.")
            
            # Si apareció, le damos click para terminar el flujo
            self.btn_buscar_final.click()
            
        except:
            # 3. SI FALLA: DIAGNÓSTICO
            print("⚠️ ADVERTENCIA: No se detectó avance. Buscando errores en el formulario...")
            
            errores = self.page.locator("mat-error").all_inner_texts()
            if errores:
                print(f"❌ ERRORES ENCONTRADOS EN EL FORMULARIO: {errores}")
            else:
                print("❌ No veo errores de texto explícitos, pero el formulario no avanza.")

            # TOMA UNA CAPTURA DE PANTALLA
            nombre_foto = f"error_apertura_{self.page.context.pages.index(self.page)}.png"
            self.page.screenshot(path=nombre_foto, full_page=True)
            print(f"📸 Captura de pantalla guardada como: {nombre_foto} (Revisa la carpeta del proyecto)")
            
            raise Exception("El formulario no avanzó. Revisa la captura de pantalla.")