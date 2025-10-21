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
    
    # Determinar los parámetros según el sistema operativo
    if os.name == 'nt':  # Windows
        add_data_param = "--add-data=icon.ico;."
    else:  # Linux/Mac
        add_data_param = "--add-data=icon.ico:."
    
    # Comando para compilar el ejecutable
    # Usamos --onefile para crear un solo archivo ejecutable
    # Usamos --windowed para que no se abra la consola (apropiado para GUI)
    # Usamos --icon para especificar el icono
    # Usamos --name para especificar el nombre del ejecutable
    # Usamos --add-data para incluir el icono en el ejecutable
    cmd = [
        "pyinstaller",
        "--onefile",           # Crear un solo archivo ejecutable
        "--windowed",          # No abrir consola (apropiado para GUI)
        "--icon=icon.ico",     # Icono para el ejecutable
        "--name=GD_Downloader", # Nombre del ejecutable
        add_data_param,        # Incluir el icono en el ejecutable
        "main.py"              # Archivo de entrada
    ]
    
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