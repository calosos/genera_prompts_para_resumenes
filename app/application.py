# app/application.py
"""
Módulo que contiene la clase CourseraApplication.
Ubicación: app/application.py

Esta clase representa el punto de entrada de alto nivel de la aplicación.
Implementa el patrón **Facade**, ocultando la complejidad de servicios y
comandos detrás de una interfaz simple.
"""

from app.ui.menu_handler import MenuHandler
from app.services.driver_service import DriverService


class CourseraApplication:
    """
    Clase principal de la aplicación que coordina los componentes.
    Implementa el patrón Facade para simplificar la interfaz.
    """

    def __init__(self):
        """
        Inicializa los servicios y el manejador de menú.
        """
        self.driver_service = DriverService()
        self.menu_handler = MenuHandler(self.driver_service)

    def run(self):
        """
        Ejecuta la aplicación principal.
        Muestra el menú y permite la interacción con el usuario.
        """
        print("🚀 Iniciando aplicación Coursera...")
        self.menu_handler.mostrar_menu_principal()
        print("👋 ¡Hasta luego!")
