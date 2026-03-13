import random
import time
from playwright.sync_api import Page

class AsignacionPage:
    def __init__(self, page: Page):
        self.page = page

        # --- SELECTORES ---
        # Usamos .first para asegurar que tomamos el de la primera fila
        self.lbl_estatus = page.locator("td.mat-column-estatus").first
        self.btn_menu_opciones = page.locator("mat-icon:has-text('more_vert')").first
        
        # Selectores del flujo de asignación
        self.btn_buscar_persona_icon = page.locator("mat-icon:has-text('person_search')")
        self.btn_aceptar = page.locator("button.btn-aceptar")
        
        # Lista de proveedores (usaremos .all() dinámicamente)
        self.selector_proveedores = "span.id-proveedor"
        
        self.btn_seleccionar_ajustador = page.locator("button", has_text="Seleccionar ajustador")
        self.btn_asignar_final = page.locator("button", has_text="Asignar")

    def verificar_y_asignar(self, ajustador_manual=""): # <-- AQUÍ SE DECLARA LA VARIABLE
        print("--- Verificando Estatus del Siniestro ---")
        
        # Esperamos a que la tabla cargue el estatus
        try:
            self.lbl_estatus.wait_for(state="visible", timeout=15000)
            estatus_texto = self.lbl_estatus.inner_text().strip()
            print(f"Estatus encontrado: '{estatus_texto}'")

            if "Registrada" in estatus_texto:
                print(">>> Estatus OK. Procediendo a asignar...")
                self._realizar_asignacion_manual(ajustador_manual) # <-- AQUÍ SE USA
            elif "Asignada" in estatus_texto:
                print(">>> El siniestro YA está asignado. Saltando paso.")
            else:
                print(f"⚠️ Estatus desconocido '{estatus_texto}'. No se asignará.")

        except Exception as e:
            print(f"Error leyendo la tabla (quizás no cargó a tiempo): {e}")

    # Agregamos la variable en la definición
    def _realizar_asignacion_manual(self, ajustador_manual=""):
        # 1. Abrir menú de 3 puntos
        self.btn_menu_opciones.click()

        # 2. Click en lupa (Buscar persona)
        self.page.wait_for_timeout(500)
        self.btn_buscar_persona_icon.click()

        # 3. Confirmar modal inicial
        self.btn_aceptar.click()

        # 4. Click otra vez en buscar
        self.page.wait_for_timeout(1000)
        self.btn_buscar_persona_icon.click()

        # 5. Lógica de Paginación y Selección
        print("Buscando proveedores disponibles...")
        elegido = None
        
        # Selector del botón "Siguiente" (busca un botón que por dentro tenga el ícono 'navigate_next')
        btn_siguiente = self.page.locator("button:has(mat-icon:has-text('navigate_next'))")

        # 5.1 Búsqueda manual a través de las páginas
        if ajustador_manual:
            print(f"Buscando ajustador específico que contenga: '{ajustador_manual}'")
            
            while True:
                # Esperamos a que los resultados carguen
                self.page.wait_for_selector(self.selector_proveedores, timeout=10000)
                opciones = self.page.locator(self.selector_proveedores).all()
                
                # Buscamos en la página actual
                for op in opciones:
                    texto_opcion = op.inner_text()
                    if ajustador_manual.lower() in texto_opcion.lower():
                        elegido = op
                        print(f"¡Ajustador encontrado!: {texto_opcion}")
                        break
                
                if elegido:
                    break # Lo encontramos, salimos del ciclo while
                
                # Si no lo encontró, checamos si podemos ir a la siguiente página
                if btn_siguiente.is_visible() and not btn_siguiente.is_disabled():
                    print("No está en esta página. Dando clic a la flecha siguiente...")
                    btn_siguiente.click()
                    self.page.wait_for_timeout(1000) # Pausa para que cambien los nombres
                else:
                    print(f"⚠️ Se llegó a la última página y no se encontró a '{ajustador_manual}'.")
                    break # Rompemos el ciclo porque ya no hay a dónde avanzar

        # 5.2 Si dio Enter (vacío) o si escaneó todas las páginas y no lo encontró
        if not elegido:
            print("Activando selección al azar...")
            self.page.wait_for_selector(self.selector_proveedores, timeout=10000)
            opciones = self.page.locator(self.selector_proveedores).all()
            
            if opciones:
                elegido = random.choice(opciones)
                texto_id = elegido.inner_text()
                print(f"Seleccionando proveedor al azar ID: {texto_id}")
            else:
                print("⚠️ No se encontraron proveedores en la lista de ninguna manera.")
                return # Si la lista está totalmente vacía, abortamos
        
        # 6. Finalizar la asignación
        elegido.click()
        
        self.page.wait_for_timeout(500)
        self.btn_seleccionar_ajustador.click()
        
        self.page.wait_for_timeout(500)
        self.btn_asignar_final.click()
        print("¡Asignación completada!")