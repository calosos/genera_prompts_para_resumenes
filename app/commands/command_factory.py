# app/commands/command_factory.py

"""
Archivo: app/commands/command_factory.py

Define una fábrica para construir comandos basados en opciones del usuario.
Implementa el patrón Factory Method.
"""

from app.commands.guardar_cookies_command import GuardarCookiesCommand
from app.commands.extraer_y_procesar_command import ExtraerYProcesarCommand
from app.commands.extraer_y_resumir_command import ExtraerYResumirCommand
from app.commands.resumir_multiples_command import ResumirMultiplesCommand


class CommandFactory:
    """
    Fábrica de comandos. Se encarga de mapear opciones del menú con comandos
    concretos.
    """

    def __init__(self, driver_service):
        self.driver_service = driver_service
        self._comandos = {
            "1": GuardarCookiesCommand,
            "2": ExtraerYProcesarCommand,
            "3": ExtraerYResumirCommand,
            "4": ResumirMultiplesCommand
        }

    def crear_comando(self, opcion):
        """
        Crea el comando correspondiente a la opción ingresada.

        Args:
            opcion (str): Opción ingresada por el usuario.

        Returns:
            BaseCommand o None: Comando correspondiente o None si la opción no
            es válida.
        """
        command_class = self._comandos.get(opcion)
        if command_class:
            return command_class(self.driver_service)
        return None
