#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para compilar el ejecutable del programa usando PyInstaller
"""
import subprocess
import sys
import os

def build_exe():
    """Compila el ejecutable del programa usando PyInstaller"""
    print("Compilando el ejecutable...")
    
    # Verificar si PyInstaller está instalado
    try:
        import PyInstaller
    except ImportError:
        print("PyInstaller no está instalado. Instalando...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Determinar los separadores de ruta según el sistema operativo
    if os.name == 'nt':  # Windows
        sep = ';'
    else:  # Linux/Mac
        sep = ':'
        
    # Archivos y carpetas a incluir en el ejecutable
    add_data_files = [
        f"icon.ico{sep}.",
        f".env{sep}."
    ]

    # Comando para compilar el ejecutable
    cmd = [
        "pyinstaller",
        "--onefile",                   # Crear un solo archivo ejecutable
        "--windowed",                  # No abrir consola (apropiado para GUI)
        "--icon=icon.ico",             # Icono para el ejecutable
        "--name=GD_Downloader",        # Nombre del ejecutable
        "--version-file=version.txt",  # Archivo con metadatos de versión
        "main.py"                      # Archivo de entrada
    ]

    # Añadir los archivos de datos al comando
    for file in add_data_files:
        cmd.extend(["--add-data", file])

    print(f"Ejecutando: {' '.join(cmd)}")
    
    try:
        subprocess.check_call(cmd)
        print("\nEjecutable compilado exitosamente en la carpeta 'dist'.")
        print("El archivo se llama 'GD_Downloader.exe' (en Windows) o 'GD_Downloader' (en Linux/Mac)")
    except subprocess.CalledProcessError as e:
        print(f"Error al compilar el ejecutable: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("Error: PyInstaller no se encontró. Asegúrate de tenerlo instalado.")
        sys.exit(1)

if __name__ == "__main__":
    build_exe()