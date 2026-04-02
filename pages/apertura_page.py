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
        self.input_endoso = page.locator("input[formcontrolname='endoso'], [data-placeholder='Inciso']").first
        self.select_oficina = page.locator("input[formcontrolname='oficina']")
        self.opcion_oficina = page.locator("mat-option", has_text="80E - UABC")
        self.dropdown_producto = page.locator("mat-select[formcontrolname='producto']")
        self.opcion_a000 = page.locator("mat-option", has_text="A000 - AUTOS GFNORTE")

        # Botón Buscar
        self.btn_buscar_especifico = page.locator("button").filter(has=page.locator("span.mat-button-wrapper", has_text="Buscar")).last

        # Botón Seleccionar de la tabla
        self.btn_seleccionar_tabla = page.locator("button[status='primary']", has_text="Seleccionar").first

        # --- FORMULARIO ASEGURADO ---
        self.input_nombre_modal = page.locator("input[formcontrolname='nombre']")
        self.input_paterno_modal = page.locator("input[formcontrolname='apellido_paterno']")
        self.input_materno_modal = page.locator("input[formcontrolname='apellido_materno']")
        
        # Selectores de teléfono
        self.inputs_telefono_modal = page.locator("input[formcontrolname='telefono']")

        # Botones de cierre y confirmación del flujo avanzado
        self.btn_seleccionar_aperturar = page.locator("button:has-text('Seleccionar y aperturar')")
        self.btn_aceptar_modal_final = page.locator("button.btn-accept, button.btn-aceptar").first
        self.btn_guardar = page.locator("button:has-text('Guardar')")

        # --- INFO SINIESTRO Y POLIZA ---
        self.input_desc_vehiculo = page.locator("input[formcontrolname='descripcion_vehiculo']")
        self.input_que_ocurrio = page.locator("textarea[formcontrolname='que_ocurrio']")
        self.input_placas = page.locator("input[data-placeholder='Placas Vehículo']").first
        
        # Calendario
        self.btn_calendario_icon = page.locator("mat-datepicker-toggle button").first
        self.btn_dia_hoy = page.locator(".mat-calendar-body-today").first
        
        # Causa
        self.select_causa = page.locator("mat-form-field:has-text('Causa') mat-select").first
        self.opcion_colision = page.locator("mat-option", has_text="COLISION").first
        
        # Relación
        self.select_relacion = page.locator("mat-select[formcontrolname='cCveRelacion']")
        self.opcion_relacion = page.locator("mat-option", has_text="PADRE").first
        
        # Color
        self.select_color = page.locator("mat-select[formcontrolname='cCveColor']")
        self.opcion_color = page.locator("mat-option", has_text="AMARILLO").first
        
        # Tipo de siniestro
        self.select_tipo_siniestro = page.locator("mat-select[placeholder='Tipo de siniestro']")
        self.opcion_tipo_siniestro = page.locator("mat-option", has_text="Local").first

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
        datos = [
            (self.input_nombre, "ANA"),
            (self.input_paterno, "TEST"),
            (self.input_materno, "TEST")
        ]
        for input_field, valor in datos:
            input_field.nth(0).fill(valor)
        
        if self.inputs_telefono.count() >= 2:
            self.inputs_telefono.nth(0).fill("1111111111")
            self.inputs_telefono.nth(1).fill("1111111111")

    def gestionar_poliza(self, usar_logica_avanzada=False):
        if usar_logica_avanzada:
            print(">>> Usando lógica AVANZADA...")
            self._flujo_avanzado_poliza()
            return

        print(">>> Usando limpieza ESTÁNDAR...")
        for btn in [self.btn_clear_poliza, self.btn_clear_inciso]:
            if btn.is_visible():
                btn.click()
        
        self.btn_sin_poliza.click()
        print("Llenando correo del reportante...")
        self.input_email.fill("josemanuel@gmail.com")

    def _flujo_avanzado_poliza(self):
        print(">>> Iniciando flujo de Póliza AVANZADA...")
    
        self.input_poliza_buscar.wait_for(state="visible", timeout=15000)
        self.page.wait_for_load_state("networkidle") 
        
        self.input_poliza_buscar.click()
        self.input_poliza_buscar.fill("1000002")
        print("Póliza ingresada: 1000002")

        try:
            self.input_endoso.wait_for(state="attached", timeout=5000)
            self.input_endoso.click(force=True)
            self.page.keyboard.press("Control+A")
            self.page.keyboard.press("Backspace")
            self.input_endoso.fill("1")
            print("Inciso llenado correctamente.")
        except Exception as e:
            print(f"⚠️ Nota: No se pudo interactuar con Inciso, continuando... Error: {e}")

        print("Configurando Oficina 80E...")
        self.select_oficina.click()
        self.select_oficina.fill("80E")
        self.page.wait_for_timeout(1500) 
        self.opcion_oficina.wait_for(state="visible", timeout=5000)
        self.opcion_oficina.click()

        print("Seleccionando Producto...")
        self.dropdown_producto.click()
        self.page.wait_for_timeout(800)
        self.opcion_a000.wait_for(state="visible", timeout=5000)
        self.opcion_a000.click()

        print("Buscando póliza...")
        self.btn_buscar_especifico.wait_for(state="visible")
        self.btn_buscar_especifico.click()

        print("Esperando resultados en la tabla...")
        try:
            self.btn_seleccionar_tabla.wait_for(state="visible", timeout=12000)
            self.btn_seleccionar_tabla.click()
            
            self.page.wait_for_timeout(1000)
            self.input_nombre_modal.fill("RAUL")
            self.input_paterno_modal.fill("TEST")
            self.input_materno_modal.fill("TEST")

            if self.inputs_telefono_modal.count() >= 2:
                self.inputs_telefono_modal.nth(0).fill("5555555555")
                self.inputs_telefono_modal.nth(1).fill("5555555555")
            
            print("Finalizando selección y cerrando modal...")
            self.btn_seleccionar_aperturar.scroll_into_view_if_needed()
            self.btn_seleccionar_aperturar.click()
            
            self.btn_aceptar_modal_final.wait_for(state="visible", timeout=5000)
            self.btn_aceptar_modal_final.click()
            
        except Exception as e:
            print(f"❌ Error en la fase final del modal: {e}")
            self.page.screenshot(path="error_modal_avanzado.png")
            raise e
        
        self.page.wait_for_timeout(2000)
        print("✅ Póliza avanzada completada.")

    def datos_asegurado(self):
        print("Llenando datos del conductor en el formulario principal...")
        self.page.locator("text=Datos del conductor").first.scroll_into_view_if_needed()
        
        def llenar(campo, valor):
            xpath = f"//*[contains(text(), 'Datos del conductor')]/following::input[@data-placeholder='{campo}']"
            loc = self.page.locator(xpath).first
            
            loc.fill(valor)
            loc.press("Tab")
            
            if loc.input_value() != valor:
                print(f"⚠️ Reintentando llenado de '{campo}'...")
                self.page.wait_for_timeout(500)
                loc.click()
                loc.fill(valor)
                loc.press("Tab")

        print("Llenando correo del reportante...")
        input_correo = self.page.locator("input[data-placeholder='Email']").first
        input_correo.scroll_into_view_if_needed()
        input_correo.click()
        input_correo.fill("josemanuel@gmail.com")
        input_correo.press("Tab")
        
        if input_correo.input_value() != "josemanuel@gmail.com":
            self.page.wait_for_timeout(500)
            input_correo.fill("josemanuel@gmail.com")

        llenar("Nombre(s)", "ANA")
        llenar("Apellido Paterno", "ANA")
        llenar("Apellido Materno", "NANA")

        print("Seleccionando género...")
        self.select_genero.scroll_into_view_if_needed()
        self.select_genero.click()
        self.page.wait_for_timeout(500) 
        self.opcion_genero.click()

    def llenar_siniestro_y_ubicacion(self, direccion_mapa, cp_buscado, colonia_buscada):
        print("Llenando info siniestro y ubicación...")
        self.page.wait_for_timeout(1000) 
        
        print("Llenando Descripción Vehículo y Placas...")
        self.input_desc_vehiculo.scroll_into_view_if_needed()
        self.input_desc_vehiculo.click(force=True)
        self.input_desc_vehiculo.fill("Auto bonito")
        
        self.input_placas.click(force=True)
        self.input_placas.fill("ZZ11111")

        print("Seleccionando fecha en calendario...")
        self.btn_calendario_icon.scroll_into_view_if_needed()
        self.btn_calendario_icon.click(force=True)
        self.page.wait_for_timeout(500)
        self.btn_dia_hoy.click(force=True)
        self.page.keyboard.press("Escape")

        print("Llenando Qué ocurrió...")
        self.input_que_ocurrio.scroll_into_view_if_needed()
        self.input_que_ocurrio.click(force=True)
        self.input_que_ocurrio.fill("Chocó")

        print("Seleccionando Causa...")
        self.select_causa.scroll_into_view_if_needed()
        self.select_causa.click(force=True)
        self.page.wait_for_timeout(500)
        self.opcion_colision.click()

        print("Seleccionando Relación...")
        self.select_relacion.scroll_into_view_if_needed()
        self.select_relacion.click(force=True)
        self.page.wait_for_timeout(500) 
        self.opcion_relacion.click()
        
        print("Seleccionando Color...")
        self.select_color.scroll_into_view_if_needed()
        self.select_color.click(force=True)
        self.page.wait_for_timeout(500)
        self.opcion_color.click()

        print("Seleccionando Tipo de Siniestro...")
        self.select_tipo_siniestro.scroll_into_view_if_needed()
        self.select_tipo_siniestro.click(force=True)
        self.page.wait_for_timeout(500)
        self.opcion_tipo_siniestro.click()

        # --- BLOQUE 2: Ubicación ---
        selects_ubicacion = [
            (self.select_vialidad, self.opcion_avenida),
            (self.select_tipo_ubicacion, self.opcion_tramo),
            (self.select_tipo_carretera, self.opcion_cuota)
        ]
        
        for selector, opcion in selects_ubicacion:
            selector.scroll_into_view_if_needed() 
            selector.click(force=True)
            self.page.wait_for_timeout(300)
            opcion.click()

        self.input_nom_carretera.fill("MEXICO-PUEBLA")
        self.input_km.fill("123")

        # --- BLOQUE 3: Mapa ---
        self._buscar_en_mapa(direccion_mapa)

        # --- LÓGICA INTELIGENTE DE COLONIA Y C.P. (CUIDADOSA) ---
        print("Esperando a que el mapa termine de cargar los datos postales...")
        self.page.wait_for_timeout(3000) 
        
        try:
            # --- 1. LEER LO QUE PUSO EL MAPA ---
            select_cp = self.page.locator("mat-form-field").filter(has_text="C.P.").locator("mat-select").first
            select_colonia = self.page.locator("mat-form-field").filter(has_text="Colonia").locator("mat-select").first
            
            try:
                valor_cp_actual = select_cp.locator(".mat-select-value-text").inner_text(timeout=1000).strip()
            except:
                valor_cp_actual = ""
                
            try:
                valor_colonia_actual = select_colonia.locator(".mat-select-value-text").inner_text(timeout=1000).strip()
            except:
                valor_colonia_actual = ""

            print(f"El mapa puso -> C.P.: '{valor_cp_actual}' | Colonia: '{valor_colonia_actual}'")

            # --- 2. VALIDAR Y CORREGIR C.P. SOLO SI ES NECESARIO ---
            if cp_buscado and cp_buscado not in valor_cp_actual:
                print(f"⚠️ El C.P. actual no es {cp_buscado}. Intentando corregir...")
                select_cp.scroll_into_view_if_needed()
                select_cp.click(force=True)
                self.page.wait_for_timeout(1000)
                
                opcion_cp = self.page.locator("mat-option", has_text=cp_buscado).first
                if opcion_cp.is_visible():
                    opcion_cp.click()
                    print(f"✅ C.P. corregido a '{cp_buscado}'.")
                    self.page.wait_for_timeout(1500) # Pausa para que carguen las colonias
                else:
                    print(f"❌ No se encontró el C.P. '{cp_buscado}' en la lista. Presionando Escape para no dañar nada.")
                    self.page.keyboard.press("Escape")
            else:
                print("✅ El C.P. ya es correcto. No se tocará.")

            # --- 3. VALIDAR Y CORREGIR COLONIA SOLO SI ES NECESARIO ---
            try:
                valor_colonia_actual = select_colonia.locator(".mat-select-value-text").inner_text(timeout=1000).strip()
            except:
                pass

            if colonia_buscada and colonia_buscada.upper() not in valor_colonia_actual.upper():
                print(f"⚠️ La Colonia actual no es {colonia_buscada}. Intentando corregir...")
                select_colonia.scroll_into_view_if_needed()
                select_colonia.click(force=True)
                self.page.wait_for_timeout(1000)
                
                opcion_colonia = self.page.locator("mat-option").filter(has_text=colonia_buscada).first
                if opcion_colonia.is_visible():
                    opcion_colonia.click()
                    print(f"✅ Colonia corregida a '{colonia_buscada}'.")
                else:
                    print(f"❌ No se encontró '{colonia_buscada}' en la lista. Presionando Escape.")
                    self.page.keyboard.press("Escape")
            else:
                print("✅ La Colonia ya es correcta. No se tocará.")

        except Exception as e:
            print(f"⚠️ Error en la validación de Colonia/C.P.: {e}")

    def _buscar_en_mapa(self, direccion):
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

        self.page.wait_for_timeout(2000)

    def enviar_apertura(self):
        print("Finalizando apertura...")
        self.btn_aperturar.scroll_into_view_if_needed()
        print("Esperando a que la página procese la ubicación...")
        self.page.wait_for_timeout(3000) 
        
        print(">>> Haciendo CLICK en Aperturar...")
        self.btn_aperturar.click()
        
        # --- NUEVO: ESPERA FORZADA DESPUÉS DEL CLIC ---
        print("⏳ Esperando 5 segundos para que el sistema piense la apertura...")
        self.page.wait_for_timeout(5000) # Se queda quieto viendo qué pasa
        
        try:
            # Aumentamos el timeout a 15000 (15 segundos) por si el internet está lento
            print("Buscando el botón de éxito...")
            self.btn_buscar_final.wait_for(state="visible", timeout=15000)
            print("✅ ¡Apertura exitosa! Botón Buscar detectado.")
            self.btn_buscar_final.click()
        except:
            print("⚠️ ADVERTENCIA: No se detectó avance. Buscando errores en el formulario...")
            errores = self.page.locator("mat-error").all_inner_texts()
            if errores:
                print(f"❌ ERRORES ENCONTRADOS EN EL FORMULARIO: {errores}")
            else:
                print("❌ No veo errores de texto explícitos, pero el formulario no avanza.")

            # Toma la foto antes de rendirse
            nombre_foto = f"error_apertura_{self.page.context.pages.index(self.page)}.png"
            self.page.screenshot(path=nombre_foto, full_page=True)
            print(f"📸 Captura de pantalla guardada como: {nombre_foto} (Revisa la carpeta del proyecto)")
            
            # Otro respiro antes de arrojar el error y recargar
            self.page.wait_for_timeout(2000)
            raise Exception("El formulario no avanzó. Revisa la captura de pantalla.")