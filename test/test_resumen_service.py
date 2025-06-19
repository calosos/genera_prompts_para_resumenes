"""
test/test_resumen_service.py

Pruebas unitarias para la clase `ResumenService`, validando la lógica de
extracción, resumen y guardado de contenido desde una lección de Coursera.

Se mockean todas las dependencias externas para que la prueba sea rápida
y sin acceso a red.
"""

import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock
from app.services.resumen_service import ResumenService


@patch("app.services.resumen_service.AgenteResumidor.resumir_contenido")
@patch("app.services.resumen_service.obten_titulo")
@patch("app.services.resumen_service.extraer_transcripcion")
@patch("app.services.resumen_service.ContenidoService")
@patch("app.services.resumen_service.CARPETA_RESUMENES",
       new_callable=lambda: Path("test/output"))
def test_procesar_y_guardar_resumen_ok(
    mock_output_dir,
    mock_contenido_service,
    mock_transcripcion,
    mock_titulo,
    mock_resumir
):
    """
    Verifica que `procesar_y_guardar_resumen` genere un archivo correctamente
    cuando todas las dependencias responden como se espera.
    """

    # Limpieza previa por si quedó algo
    if mock_output_dir.exists():
        shutil.rmtree(mock_output_dir)

    # Configuración de mocks
    mock_driver = MagicMock()
    # flake8: noqa: E501
    # pylint: disable=line-too-long
    contenido_simulado = "<html>contenido</html>"
    mock_contenido_service.return_value.extraer_contenido_completo_leccion.return_value = contenido_simulado
    mock_transcripcion.return_value = "Texto de transcripción simulada"
    mock_titulo.return_value = "Titulo de Prueba"  # sin tilde para coincidir con el patrón
    mock_resumir.return_value = "Este es el resumen generado por el agente IA."

    # Ejecutar el servicio
    servicio = ResumenService()
    url = "https://coursera.org/ejemplo"
    resumen = servicio.procesar_y_guardar_resumen(mock_driver, url)

    # Verificaciones
    assert resumen is not None
    assert "resumen generado" in resumen

    archivos = list(mock_output_dir.glob("resumen_Titulo_de_Prueba_*.md"))
    assert len(archivos) == 1

    contenido_archivo = archivos[0].read_text(encoding="utf-8")
    assert "# Titulo de Prueba" in contenido_archivo
    assert "Este es el resumen generado" in contenido_archivo

    # Limpieza final
    shutil.rmtree(mock_output_dir)
