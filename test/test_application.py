# test/test_application.py
"""
Prueba para la clase CourseraApplication ubicada en: app/application.py

Verifica que la aplicación inicializa correctamente los servicios y ejecuta el
menú principal.
"""

from unittest.mock import patch, MagicMock
from app.application import CourseraApplication


@patch("app.application.MenuHandler")
@patch("app.application.DriverService")
# pylint: disable=unused-argument
def test_run_aplicacion(mock_driver_service_class, mock_menu_handler_class):
    """
    Verifica que se construya correctamente CourseraApplication
    y que se llame a mostrar_menu_principal().
    """
    mock_menu_handler = MagicMock()
    mock_menu_handler_class.return_value = mock_menu_handler

    app = CourseraApplication()
    app.run()

    mock_menu_handler_class.assert_called_once_with(app.driver_service)
    mock_menu_handler.mostrar_menu_principal.assert_called_once()
