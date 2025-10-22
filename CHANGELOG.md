# Changelog

## [1.1.0] - 2025-10-22

### Fixed
- **Error de Ejecución Múltiple:** Se solucionó un problema crítico que causaba que el ejecutable se lanzara a sí mismo en un bucle infinito en Windows. La causa raíz (el uso de `subprocess` para invocar `gdown`) fue eliminada.
- **Error de Argumento en `gdown`:** Se corrigió un error fatal que ocurría al intentar pasar un `callback` de progreso no soportado a la función `gdown.download()`.

### Changed
- **Lógica de Descarga Refactorizada:** El método de descarga fue completamente reescrito. Ahora se utiliza `gdown` como una biblioteca nativa y se captura la salida de progreso de `tqdm` (su dependencia) redirigiendo `stderr`. Esto proporciona una actualización de la barra de progreso robusta y estable sin crear procesos secundarios.

## [1.0.0] - 2025-10-22

### Added
- **Interfaz Gráfica de Usuario (GUI):** Ventana de descarga con barra de progreso.
- **Descarga Automática:** El proceso de descarga se inicia al abrir la aplicación.
- **Feedback Visual:** Mensajes de éxito o error al finalizar la descarga.
- **Compilación a .EXE:** Script `build_exe.py` para generar un ejecutable de Windows.

### Changed
- **Configuración Externalizada:** El ID del archivo de Google Drive ahora se gestiona a través de un archivo `.env` para mayor seguridad y flexibilidad.
- **Código Refactorizado:** Mejoras en la estructura y legibilidad del código fuente en `main.py`.
- **Dependencias Actualizadas:** Se añadió `python-dotenv` para gestionar las variables de entorno.

### Security
- Se ha eliminado el ID de archivo hardcodeado del código fuente para prevenir exposición de datos sensibles.