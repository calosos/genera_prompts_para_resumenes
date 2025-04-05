import os
import time
from coursera_utils import (
    crear_driver,
    guardar_cookies,
    cargar_cookies,
    extraer_contenido,
    generar_nombre_archivo,
    COOKIES_FILE
)
from flujo_procesamiento import procesar_archivo_guardado


def opcion_guardar_cookies(driver):
    driver.get("https://www.coursera.org")
    print("➡️ Inicia sesión manualmente en la ventana abierta.")
    input("Presiona Enter cuando hayas terminado el login...")
    guardar_cookies(driver)


def opcion_extraer_y_procesar_contenido(driver):
    if not os.path.exists(COOKIES_FILE):
        print("❌ No hay cookies guardadas. Ejecuta la opción 1 primero.")
        return

    driver.get("https://www.coursera.org")
    cargar_cookies(driver)
    driver.refresh()
    time.sleep(2)

    url = input("🔗 Pega la URL de la lección que quieres extraer: ").strip()
    contenido = extraer_contenido(driver, url)

    archivo = guardar_contenido_extraido(url, contenido)
    procesar_archivo_guardado(archivo)


def guardar_contenido_extraido(url, contenido):
    archivo = generar_nombre_archivo(url)
    os.makedirs(os.path.dirname(archivo), exist_ok=True)
    with open(archivo, "w", encoding="utf-8") as f:
        f.write(contenido)

    print(f"✅ Contenido guardado en: {archivo}")
    return archivo


def mostrar_menu():
    print("¿Qué deseas hacer?")
    print("1. Guardar cookies (login manual)")
    print("2. Usar cookies guardadas y extraer contenido")
    return input("Ingresa 1 o 2: ").strip()


def main():
    opcion = mostrar_menu()
    driver = crear_driver()

    if opcion == "1":
        opcion_guardar_cookies(driver)
    elif opcion == "2":
        opcion_extraer_y_procesar_contenido(driver)
    else:
        print("❌ Opción no válida.")

    driver.quit()

if __name__ == "__main__":
    main()
