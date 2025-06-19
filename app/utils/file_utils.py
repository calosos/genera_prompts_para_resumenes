"""
app/utils/file_utils.py

Este módulo proporciona utilidades para la lectura y validación de archivos que
contienen listas de URLs, utilizadas principalmente para automatizar procesos
de extracción y resumen de contenido en Coursera.
Contiene la clase `FileUtils`, que implementa el patrón Utility, centralizando
operaciones comunesrelacionadas con archivos de texto plano en el proyecto.

Funciones clave:
- Lectura de URLs desde un archivo (`urls_resumen.txt` por defecto).
- Limpieza de líneas vacías y comentarios.
- Confirmación interactiva con el usuario antes de procesar la lista de URLs.

Uso típico:
    >>> fu = FileUtils()
    >>> urls = fu.leer_y_confirmar_urls()
    >>> if urls:
    ...     procesar_urls(urls)

Este módulo es parte del sistema modular de automatización de cursos en
Coursera.
"""

import os


class FileUtils:
    """
    Utilidades para manejo de archivos.
    Implementa el patrón Utility.
    """

    def leer_y_confirmar_urls(self, ruta="urls_resumen.txt"):
        """Lee URLs de un archivo y pide confirmación al usuario."""
        if not os.path.exists(ruta):
            print(f"❌ No se encontró el archivo: {ruta}")
            return None

        print(f"\n📄 Contenido de {ruta}:")
        with open(ruta, encoding="utf-8") as f:
            urls = [line.strip() for line in f if line.strip() and
                    not line.strip().startswith("#")]

        for i, url in enumerate(urls, 1):
            print(f"{i}. {url}")
        mensaje = "\n¿El contenido es correcto? (s/n): "
        confirmacion = input(mensaje).strip().lower()
        if confirmacion == "s":
            return urls
        print("❌ Operación cancelada por el usuario.")
        return None
