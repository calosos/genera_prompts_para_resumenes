"""
app/services/driver_service.py

Servicio para manejo de WebDriver (Selenium) y gestión de cookies de sesión.

Este módulo define la clase `DriverService`, responsable de encapsular la
lógica necesaria para:
- Crear un navegador automatizado.
- Cargar y guardar cookies de sesión para Coursera.
- Preparar un entorno interactivo para extraer contenido desde una URL.

Funciones clave:
- Facilita la reutilización de sesión iniciada mediante cookies.
- Permite automatizar navegación sin tener que autenticar en cada ejecución.
- Prepara el WebDriver y valida la URL objetivo antes de pasarla a capas
superiores.

Dependencias externas:
- Funciones definidas en `coursera_utils.py`: `crear_driver`,
`guardar_cookies`, `cargar_cookies`, y `COOKIES_FILE`.
"""

import os
import time
from coursera_utils import (crear_driver,
                            guardar_cookies,
                            cargar_cookies,
                            COOKIES_FILE)


class DriverService:
    """
    Servicio para manejo de WebDriver y cookies de sesión.

    Implementa el patrón Service Layer para desacoplar la inicialización
    del navegador, carga de cookies y validación de URL del resto del sistema.
    """

    def crear_driver(self):
        """
        Crea y retorna una instancia de WebDriver preconfigurada.

        Returns:
            selenium.webdriver: Instancia lista para usarse.
        """
        return crear_driver()

    def guardar_cookies_interactivo(self, driver):
        """
        Realiza un flujo de login manual en Coursera y guarda las cookies
        resultantes.

        Args:
            driver (selenium.webdriver): Instancia activa del navegador.

        Este método abre Coursera en el navegador, pide al usuario que inicie
        sesión, y luego guarda las cookies para futuras ejecuciones
        automatizadas.
        """
        driver.get("https://www.coursera.org")
        print("➡️ Inicia sesión manualmente en la ventana abierta.")
        input("Presiona Enter cuando hayas terminado el login...")
        guardar_cookies(driver)

    def preparar_driver_y_url(self, url_manual=None):
        """
        Prepara el entorno automatizado: carga cookies y solicita la URL a
        visitar.

        Args:
            url_manual (str | None): URL a visitar. Si no se proporciona,
            se pedirá al usuario.

        Returns:
            tuple: (driver, url) si todo es válido, o (None, None) en caso
            de error.
        """
        if not os.path.exists(COOKIES_FILE):
            print("❌ No hay cookies guardadas. Ejecuta la opción 1 primero.")
            return None, None

        driver = self.crear_driver()
        driver.get("https://www.coursera.org")
        cargar_cookies(driver)
        driver.refresh()
        time.sleep(2)
        # flake8: noqa: E128
        url = url_manual or input("🔗 Pega la URL de la lección que quieres "
                                 "extraer: ").strip()
        if not url:
            print("⚠️ No se proporcionó ninguna URL.")
            driver.quit()
            return None, None

        return driver, url
