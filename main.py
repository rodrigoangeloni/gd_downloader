import tkinter as tk
from tkinter import ttk, messagebox
import gdown
import threading
import os
import sys

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
        # ID del archivo de Google Drive (esto se enmascara para el usuario)
        self.file_id = "1rl-nO3nZ-8qAj-L7MRyGfL5ipsTuREeM"
        # Nombre del archivo a descargar (se obtiene automáticamente)
        self.filename = None
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

    def get_drive_metadata(self, file_id):
        """Obtiene nombre y tamaño del archivo desde Google Drive, manejando archivos grandes y ejecutables"""
        import requests
        import re
        url_download = f"https://drive.google.com/uc?export=download&id={file_id}"
        with requests.Session() as session:
            response = session.get(url_download, stream=True)
            filename = None
            # Intentar obtener el nombre del archivo desde la cabecera
            if 'Content-Disposition' in response.headers:
                cd = response.headers['Content-Disposition']
                fname = re.findall('filename="(.+?)"', cd)
                if fname:
                    filename = fname[0]
            size = int(response.headers.get('content-length', 0))
            # Si no se obtuvo el nombre, intentar con confirmación para archivos grandes
            if not filename or size == 0 or 'Set-Cookie' in response.headers or 'confirmation' in response.text:
                confirm_token = re.search(r'confirm=([0-9A-Za-z_]+)', response.text)
                if confirm_token:
                    token = confirm_token.group(1)
                    url_confirm = f"https://drive.google.com/uc?export=download&confirm={token}&id={file_id}"
                    response2 = session.get(url_confirm, stream=True)
                    if 'Content-Disposition' in response2.headers:
                        cd = response2.headers['Content-Disposition']
                        fname = re.findall('filename="(.+?)"', cd)
                        if fname:
                            filename = fname[0]
                    size = int(response2.headers.get('content-length', 0))
            # Fallback: si sigue sin nombre, usar el id y extensión genérica
            if not filename:
                # Intentar obtener la extensión desde la URL de redirección
                ext = '.bin'
                if response.url.endswith('.exe'):
                    ext = '.exe'
                filename = f"archivo_{file_id}{ext}"
            return filename, size

    def download_file(self):
        """Descarga el archivo de Google Drive usando gdown como subproceso y actualiza la barra de progreso en tiempo real"""
        import subprocess
        import os
        import sys
        import re
        try:
            url = f"https://drive.google.com/uc?id={self.file_id}"
            self.status_label.config(text="Descargando archivo...")
            # Ejecutar gdown como subproceso
            cmd = [sys.executable, '-m', 'gdown', url, '--fuzzy']
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, bufsize=1)
            filename = None
            size_mb = None
            if process.stdout:
                for line in iter(process.stdout.readline, ''):
                    # Buscar nombre del archivo
                    match_to = re.search(r'To: (.+)', line)
                    if match_to:
                        filename = match_to.group(1).strip()
                    # Buscar tamaño total
                    match_size = re.search(r'\|\s*([\d\.]+)M/([\d\.]+)M', line)
                    if match_size:
                        size_mb = float(match_size.group(2))
                    # Buscar porcentaje
                    match_percent = re.search(r'(\d+)%\|', line)
                    if match_percent:
                        percent = int(match_percent.group(1))
                        self.root.after(0, lambda p=percent: self.progress.configure(value=p))
                        if filename and size_mb:
                            self.root.after(0, lambda p=percent, f=filename, s=size_mb: self.status_label.config(text=f"Descargando: {f} ({p}%) de {round(s,2)} MB"))
            process.wait()
            # Verificar si se descargó correctamente
            if filename and os.path.exists(filename):
                size = os.path.getsize(filename)
                self.status_label.config(text=f"Descargado: {filename} ({round(size/1024/1024,2)} MB)")
                self.progress['value'] = 100
                self.root.after(0, self.show_success_message)
            else:
                self.root.after(0, lambda: self.show_error_message("El archivo no se descargó correctamente"))
        except Exception as e:
            error_msg = str(e)
            if "404" in error_msg or "not found" in error_msg.lower() or "not accessible" in error_msg.lower():
                self.root.after(0, lambda: self.show_error_message("Actualice el gb_download.exe que tendrá el nuevo link de Google Drive"))
            elif "403" in error_msg:
                self.root.after(0, lambda: self.show_error_message("Acceso denegado. El archivo puede no estar disponible para descarga."))
            else:
                self.root.after(0, lambda: self.show_error_message(f"Error durante la descarga: {error_msg}"))

    def show_success_message(self):
        """Muestra mensaje de descarga completada"""
        messagebox.showinfo("Éxito", "¡Descarga completada con éxito!")
        self.progress['value'] = 100
        self.status_label.config(text="Descarga completada")
    # ...eliminado: no hay botón de inicio

    def show_error_message(self, message):
        """Muestra mensaje de error"""
        messagebox.showerror("Error", message)
        self.status_label.config(text="Error en la descarga")
    # ...eliminado: no hay botón de inicio

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
    main()