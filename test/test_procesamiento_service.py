"""
test/test_procesamiento_service.py

Pruebas unitarias para el servicio `ProcesamientoService`, responsable
de guardar archivos de salida como JSON y Markdown, y de procesar archivos
extraídos desde Coursera.

Estas pruebas aseguran que:

- Los subtítulos se guarden correctamente como JSON.
- El contenido extraído se guarde correctamente como archivo `.md` o `.txt`.
- La función de procesamiento final se invoque correctamente (si aplica).
"""

import json
import os
from app.services.procesamiento_service import ProcesamientoService


def test_guardar_subtitulos_json(tmp_path):
    """
    Verifica que `guardar_subtitulos_json` cree un archivo JSON válido.
    """
    service = ProcesamientoService()
    subtemas = [{"titulo": "Tema 1"}, {"titulo": "Tema 2"}]
    ruta_json = tmp_path / "subtitulos.json"

    service.guardar_subtitulos_json(subtemas, ruta=str(ruta_json))

    assert ruta_json.exists()

    with open(ruta_json, encoding="utf-8") as f:
        data = json.load(f)
        assert isinstance(data, list)
        assert data == subtemas


def test_guardar_contenido_extraido(tmp_path, monkeypatch):
    """
    Verifica que `guardar_contenido_extraido` cree un archivo correctamente
    nombrado a partir de una URL simulada.
    """
    # Simulamos la función `generar_nombre_archivo`
    func_simulada = "app.services.procesamiento_service.generar_nombre_archivo"

    monkeypatch.setattr(func_simulada,
                        lambda url: str(tmp_path / "contenido.md"))

    service = ProcesamientoService()
    contenido = "# Título\nContenido de prueba"
    url_simulada = "https://example.com/leccion"
    archivo_generado = service.guardar_contenido_extraido(url_simulada,
                                                          contenido)

    assert os.path.exists(archivo_generado)

    with open(archivo_generado, encoding="utf-8") as f:
        texto = f.read()
        assert contenido in texto


def test_procesar_archivo_guardado(monkeypatch):
    """
    Verifica que `procesar_archivo_guardado` invoque correctamente la función
    externa.
    """
    procesado = {"ejecutado": False}

    def mock_procesar(archivo):
        procesado["ejecutado"] = True
        procesado["archivo"] = archivo
    # flake8: noqa: E501
    func_simulada = "app.services.procesamiento_service.procesar_archivo_guardado"
    monkeypatch.setattr(func_simulada, mock_procesar)

    service = ProcesamientoService()
    dummy_archivo = "archivo_prueba.md"
    service.procesar_archivo_guardado(dummy_archivo)

    assert procesado["ejecutado"] is True
    assert procesado["archivo"] == dummy_archivo
