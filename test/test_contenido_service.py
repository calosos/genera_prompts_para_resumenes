"""
test/test_contenido_service.py

Pruebas unitarias para la clase `ContenidoService`, que encapsula funciones
de extracción de contenido desde páginas de lecciones de Coursera.

Estas pruebas mockean las funciones importadas desde `coursera_utils.py` para
verificar que `ContenidoService` las invoque correctamente.
"""
# flake8: noqa: E501
from unittest.mock import patch
from app.services.contenido_service import ContenidoService


@patch("app.services.contenido_service.extraer_contenido_completo")
def test_extraer_contenido_completo(mock_func):
    """
    Verifica que `extraer_contenido_completo` invoque correctamente
    la función subyacente y devuelva el contenido simulado.
    """
    mock_func.return_value = "contenido completo simulado"
    servicio = ContenidoService()

    resultado = servicio.extraer_contenido_completo("driver_fake", "https://test.url")

    mock_func.assert_called_once_with("driver_fake", "https://test.url")
    assert resultado == "contenido completo simulado"


@patch("app.services.contenido_service.extraer_contenido_completo_leccion")
def test_extraer_contenido_completo_leccion(mock_func):
    """
    Verifica que `extraer_contenido_completo_leccion` invoque correctamente
    la función base con los parámetros esperados.
    """
    mock_func.return_value = "contenido lección simulado"
    servicio = ContenidoService()

    resultado = servicio.extraer_contenido_completo_leccion("driver_fake", "https://test.url")

    mock_func.assert_called_once_with("driver_fake", "https://test.url")
    assert resultado == "contenido lección simulado"


@patch("app.services.contenido_service.extraer_temas_principales")
def test_extraer_temas_principales(mock_func):
    """
    Verifica que `extraer_temas_principales` llame a la función correcta
    y retorne la lista esperada.
    """
    mock_func.return_value = [{"titulo": "Tema 1"}, {"titulo": "Tema 2"}]
    servicio = ContenidoService()

    resultado = servicio.extraer_temas_principales("driver_fake", "https://test.url")

    mock_func.assert_called_once_with("driver_fake", "https://test.url")
    assert isinstance(resultado, list)
    assert resultado[0]["titulo"] == "Tema 1"
