import tkinter as tk
from tkinter import ttk, messagebox
import gdown
import threading
import os
import sys
import multiprocessing
import re
import io
import contextlib
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

class GoogleDriveDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("Google Drive Downloader")
        self.root.geometry("400x120")
        self.root.resizable(False, False)
        # Centrar la ventana en la pantalla
        self.center_window()
        # Configurar el contenido de la interfaz
        self.setup_ui()
        # ID del archivo de Google Drive (desde .env)
        self.file_id = os.getenv("FILE_ID")
        # Nombre del archivo a descargar (se obtiene automáticamente)
        # Flag para evitar descargas múltiples
        self.download_started = False

    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        # Configurar el peso de las columnas y filas
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        # Etiqueta de estado
        self.status_label = ttk.Label(main_frame, text="Preparando descarga...")
        self.status_label.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="w")
        # Barra de progreso
        self.progress = ttk.Progressbar(main_frame, mode='determinate')
        self.progress.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))
    # No se crea el botón de inicio, la descarga es automática
        # Configurar estilo para la barra de progreso
        style = ttk.Style()
        style.configure("green.Horizontal.TProgressbar", foreground='green', background='green')
        self.progress.configure(style="green.Horizontal.TProgressbar")

    def start_download_thread(self):
        """Inicia el proceso de descarga en un hilo separado, solo una vez"""
        if self.download_started:
            return
        self.download_started = True
        self.status_label.config(text="Descargando archivo...")
        download_thread = threading.Thread(target=self.download_file)
        download_thread.daemon = True
        download_thread.start()

    def download_file(self):
        """Descarga el archivo de Google Drive usando gdown como biblioteca y captura el progreso."""

        class TqdmRedirect(io.TextIOBase):
            def __init__(self, app):
                self.app = app
                self.last_percent = -1

            def write(self, s):
                # tqdm, por defecto, escribe el progreso en stderr. Lo capturamos aquí.
                # Ejemplo: "  9%|▉         | 50.1M/555M [00:03<00:33, 15.2MB/s]"
                match = re.search(r"(\d+)%", s)
                if match:
                    percent = int(match.group(1))
                    # Solo actualizar si el porcentaje ha cambiado para evitar sobrecargar la GUI
                    if percent != self.last_percent:
                        self.last_percent = percent
                        # Usar root.after para actualizar la GUI desde el hilo de descarga de forma segura
                        self.app.root.after(0, self.app.update_progress, percent)
                return len(s)

        def update_progress(percent):
            """Función para actualizar la barra de progreso y la etiqueta de estado."""
            self.progress.configure(value=percent)
            self.status_label.config(text=f"Descargando... {percent}%")

        self.update_progress = update_progress

        try:
            url = f"https://drive.google.com/uc?id={self.file_id}"
            self.root.after(0, lambda: self.status_label.config(text="Iniciando descarga..."))

            output_filename = None
            # Redirigir stderr para capturar la salida de la barra de progreso de tqdm
            with contextlib.redirect_stderr(TqdmRedirect(self)):
                # quiet=False es necesario para que gdown/tqdm impriman la barra de progreso
                output_filename = gdown.download(url=url, quiet=False, fuzzy=True)

            if output_filename and os.path.exists(output_filename):
                size = os.path.getsize(output_filename)
                self.root.after(0, lambda: self.status_label.config(text=f"Descargado: {output_filename} ({round(size/1024/1024,2)} MB)"))
                self.root.after(0, lambda: self.progress.configure(value=100))
                self.root.after(0, self.show_success_message)
            else:
                self.root.after(0, lambda: self.show_error_message("El archivo no se descargó o no se encontró."))
        except Exception as e:
            error_msg = str(e)
            if "404" in error_msg or "not found" in error_msg.lower() or "not accessible" in error_msg.lower():
                self.root.after(0, lambda: self.show_error_message("Actualice el gb_download.exe que tendrá el nuevo link de Google Drive"))
            elif "403" in error_msg:
                self.root.after(0, lambda: self.show_error_message("Acceso denegado. El archivo puede no estar disponible para descarga."))
            else:
                self.root.after(0, lambda: self.show_error_message(f"Error durante la descarga: {error_msg}"))

    def show_success_message(self):
        """Muestra mensaje de descarga completada y cierra la aplicación"""
        messagebox.showinfo("Éxito", "¡Descarga completada con éxito!")
        self.root.destroy()

    def show_error_message(self, message):
        """Muestra mensaje de error y cierra la aplicación"""
        messagebox.showerror("Error", message)
        self.root.destroy()

    def start_auto_download(self):
        """Inicia automáticamente la descarga cuando se abre la aplicación"""
        self.root.after(100, self.start_download_thread)

def main():
    # Crear ventana principal
    root = tk.Tk()
    # Crear instancia de la aplicación
    app = GoogleDriveDownloader(root)
    # Iniciar descarga automática
    app.start_auto_download()
    # Iniciar el bucle de la interfaz
    root.mainloop()

if __name__ == "__main__":
    # Necesario para que PyInstaller funcione correctamente en Windows
    multiprocessing.freeze_support()
    main()