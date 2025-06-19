"""
Archivo: app/commands/base_command.py

Define la interfaz base para los comandos del sistema Coursera.
Implementa el patrón Command.
"""

from abc import ABC, abstractmethod


class BaseCommand(ABC):
    """
    Clase abstracta base para los comandos.

    Cada comando debe heredar de esta clase e implementar el método `ejecutar`.
    """

    def __init__(self, driver_service):
        self.driver_service = driver_service

    @abstractmethod
    def ejecutar(self):
        """
        Ejecuta la acción del comando.
        Este método debe ser implementado por las subclases.
        """
