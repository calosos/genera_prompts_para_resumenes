"""
app/services/resumen_service.py

Servicio para la generación de resúmenes a partir de contenido extraído de
Coursera.

Este módulo contiene la clase `ResumenService`, que forma parte del Service
Layer de la aplicación. Su responsabilidad es orquestar la extracción del
contenido, procesarlo mediante funciones auxiliares y un agente de resumen,
y almacenar el resultado en archivos Markdown.

Funciones principales:
- Extraer contenido completo de una lección con `ContenidoService`.
- Procesar el texto con `extraer_transcripcion` y `AgenteResumidor`.
- Guardar el resumen generado con formato claro y estructurado.
- Procesar múltiples URLs de forma secuencial.

Requiere:
- Un driver de Selenium con sesión activa en Coursera.
- Funciones auxiliares del módulo `procesar_texto_leccion`.
- Un agente basado en LLM (`AgenteResumidor`).
"""

import re
from datetime import datetime
from procesar_texto_leccion import extraer_transcripcion, obten_titulo
# pylint: disable=wrong-import-position, import-error, no-name-in-module
# pylint: disable=wrong-import-order
from selenium.common.exceptions import WebDriverException
# pylint: enable=wrong-import-position, import-error, no-name-in-module
# pylint: enable=wrong-import-order
from agentes.agente_resumidor import AgenteResumidor
from config import CARPETA_RESUMENES
from app.services.contenido_service import ContenidoService


class ResumenService:
    """
    Servicio para la generación de resúmenes automáticos a partir de contenido
    web.

    Esta clase coordina la extracción de contenido educativo desde Coursera,
    aplica lógica de transcripción y resumen utilizando un agente LLM, y
    almacena el resultado en archivos Markdown legibles y organizados.

    Implementa el patrón Service Layer para mantener la separación entre
    lógica de dominio y presentación/interacción.
    """

    def __init__(self):
        """Inicializa el servicio de resúmenes con acceso a
        `ContenidoService`."""
        self.contenido_service = ContenidoService()

    def procesar_y_guardar_resumen(self, driver, url):
        """
        Extrae el contenido de una URL y guarda su resumen en un archivo.

        Args:
            driver (selenium.webdriver): Instancia con sesión activa en
            Coursera.
            url (str): URL de la lección a procesar.

        Returns:
            str | None: Resumen generado si fue exitoso, o None si falló.
        """
        contenido = self.contenido_service.extraer_contenido_completo_leccion(
            driver, url)
        transcripcion = extraer_transcripcion(contenido)
        titulo = obten_titulo(contenido)

        resumen = AgenteResumidor.resumir_contenido(transcripcion, titulo)

        if not resumen:
            print(f"⚠️ ADVERTENCIA: No se pudo generar resumen para "
                  f"'{titulo}'.")
            return None

        self._guardar_resumen(titulo, resumen)
        return resumen

    def procesar_multiples_resumenes(self, driver, lista_urls):
        """
        Procesa una lista de URLs para extraer y guardar sus resúmenes.

        Args:
            driver (selenium.webdriver): Instancia activa de navegador.
            lista_urls (list[str]): Lista de URLs a procesar en lote.
        """
        for url in lista_urls:
            try:
                print(f"\n🔍 Procesando: {url}")
                self.procesar_y_guardar_resumen(driver, url)
            except (WebDriverException, ValueError, TypeError) as error:
                print(f"❌ Error procesando {url}: {type(error).__name__} - "
                      f"{error}")

    def _guardar_resumen(self, titulo, resumen):
        """
        Guarda un resumen generado en un archivo Markdown.

        Args:
            titulo (str): Título de la lección.
            resumen (str): Texto del resumen generado.
        """
        fecha_hora = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        titulo_limpio = re.sub(r"[^\w\-]+", "_", titulo.strip())
        nombre_archivo = f"resumen_{titulo_limpio}_{fecha_hora}.md"
        ruta_resumen = CARPETA_RESUMENES / nombre_archivo

        ruta_resumen.parent.mkdir(parents=True, exist_ok=True)

        with open(ruta_resumen, "w", encoding="utf-8") as f:
            f.write(f"# {titulo}\n\n{resumen}")

        print(f"✅ Resumen guardado en: {ruta_resumen}")
