# test/test_menu_handler.py
"""
Test para la clase MenuHandler que maneja la interfaz de usuario.
"""
# pylint: disable=import-error
from unittest.mock import MagicMock, patch
import pytest
from app.ui.menu_handler import MenuHandler


@pytest.fixture
def mock_driver_service():
    """
    Fixture para crear un mock del driver_service.
    """
    return MagicMock()


@pytest.fixture
def mock_command():
    """
    Fixture para crear un mock del comando.
    """
    comando = MagicMock()
    comando.ejecutar = MagicMock()
    return comando


@patch("app.ui.menu_handler.input", side_effect=["1", "Q"])
@patch("app.ui.menu_handler.CommandFactory")
# flake8: noqa: E501
# pylint: disable=unused-argument
def test_mostrar_menu_principal_con_una_opcion(mock_factory_class, mock_input, mock_driver_service, mock_command):
    """
    Verifica que MenuHandler invoque el comando correcto y luego salga al
    presionar Q.
    """
    mock_factory = MagicMock()
    mock_factory.crear_comando.return_value = mock_command
    mock_factory_class.return_value = mock_factory

    handler = MenuHandler(mock_driver_service)
    handler.mostrar_menu_principal()

    # Se llamó a crear_comando una vez con "1"
    mock_factory.crear_comando.assert_called_with("1")
    mock_command.ejecutar.assert_called_once()


@patch("app.ui.menu_handler.input", side_effect=["X", "Q"])
@patch("app.ui.menu_handler.CommandFactory")
def test_mostrar_menu_principal_con_opcion_invalida(mock_factory_class, mock_input, mock_driver_service):
    """
    Verifica que se maneje una opción inválida y luego salir con Q.
    """
    mock_factory = MagicMock()
    mock_factory.crear_comando.return_value = None
    mock_factory_class.return_value = mock_factory

    handler = MenuHandler(mock_driver_service)
    handler.mostrar_menu_principal()

    # Se llamó a crear_comando con "X", pero no se ejecutó ningún comando
    mock_factory.crear_comando.assert_called_with("X")
