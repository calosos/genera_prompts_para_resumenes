# app/ui/menu_handler.py
"""
Clase MenuHandler ubicada en: app/ui/menu_handler.py

Esta clase maneja la interfaz de usuario del menú principal de la aplicación
Coursera.
Se encarga de mostrar las opciones disponibles al usuario y ejecutar el comando
correspondiente utilizando el patrón Command. Actúa como punto de interacción
entre el usuario y la lógica de negocio, facilitando la navegación por el
sistema.
"""

from app.commands.command_factory import CommandFactory


class MenuHandler:
    """
    Maneja la interfaz de usuario del menú.
    Implementa el patrón Command para ejecutar acciones.
    """

    def __init__(self, driver_service):
        self.driver_service = driver_service
        self.command_factory = CommandFactory(driver_service)

    def mostrar_menu_principal(self):
        """Muestra el menú principal y maneja la interacción del usuario."""
        while True:
            opcion = self._mostrar_opciones()

            if opcion.upper() == "Q":
                break

            command = self.command_factory.crear_comando(opcion)
            if command:
                command.ejecutar()
            else:
                print("❌ Opción no válida. Intenta de nuevo.")

    def _mostrar_opciones(self):
        """Muestra las opciones del menú y retorna la selección del usuario."""
        print("\n📘 Menú Principal")
        print("1. Guardar cookies (login manual)")
        print("2. Extraer y procesar contenido de una lección")
        print("3. Extraer y resumir contenido de una lección")
        print("4. Extraer resúmenes de múltiples lecciones (archivo fijo: "
              "urls_resumen.txt)")
        print("Q. Salir")
        return input("Ingresa una opción (1-4 o Q): ").strip()
