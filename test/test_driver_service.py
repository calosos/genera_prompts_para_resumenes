"""
test/test_driver_service.py

Pruebas unitarias para el módulo `app/services/driver_service.py`.

Este archivo valida el comportamiento del servicio encargado de:
- Crear un driver de Selenium usando funciones utilitarias.
- Preparar una sesión reutilizando cookies si están disponibles.
- Obtener la URL de la lección desde el usuario.
- Manejar el flujo interactivo de login y guardado de cookies.

Se emplea `unittest.mock` para simular entradas del usuario, drivers y funciones externas
sin depender de conexión real a Coursera ni abrir el navegador.
"""
# flake8: noqa: E501
from unittest.mock import patch, MagicMock
from app.services.driver_service import DriverService


@patch("app.services.driver_service.crear_driver")
def test_crear_driver(mock_crear_driver):
    """Verifica que `crear_driver()` invoque la función externa correctamente."""
    mock_driver = MagicMock()
    mock_crear_driver.return_value = mock_driver

    service = DriverService()
    driver = service.crear_driver()

    mock_crear_driver.assert_called_once()
    assert driver == mock_driver


@patch("app.services.driver_service.input", return_value="")
@patch("app.services.driver_service.os.path.exists", return_value=True)
@patch("app.services.driver_service.cargar_cookies")
@patch("app.services.driver_service.crear_driver")
# pylint: disable=unused-argument
def test_preparar_driver_y_url_sin_url(mock_crear_driver,
                                       mock_cargar_cookies,
                                       mock_path_exists,
                                       mock_input):
    # pylint: disable=line-too-long
    """Verifica que el flujo se interrumpa si no se proporciona URL."""
    mock_driver = MagicMock()
    mock_crear_driver.return_value = mock_driver

    service = DriverService()
    driver, url = service.preparar_driver_y_url()

    assert driver is None
    assert url is None
    mock_driver.quit.assert_called_once()


@patch("app.services.driver_service.input", return_value="https://coursera.org/leccion")
@patch("app.services.driver_service.os.path.exists", return_value=True)
@patch("app.services.driver_service.cargar_cookies")
@patch("app.services.driver_service.crear_driver")
# pylint: disable=unused-argument
def test_preparar_driver_y_url_ok(mock_crear_driver, mock_cargar_cookies,
                                  mock_path_exists, mock_input):
    # pylint: disable=line-too-long
    """Verifica que se prepare el driver correctamente y se obtenga una URL válida."""
    mock_driver = MagicMock()
    mock_crear_driver.return_value = mock_driver

    service = DriverService()
    driver, url = service.preparar_driver_y_url()

    assert driver == mock_driver
    assert url == "https://coursera.org/leccion"
    mock_cargar_cookies.assert_called_once_with(mock_driver)
