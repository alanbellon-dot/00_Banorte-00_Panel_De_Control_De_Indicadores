import time
import re  # <-- IMPORTANTE: Librería para buscar el C.P. con expresiones regulares
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from pages.apertura_page import AperturaPage
from pages.asignacion_page import AsignacionPage

def run():
    print("=== BOT DE AUTOMATIZACIÓN (Versión Playwright) ===")
    
    # Inputs de usuario
    try:
        cantidad = int(input("Ingresa las veces a ejecutar: "))
    except ValueError:
        cantidad = 1

    resp_poliza = input("¿Deseas hacer busqueda de poliza avanzada? (si/no): ").lower().strip()
    usar_avanzada = (resp_poliza == 'si' or resp_poliza == 's')

    # --- LÓGICA AUTOMÁTICA DE DIRECCIÓN ---
    print("\nEjemplo de dirección: Calle Jorge Negrete 63, Nueva Santa Rosa, 56310 Atenco, Estado de México")
    direccion_input = input("Ingresa la dirección completa (o da Enter para usar una por defecto): ").strip()
    
    if not direccion_input:
        # Dirección por defecto si el usuario solo da Enter
        direccion_input = "Av. Insurgentes Sur 701, Nápoles, Benito Juárez, 03810 Ciudad de México, CDMX"

    # Variables que vamos a extraer
    cp_input = ""
    colonia_input = ""
    municipio_input = ""

    # 1. Extraer el C.P. buscando 5 dígitos seguidos usando Regex
    match_cp = re.search(r'\b(\d{5})\b', direccion_input)
    if match_cp:
        cp_input = match_cp.group(1)

    # 2. Separar la dirección por comas para sacar Colonia y Municipio
    partes_direccion = [p.strip() for p in direccion_input.split(',')]
    
    if len(partes_direccion) >= 3:
        # La colonia casi siempre es la segunda parte después de la calle
        colonia_input = partes_direccion[1].upper()
        
        # El Municipio suele ser la tercera parte (a veces tiene el CP pegado)
        parte_tres = partes_direccion[2]
        if cp_input and cp_input in parte_tres:
            # Si el municipio y el CP están juntos (ej. "56310 Atenco"), quitamos los números
            municipio_input = parte_tres.replace(cp_input, "").strip().upper()
        else:
            # Si están separados (ej. "Benito Juárez")
            municipio_input = parte_tres.strip().upper()

    print("\n--- DATOS EXTRAÍDOS AUTOMÁTICAMENTE ---")
    print(f"📍 Dirección a buscar : {direccion_input}")
    print(f"🏙️ Municipio extraído : {municipio_input}")
    print(f"🏘️ Colonia extraída   : {colonia_input}")
    print(f"📮 C.P. extraído      : {cp_input}")
    print("---------------------------------------\n")
        
    ajustador_input = input("Ingresa el nombre o ID del ajustador (o da Enter para elegir uno al azar): ").strip()

    with sync_playwright() as p:
        # Lanzamos navegador (headless=False para ver la acción)
        print("\nLanzando navegador...")
        browser = p.chromium.launch(headless=False, args=["--start-maximized"])
        
        # Contexto maximizado (viewport None usa el tamaño de la ventana)
        context = browser.new_context(no_viewport=True)
        page = context.new_page()

        # Instanciamos los Page Objects
        login_p = LoginPage(page)
        apertura_p = AperturaPage(page)
        asignacion_p = AsignacionPage(page)

        # --- LOGIN (Solo una vez al inicio) ---
        try:
            print("\n--- Iniciando Sesión ---")
            login_p.navigate()
            login_p.login("DEVBANORTE", "12345678")
            
            # Esperamos redirección
            print("Esperando redirección...")
            page.wait_for_url(lambda url: "/inicio" in url or "/panel-control" in url, timeout=30000)
            
            print("Login exitoso.")
        except Exception as e:
            print(f"❌ Error fatal en Login: {e}")
            return # Salimos si no hay login

        # --- BUCLE PRINCIPAL ---
        for i in range(cantidad):
            print(f"\n>>> ITERACIÓN {i + 1} de {cantidad} <<<")
            
            try:
                # 1. Navegación
                apertura_p.navegar_al_modulo()

                # 2. Llenado
                apertura_p.llenar_reportante()
                apertura_p.gestionar_poliza(usar_logica_avanzada=usar_avanzada)
                apertura_p.datos_asegurado()
                
                # --- AHORA ENVÍA LOS 4 DATOS CORRECTAMENTE ---
                apertura_p.llenar_siniestro_y_ubicacion(
                    direccion_mapa=direccion_input, 
                    municipio_buscado=municipio_input, 
                    colonia_buscada=colonia_input,
                    cp_buscado=cp_input
                )

                # 3. Apertura
                apertura_p.enviar_apertura()

                # 4. Asignación (Si la apertura fue exitosa)
                asignacion_p.verificar_y_asignar(ajustador_manual=ajustador_input)
                
                print(f"✅ Iteración {i + 1} finalizada con éxito.")
                
                # Pausa breve entre iteraciones
                time.sleep(2)

            except Exception as e:
                print(f"🔥 Error en iteración {i + 1}: {e}")
                
                # Recuperación: Intentamos recargar la página para la siguiente vuelta
                print("Intentando recuperar refrescando página...")
                try:
                    page.reload()
                    time.sleep(3)
                except:
                    pass

        print("\n=== PROCESO TERMINADO ===")
        # Dejamos abierto 5 segs para ver el final y cerramos
        time.sleep(5)
        browser.close()

if __name__ == "__main__":
    run()