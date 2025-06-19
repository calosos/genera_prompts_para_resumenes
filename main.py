"""
Archivo principal de entrada de la aplicación.
Ubicación: main.py

Este script inicializa y ejecuta la aplicación completa.
Sirve como punto de entrada (entrypoint) cuando se ejecuta desde la terminal
o entorno local.
"""

from app.application import CourseraApplication


def main():
    """
    Punto de entrada principal de la aplicación.
    Solo inicializa y ejecuta la aplicación.
    """
    app = CourseraApplication()
    app.run()


if __name__ == "__main__":
    main()
