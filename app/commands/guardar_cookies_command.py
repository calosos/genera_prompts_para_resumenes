"""
Archivo: app/commands/guardar_cookies_command.py

Define el comando para guardar cookies mediante login manual.
Implementa el patrón Command.
"""

from app.commands.base_command import BaseCommand


class GuardarCookiesCommand(BaseCommand):
    """
    Comando para guardar cookies usando un flujo interactivo.

    Utiliza el driver_service para abrir Coursera, esperar al login manual
    y guardar las cookies resultantes.
    """

    def ejecutar(self):
        """
        Ejecuta el proceso de guardado de cookies.

        Abre Coursera en el navegador, solicita login manual
        y guarda las cookies tras la confirmación del usuario.
        """
        try:
            driver = self.driver_service.crear_driver()
            self.driver_service.guardar_cookies_interactivo(driver)
        finally:
            if 'driver' in locals():
                driver.quit()
