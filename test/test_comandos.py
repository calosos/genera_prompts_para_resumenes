# test/test_comandos.py

"""
Archivo de pruebas para los comandos principales de la aplicación Coursera.
Prueba los comandos:
1. GuardarCookiesCommand
2. ExtraerYProcesarCommand
3. ExtraerYResumirCommand
4. ResumirMultiplesCommand
"""
# pylint: disable=import-error
import pytest
from unittest.mock import patch, MagicMock
from app.commands.guardar_cookies_command import GuardarCookiesCommand
from app.commands.extraer_y_procesar_command import ExtraerYProcesarCommand
from app.commands.extraer_y_resumir_command import ExtraerYResumirCommand
from app.commands.resumir_multiples_command import ResumirMultiplesCommand


@pytest.fixture
def mock_driver_service():
    service = MagicMock()
    service.crear_driver.return_value = MagicMock()
    service.preparar_driver_y_url.return_value = (MagicMock(), "https://example.com")
    service.guardar_cookies_interactivo = MagicMock()
    return service

def test_guardar_cookies_command(mock_driver_service):
    comando = GuardarCookiesCommand(mock_driver_service)
    comando.ejecutar()
    mock_driver_service.crear_driver.assert_called_once()
    mock_driver_service.guardar_cookies_interactivo.assert_called_once()

@patch("app.commands.extraer_y_procesar_command.ContenidoService")
@patch("app.commands.extraer_y_procesar_command.ProcesamientoService")
def test_extraer_y_procesar_command(mock_proc, mock_contenido,
                                    mock_driver_service):
    comando = ExtraerYProcesarCommand(mock_driver_service)

    mock_contenido.return_value.extraer_contenido_completo.return_value = "contenido simulado"
    mock_contenido.return_value.extraer_temas_principales.return_value = ["Tema 1", "Tema 2"]
    mock_proc.return_value.guardar_subtitulos_json.return_value = None
    mock_proc.return_value.guardar_contenido_extraido.return_value = "archivo.md"
    mock_proc.return_value.procesar_archivo_guardado.return_value = None

    comando.ejecutar()
    assert mock_proc.return_value.guardar_subtitulos_json.called
    assert mock_proc.return_value.procesar_archivo_guardado.called

@patch("app.commands.extraer_y_resumir_command.ResumenService")
@patch("app.commands.extraer_y_resumir_command.ContenidoService")
def test_extraer_y_resumir_command(mock_contenido, mock_resumen, 
                                   mock_driver_service):
    comando = ExtraerYResumirCommand(mock_driver_service)
    mock_resumen.return_value.procesar_y_guardar_resumen.return_value = "Resumen listo"
    comando.ejecutar()
    assert mock_resumen.return_value.procesar_y_guardar_resumen.called

@patch("app.commands.resumir_multiples_command.ResumenService")
@patch("app.commands.resumir_multiples_command.FileUtils")
def test_resumir_multiples_command(mock_utils, mock_resumen, 
                                   mock_driver_service):
    comando = ResumirMultiplesCommand(mock_driver_service)
    mock_utils.return_value.leer_y_confirmar_urls.return_value = [
        "https://coursera.org/leccion1", "https://coursera.org/leccion2"
    ]
    mock_resumen.return_value.procesar_multiples_resumenes.return_value = None

    comando.ejecutar()
    mock_resumen.return_value.procesar_multiples_resumenes.assert_called_once()
