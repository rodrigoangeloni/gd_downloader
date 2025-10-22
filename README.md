# 📥 Google Drive Downloader

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

Una aplicación de escritorio minimalista para descargar archivos de Google Drive. Su propósito principal es ocultar el enlace de descarga, permitiendo distribuir un único ejecutable que garantiza que todos los usuarios obtengan exactamente el mismo archivo, sin revelar la fuente original.

 <!-- Reemplazar con una captura de pantalla real -->

---

## ✨ Características Principales

- 🖱️ **Descarga con un Clic:** Ejecuta la aplicación y la descarga comenzará automáticamente.
- 📊 **Interfaz Intuitiva:** Una barra de progreso visual te mantiene informado sobre el estado de la descarga.
- ⚙️ **Configuración Flexible:** El ID del archivo se gestiona externamente, permitiendo cambiar el enlace sin modificar el código.
- 📦 **Ejecutable Portátil:** Compila la aplicación en un único archivo `.exe` para una distribución sencilla en Windows.
- 🔔 **Notificaciones Claras:** Mensajes de éxito o error te informan sobre el resultado de la operación.

---

## 🚀 Cómo Empezar

### Prerrequisitos

- Python 3.11 o superior.
- Las dependencias listadas en `requirements.txt`.

### Ejecutar desde el Código Fuente

1.  **Clona el repositorio:**
    ```bash
    git clone https://github.com/rodrigoangeloni/gd_downloader.git
    cd gd_downloader
    ```

2.  **Crea y activa un entorno virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

3.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configura tus variables de entorno:**
    Copia el archivo de ejemplo `.env.example` y renómbralo a `.env`.
    ```bash
    cp .env.example .env
    ```
    Luego, abre el archivo `.env` y reemplaza `REEMPLAZA_CON_EL_ID_DE_TU_ARCHIVO` con el ID real de tu archivo de Google Drive.

5.  **Ejecuta la aplicación:**
    ```bash
    python main.py
    ```

---

## 📦 Compilación

Para crear un ejecutable `.exe` para Windows, simplemente ejecuta el script de compilación:

```bash
python build_exe.py
```

El archivo `GD_Downloader.exe` se creará en la carpeta `dist`.

---

## 🛠️ Estructura del Proyecto

```
gd_downloader/
├── .env.example      # Archivo de ejemplo para variables de entorno
├── .gitignore        # Archivos ignorados por Git
├── build_exe.py      # Script de compilación para PyInstaller
├── CHANGELOG.md      # Registro de cambios del proyecto
├── crear_venv.py     # Script para crear entorno virtual
├── icon.ico          # Icono de la aplicación
├── main.py           # Código fuente principal de la aplicación
---

## 🔧 Detalles Técnicos

### Integración de la Barra de Progreso

Uno de los principales desafíos técnicos de este proyecto fue mostrar el progreso de la descarga de `gdown` (una herramienta de línea de comandos) en una interfaz gráfica de Tkinter.

La solución implementada consiste en:

1.  **Utilizar `gdown` como Biblioteca:** En lugar de llamarlo como un subproceso (lo que causaba bucles de ejecución en el `.exe`), se importa y utiliza directamente.
2.  **Redirección de `stderr`:** `gdown` utiliza la biblioteca `tqdm` para renderizar su barra de progreso en la consola, escribiendo en el flujo de error estándar (`stderr`).
3.  **Captura y Análisis:** Se crea una clase personalizada que simula ser `stderr`. Esta clase intercepta en tiempo real lo que `tqdm` escribe, lo analiza con una expresión regular para extraer el porcentaje de progreso y actualiza la barra de progreso de Tkinter de forma segura entre hilos usando `root.after()`.

Esta arquitectura evita problemas de concurrencia y permite una integración limpia y robusta entre la lógica de backend y la interfaz de usuario.
├── README.md         # Este archivo
└── requirements.txt  # Dependencias de Python
```

---

## 📜 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.