import time
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from pages.apertura_page import AperturaPage
from pages.asignacion_page import AsignacionPage

def run():
    print("=== BOT DE AUTOMATIZACIÓN (Versión Playwright) ===")
    
    # Inputs de usuario (igual que tu script original)
    try:
        cantidad = int(input("Ingresa las veces a ejecutar: "))
    except ValueError:
        cantidad = 1

    resp_poliza = input("¿Deseas hacer busqueda de poliza avanzada? (si/no): ").lower().strip()
    usar_avanzada = (resp_poliza == 'si' or resp_poliza == 's')

    direccion_input = input("Ingresa la dirección (o da Enter para usar Metrobús Nápoles): ").strip()
    
    # Si el usuario da Enter sin escribir nada, la variable se queda vacía, así que le asignamos la por defecto
    if not direccion_input:
        direccion_input = "Metrobús Nápoles, Avenida Insurgentes Sur, Colonia Nápoles, Mexico City, CDMX, Mexico"

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
            
            # --- CAMBIO AQUÍ ---
            # Antes esperábamos "**/panel-control", ahora aceptamos "**/inicio"
            # O incluso podemos usar una expresión regular para aceptar cualquiera de los dos.
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
                apertura_p.datos_asegurado()
                apertura_p.llenar_siniestro_y_ubicacion(direccion_mapa=direccion_input)

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