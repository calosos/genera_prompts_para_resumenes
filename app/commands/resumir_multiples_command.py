# app/commands/resumir_multiples_command.py

"""
Archivo: app/commands/resumir_multiples_command.py

Define el comando para resumir múltiples lecciones de Coursera
leyendo las URLs desde un archivo externo.
Implementa el patrón Command.
"""

from app.commands.base_command import BaseCommand
from app.services.resumen_service import ResumenService
from app.utils.file_utils import FileUtils


class ResumirMultiplesCommand(BaseCommand):
    """
    Comando para resumir múltiples lecciones desde un archivo de URLs.
    """

    def __init__(self, driver_service):
        super().__init__(driver_service)
        self.resumen_service = ResumenService()
        self.file_utils = FileUtils()

    def ejecutar(self):
        """
        Ejecuta el proceso completo de:
        - Leer archivo de URLs (por defecto: urls_resumen.txt)
        - Confirmar con el usuario
        - Preparar driver con cookies
        - Procesar y guardar resúmenes uno a uno
        """
        urls = self.file_utils.leer_y_confirmar_urls()
        if not urls:
            return
        url_manual = "https://www.coursera.org"
        driver, _ = self.driver_service.preparar_driver_y_url(url_manual)
        if not driver:
            return

        try:
            self.resumen_service.procesar_multiples_resumenes(driver, urls)
        finally:
            driver.quit()
