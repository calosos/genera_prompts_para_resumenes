"""
test/test_file_utils.py

Pruebas unitarias para el módulo `file_utils.py`, que contiene utilidades
relacionadas con la lectura de archivos de URLs y confirmación del usuario.

Estas pruebas aseguran que:

- Las URLs se lean correctamente desde archivos con formato mixto (líneas
vacías y comentarios).
- El flujo se cancele correctamente si el usuario no confirma.
- Se maneje adecuadamente la ausencia del archivo.
"""
from app.utils.file_utils import FileUtils


def test_leer_y_confirmar_urls_ok(tmp_path, monkeypatch):
    """
    Verifica que se lean correctamente las URLs desde un archivo válido
    y se filtren líneas vacías y comentarios. El usuario confirma con 's'.
    """
    archivo = tmp_path / "urls_resumen.txt"
    archivo.write_text("https://ejemplo.com/leccion1\n\n# Esto es un "
                       "comentario\nhttps://ejemplo.com/leccion2")

    monkeypatch.setattr("builtins.input", lambda _: "s")

    fu = FileUtils()
    resultado = fu.leer_y_confirmar_urls(str(archivo))

    assert resultado == [
        "https://ejemplo.com/leccion1",
        "https://ejemplo.com/leccion2"
    ]


def test_leer_y_confirmar_urls_cancelado(tmp_path, monkeypatch):
    """
    Verifica que el método devuelva None si el usuario no confirma
    (responde con 'n' cuando se le pide validación).
    """
    archivo = tmp_path / "urls_resumen.txt"
    archivo.write_text("https://ejemplo.com/leccion1\n")

    monkeypatch.setattr("builtins.input", lambda _: "n")

    fu = FileUtils()
    resultado = fu.leer_y_confirmar_urls(str(archivo))

    assert resultado is None


def test_leer_y_confirmar_urls_no_existe():
    """
    Verifica que el método devuelva None si el archivo proporcionado no existe.
    """
    fu = FileUtils()
    resultado = fu.leer_y_confirmar_urls("ruta/que/no/existe.txt")

    assert resultado is None
