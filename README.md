# Google Drive Downloader

Una aplicación en Python que permite descargar archivos de Google Drive con una interfaz gráfica sencilla.

## Características

- Interfaz gráfica con barra de progreso verde
- Descarga automática al abrir el programa
- Mensajes claros de éxito o error
- Ocultamiento del link de descarga
- Ejecutable independiente (GD_Downloader.exe)

## Requisitos

- Python 3.14+
- Paquetes listados en `requirements.txt`

## Instalación

1. Clona este repositorio o descarga el archivo `GD_Downloader.exe`
2. Si deseas ejecutar desde código fuente:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

1. Ejecuta `GD_Downloader.exe`
2. La aplicación iniciará automáticamente la descarga
3. Verás una ventana con barra de progreso
4. Al completar, se mostrará un mensaje de éxito
5. Si hay problemas con el enlace, se mostrará un mensaje indicando que necesitas actualizar el ejecutable

## Funcionamiento

- El ID del archivo de Google Drive está codificado dentro del ejecutable
- El usuario no puede ver el enlace directamente
- El archivo se descarga en la misma carpeta donde se encuentra el ejecutable
- La barra de progreso muestra el avance en tiempo real, sincronizada con el porcentaje de descarga que aparece en la terminal.
- El porcentaje de descarga y la barra se actualizan automáticamente durante la descarga, permitiendo ver el progreso exacto en la interfaz gráfica.
- Al finalizar, se muestra el nombre real del archivo descargado y su tamaño.

## Errores Comunes

- **"Actualice el GD_Downloader.exe que tendrá el nuevo link de Google Drive"**: Esto indica que el enlace del archivo ha cambiado. Debes obtener una nueva versión del ejecutable.
- **"Acceso denegado"**: El archivo puede no estar disponible para descarga pública.

## Compilación

Para crear el ejecutable desde el código fuente:

```bash
python build_exe.py
```

El ejecutable se generará en la carpeta `dist`.

## Licencia

Este proyecto es de uso libre y gratuito.