# 🤖 Bot de Automatización: Apertura y Asignación de Siniestros

Este proyecto es una herramienta de automatización desarrollada en Python con Selenium. Su objetivo es realizar pruebas de estrés o tareas repetitivas en el portal de "Aseguradora Digital", automatizando el ciclo completo desde el inicio de sesión hasta la asignación de un siniestro.

## 📋 Requisitos Previos

Para ejecutar este código necesitas tener instalado:

1. **Python 3.x**: [Descargar Python](https://www.python.org/downloads/)
2. **Google Chrome**: El navegador debe estar actualizado a la última versión.
3. **Sistema Operativo Windows**: El script contiene comandos de limpieza (`taskkill`) optimizados para Windows.

## ⚙️ Instalación

Sigue estos pasos para preparar tu entorno de desarrollo:

1. **Clonar o descargar el proyecto** en tu computadora.
2. **Crear un entorno virtual** (Opcional pero recomendado para no mezclar librerías):
```bash
python -m venv venv

```


*Para activar el entorno:*
* Windows: `venv\Scripts\activate`
* Mac/Linux: `source venv/bin/activate`


3. **Instalar las dependencias**:
La única librería externa requerida es Selenium. Ejecuta el siguiente comando:
```bash
pip install selenium

```



## 🚀 Cómo Ejecutar el Código

1. Abre tu terminal o línea de comandos en la carpeta del proyecto.
2. Ejecuta el script principal:
```bash
python main.py

```


3. **Interacción**:
* Al iniciar, la consola te pedirá: `Ingresa las veces que quieres ejecutar el proceso:`.
* Escribe un número entero (ej. `5`) y presiona **Enter**.
* El navegador se abrirá automáticamente y comenzará el trabajo.



## 🧠 ¿Cómo funciona el código? (Rasgos Generales)

El script `main.py` actúa como un "robot" que simula ser un usuario humano. A continuación se describe su flujo lógico:

### 1. Inicialización y Limpieza

* Al arrancar, el bot intenta cerrar cualquier proceso de `chromedriver.exe` que haya quedado "colgado" de ejecuciones anteriores para liberar memoria.
* Configura el navegador Chrome para que no guarde contraseñas, oculte barras de automatización y evite bloqueos por detección de bots.

### 2. Inicio de Sesión (Login)

* Navega a la URL configurada.
* Ingresa las credenciales de prueba (`DEVBANORTE` / `12345678`) y accede al sistema.

### 3. Ciclo de Ejecución (Loop)

El bot repetirá los siguientes pasos la cantidad de veces que indicaste al inicio:

* **Navegación**: Va al menú principal y selecciona "Apertura Siniestro".
* **Llenado de Formularios**:
* **Datos Reportante**: Ingresa nombres predefinidos ("ANA TEST") y números de teléfono.
* **Limpieza de Póliza**: Borra los campos de póliza/inciso y marca la opción "Sin Póliza".
* **Detalles del Siniestro**: Selecciona la causa ("Colisión Automotriz"), tipo de inmueble, color del vehículo y selecciona la fecha actual en el calendario emergente.
* **Ubicación**: Configura la dirección en el mapa (Google Maps), define el tipo de carretera y zona.


* **Apertura**: Hace clic en el botón "Aperturar" y luego en "Buscar" para ver el registro creado.
* **Verificación y Asignación**:
* Lee la tabla de resultados. Si el estatus es **"Registrada"**, procede a asignar.
* Si el estatus es **"Asignada"**, omite el paso.
* Selecciona un ajustador/proveedor **al azar** de la lista disponible y confirma la asignación.



### 4. Cierre

Una vez completadas todas las iteraciones, el navegador se cierra automáticamente de forma segura.

---

### ⚠️ Notas Adicionales

* **Credenciales**: El usuario y contraseña están definidos como constantes al inicio del archivo `main.py`. Si cambian, debes actualizarlos allí.
* **Errores**: Si ocurre un error, el script lo mostrará en la consola y cerrará el navegador para evitar procesos zombies.