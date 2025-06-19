"""
app/services/procesamiento_service.py

Servicio de procesamiento de contenido extraído desde Coursera.

Este módulo forma parte del Service Layer y se encarga de:
- Guardar subtítulos como JSON.
- Guardar el contenido extraído de una lección en archivos de texto.
- Ejecutar un flujo de procesamiento adicional sobre archivos previamente
guardados.

Funciones clave:
- Interfaz simple para persistencia de contenido.
- Delegación del procesamiento real a módulos externos (`flujo_procesamiento`).
- Aislamiento de lógica de escritura de archivos desde otros componentes.

Uso típico:
    service = ProcesamientoService()
    archivo = service.guardar_contenido_extraido(url, contenido)
    service.procesar_archivo_guardado(archivo)
"""

import json
import os
import traceback
from coursera_utils import generar_nombre_archivo
from flujo_procesamiento import procesar_archivo_guardado


class ProcesamientoService:
    """
    Servicio para procesamiento de contenido extraído desde Coursera.

    Implementa el patrón Service Layer para desacoplar la lógica de escritura y
    procesamiento de archivos del resto de la aplicación. Esta clase ofrece
    métodos reutilizables para almacenar subtítulos y contenidos, y para
    invocar rutina de post-procesamiento.
    """

    def guardar_subtitulos_json(self, subtemas, ruta="subtitulos.json"):
        """
        Guarda la lista de subtítulos o temas extraídos en un archivo JSON.

        Args:
            subtemas (list): Lista de temas o subtítulos extraídos de la
            lección.
            ruta (str): Ruta del archivo JSON a generar
            (por defecto: subtitulos.json).
        """
        try:
            with open(ruta, "w", encoding="utf-8") as f:
                json.dump(subtemas, f, indent=2, ensure_ascii=False)
            print(f"✅ subtitulos.json actualizado con {len(subtemas)} temas.")
        except (IOError, OSError, TypeError, json.JSONDecodeError) as error:
            print(f"❌ Error al guardar subtítulos en '{ruta}': "
                  f"{type(error).__name__} - {error}")
            traceback.print_exc()

    def guardar_contenido_extraido(self, url, contenido):
        """
        Guarda el contenido de una lección en un archivo de texto.

        Args:
            url (str): URL de la lección, usada para generar el nombre de
            archivo.
            contenido (str): Texto extraído completo.

        Returns:
            str: Ruta absoluta del archivo guardado.
        """
        archivo = generar_nombre_archivo(url)
        os.makedirs(os.path.dirname(archivo), exist_ok=True)

        with open(archivo, "w", encoding="utf-8") as f:
            f.write(contenido)

        print(f"✅ Contenido guardado en: {archivo}")
        return archivo

    def procesar_archivo_guardado(self, archivo):
        """
        Aplica un flujo de procesamiento estructurado al archivo previamente
        guardado.

        Este paso suele incluir limpieza, segmentación y reestructuración del
        contenido
        para facilitar su posterior uso o resumen.

        Args:
            archivo (str): Ruta del archivo de contenido que se desea procesar.
        """
        procesar_archivo_guardado(archivo)
