#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para crear, activar un entorno virtual .venv e instalar las dependencias
"""
import subprocess
import sys
import os

def crear_venv():
    """Crea un entorno virtual llamado .venv, lo activa e instala las dependencias"""
    print("Creando entorno virtual .venv...")
    
    # Crear el entorno virtual
    subprocess.check_call([sys.executable, "-m", "venv", ".venv"])
    print("Entorno virtual creado exitosamente.")
    
    # Determinar los comandos según el sistema operativo
    if os.name == 'nt':  # Windows
        pip_cmd = [".venv\\Scripts\\pip.exe", "install", "-r", "requirements.txt"]
        activate_cmd = ".venv\\Scripts\\activate.bat"
    else:  # Linux/Mac
        pip_cmd = [".venv/bin/pip", "install", "-r", "requirements.txt"]
        activate_cmd = "source .venv/bin/activate"
    
    print("Instalando dependencias desde requirements.txt...")
    subprocess.check_call(pip_cmd)
    print("Dependencias instaladas exitosamente.")
    
    print("\nEntorno virtual .venv creado e instalado correctamente.")
    print(f"Para activarlo manualmente: {activate_cmd}")

if __name__ == "__main__":
    try:
        crear_venv()
    except subprocess.CalledProcessError as e:
        print(f"Error al crear el entorno virtual o instalar dependencias: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("Error: No se encontró el archivo requirements.txt")
        sys.exit(1)