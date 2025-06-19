"""
app/services/contenido_service.py

Servicio de extracción de contenido desde páginas de lecciones en Coursera.

Este módulo define la clase `ContenidoService`, que encapsula la lógica
para obtener el contenido textual de una lección, ya sea completo o
estructurado por secciones.

El servicio se apoya en funciones externas definidas en `coursera_utils.py`,
y sirve como puente entre el WebDriver (Selenium) y las capas superiores
de procesamiento o resumen.

Funciones principales:
- Extraer todo el contenido visible de una lección.
- Extraer únicamente el cuerpo principal (transcripción).
- Obtener los temas o subtítulos principales para estructurar el texto.
"""

from coursera_utils import (
    extraer_temas_principales,
    extraer_contenido_completo,
    extraer_contenido_completo_leccion,
)


class ContenidoService:
    """
    Servicio de extracción de contenido desde una lección de Coursera.

    Esta clase proporciona una interfaz consistente para obtener el contenido
    de una página, ya sea como texto plano completo, por secciones principales,
    o en formato bruto para procesamiento posterior.
    """

    def extraer_contenido_completo(self, driver, url):
        """
        Extrae todo el contenido textual visible desde una URL.

        Args:
            driver (selenium.webdriver): WebDriver activo con sesión en
            Coursera.
            url (str): URL de la lección.

        Returns:
            str: Texto completo extraído.
        """
        return extraer_contenido_completo(driver, url)

    def extraer_contenido_completo_leccion(self, driver, url):
        """
        Extrae el cuerpo principal del contenido de una lección,
        omitiendo elementos decorativos o irrelevantes.

        Args:
            driver (selenium.webdriver): WebDriver con sesión activa.
            url (str): URL del contenido específico.

        Returns:
            str: Transcripción limpia de la lección.
        """
        return extraer_contenido_completo_leccion(driver, url)

    def extraer_temas_principales(self, driver, url):
        """
        Extrae los títulos de secciones o subtítulos relevantes de una lección.

        Args:
            driver (selenium.webdriver): WebDriver activo.
            url (str): URL de la lección o recurso.

        Returns:
            list[dict]: Lista de temas o subtítulos estructurados.
        """
        return extraer_temas_principales(driver, url)
