# Gestor de Tareas — Aplicación de Escritorio (ejemplo académico)

Aplicación de escritorio simple hecha en **Python 3 + Tkinter**, usada como
ejemplo de funcionamiento en el reporte "Aplicación de Escritorio"
(Subproducto No. 3).

## Requisitos
- Python 3.8 o superior (Tkinter viene incluido en la instalación estándar
  de Python en Windows y macOS; en Linux instala `sudo apt install python3-tk`
  si no lo tienes).

## Cómo ejecutarla
```bash
python3 gestor_tareas.py
```
Se abrirá una ventana nativa. Los datos se guardan automáticamente en un
archivo `tareas.json` en la misma carpeta.

## Características
- CRUD completo de tareas (crear, editar, completar/pendiente, eliminar)
- Persistencia local en archivo JSON (sin servidor, sin internet)
- Barra de menú (Archivo, Ayuda) y atajos de teclado (Ctrl+S, Enter)
- Cuadros de diálogo nativos (confirmación, "Acerca de")

## Cómo obtener una URL pública para el subproducto (b)
Una app de escritorio no "vive" en una URL como una app web. Si tu entrega
pide una URL, la forma normal de resolverlo es subir este código a un
repositorio y compartir ese enlace:

1. Crea una cuenta en https://github.com si no tienes una.
2. Crea un repositorio nuevo (público), por ejemplo `gestor-tareas-escritorio`.
3. Sube estos dos archivos (`gestor_tareas.py` y este `README.md`) — puedes
   arrastrarlos desde la interfaz web de GitHub ("Add file > Upload files").
4. Copia la URL del repositorio (ej. `https://github.com/tu-usuario/gestor-tareas-escritorio`)
   y esa es la URL que anexas en el subproducto.

(Alternativa si tu materia pide únicamente el .exe: se puede generar con
`pip install pyinstaller` y luego `pyinstaller --onefile gestor_tareas.py`,
pero eso requiere hacerlo en tu propia computadora Windows/Mac, ya que aquí
no se puede compilar un .exe nativo de Windows.)
