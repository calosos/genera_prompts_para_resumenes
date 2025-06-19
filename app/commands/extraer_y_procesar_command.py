# app/commands/extraer_y_procesar_command.py

"""
Archivo: app/commands/extraer_y_procesar_command.py

Define el comando para extraer y procesar contenido de una lección de Coursera.
Utiliza los servicios de ContenidoService y ProcesamientoService.
Implementa el patrón Command.
"""

from app.commands.base_command import BaseCommand
from app.services.contenido_service import ContenidoService
from app.services.procesamiento_service import ProcesamientoService


class ExtraerYProcesarCommand(BaseCommand):
    """
    Comando para extraer contenido completo y procesarlo.
    """

    def __init__(self, driver_service):
        super().__init__(driver_service)
        self.contenido_service = ContenidoService()
        self.procesamiento_service = ProcesamientoService()

    def ejecutar(self):
        """
        Ejecuta el proceso de:
        - Preparar driver con cookies
        - Extraer contenido HTML completo y temas principales
        - Guardar los temas como subtítulos en JSON
        - Guardar el HTML en un archivo
        - Procesar ese archivo con reglas específicas
        """
        driver, url = self.driver_service.preparar_driver_y_url()
        if not driver:
            return

        try:
            # pylint: disable=line-too-long
            # flake8: noqa: E501
            contenido = self.contenido_service.extraer_contenido_completo(driver, url)
            sub_temas = self.contenido_service.extraer_temas_principales(driver, url)

            self.procesamiento_service.guardar_subtitulos_json(sub_temas)
            archivo = self.procesamiento_service.guardar_contenido_extraido(url, contenido)
            self.procesamiento_service.procesar_archivo_guardado(archivo)
            # pylint: enable=line-too-long
        finally:
            driver.quit()
