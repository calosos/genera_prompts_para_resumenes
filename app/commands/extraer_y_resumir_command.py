# app/commands/extraer_y_resumir_command.py

"""
Archivo: app/commands/extraer_y_resumir_command.py

Define el comando para extraer y resumir el contenido de una lección
de Coursera.
Utiliza ContenidoService y ResumenService.
Implementa el patrón Command.
"""

from app.commands.base_command import BaseCommand
from app.services.contenido_service import ContenidoService
from app.services.resumen_service import ResumenService


class ExtraerYResumirCommand(BaseCommand):
    """
    Comando para extraer y resumir contenido de una lección.
    """

    def __init__(self, driver_service):
        super().__init__(driver_service)
        self.contenido_service = ContenidoService()
        self.resumen_service = ResumenService()

    def ejecutar(self):
        """
        Ejecuta el proceso completo de:
        - Preparar el driver con cookies
        - Extraer el contenido completo de una lección
        - Generar resumen con el agente IA
        - Guardar el resumen en archivo markdown
        """
        driver, url = self.driver_service.preparar_driver_y_url()
        if not driver:
            return

        try:
            self.resumen_service.procesar_y_guardar_resumen(driver, url)
        finally:
            driver.quit()
