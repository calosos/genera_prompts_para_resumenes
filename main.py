import json
import os
import time
import  re
from coursera_utils import (
    crear_driver,
    guardar_cookies,
    cargar_cookies,
    extraer_temas_principales,
    extraer_contenido_completo,
    extraer_contenido_completo_leccion,
    generar_nombre_archivo,
    COOKIES_FILE
)
from flujo_procesamiento import procesar_archivo_guardado
from procesar_texto_leccion import extraer_transcripcion, obten_titulo
from agentes.agente_resumidor import AgenteResumidor
from config import CARPETA_RESUMENES
from datetime import datetime


def guardar_subtitulos_json(subtemas, ruta="subtitulos.json"):
    try:
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(subtemas, f, indent=2, ensure_ascii=False)
        print(f"✅ subtitulos.json actualizado con {len(subtemas)} temas.")
    except Exception as e:
        print(f"❌ Error al guardar subtítulos: {e}")


def opcion_guardar_cookies(driver):
    driver.get("https://www.coursera.org")
    print("➡️ Inicia sesión manualmente en la ventana abierta.")
    input("Presiona Enter cuando hayas terminado el login...")
    guardar_cookies(driver)


def guardar_contenido_extraido(url, contenido):
    archivo = generar_nombre_archivo(url)
    os.makedirs(os.path.dirname(archivo), exist_ok=True)
    with open(archivo, "w", encoding="utf-8") as f:
        f.write(contenido)

    print(f"✅ Contenido guardado en: {archivo}")
    return archivo


def preparar_driver_y_url(url_manual=None):
    """
    Inicializa el driver, carga cookies y navega a Coursera.
    Retorna el driver y la URL válida (manual o ingresada).
    """
    if not os.path.exists(COOKIES_FILE):
        print("❌ No hay cookies guardadas. Ejecuta la opción 1 primero.")
        return None, None

    driver = crear_driver()
    driver.get("https://www.coursera.org")
    cargar_cookies(driver)
    driver.refresh()
    time.sleep(2)

    url = url_manual or input("🔗 Pega la URL de la lección que quieres extraer: ").strip()
    if not url:
        print("⚠️ No se proporcionó ninguna URL.")
        driver.quit()
        return None, None

    return driver, url


def opcion_extraer_y_resumir_contenido(url_manual=None):
    driver, url = preparar_driver_y_url(url_manual)
    if not driver:
        return

    contenido = extraer_contenido_completo_leccion(driver, url)
    transcripcion = extraer_transcripcion(contenido)
    titulo = obten_titulo(contenido)

    resumen = AgenteResumidor.resumir_contenido(transcripcion, titulo)

    if not resumen:
        print(f"⚠️ ADVERTENCIA: No se pudo generar resumen para '{titulo}'.")
        driver.quit()
        return None

    fecha_hora = datetime.now().strftime("%Y-%m-%d_%H%M%S")

    # Limpia el título para que sea seguro como nombre de archivo

    titulo_limpio = re.sub(r"[^\w\-]+", "_", titulo.strip())

    ruta_resumen = CARPETA_RESUMENES / f"resumen_{titulo_limpio}_{fecha_hora}.md"

    # Asegurar que la carpeta existe
    ruta_resumen.parent.mkdir(parents=True, exist_ok=True)

    # Guardar el resumen
    with open(ruta_resumen, "w", encoding="utf-8") as f:
        f.write(f"# {titulo}\n\n")
        f.write(resumen)

    print(f"✅ Resumen guardado en: {ruta_resumen}")
    driver.quit()


def opcion_extraer_y_procesar_contenido(url_manual=None):
    driver, url = preparar_driver_y_url(url_manual)
    if not driver:
        return

    contenido = extraer_contenido_completo(driver, url)
    sub_temas = extraer_temas_principales(driver, url)
    guardar_subtitulos_json(sub_temas)

    archivo = guardar_contenido_extraido(url, contenido)
    procesar_archivo_guardado(archivo)


def mostrar_menu():
    print("¿Qué deseas hacer?")
    print("1. Guardar cookies (login manual)")
    print("2. Usar cookies guardadas y extraer contenido")
    print("3. Usar cookies guardadas y extraer contenido de una lección")

    return input("Ingresa 1, 2 o 3: ").strip()


def main_dos():
    prueba_url = "https://www.coursera.org/learn/python-crash-course/home/module/2"
    opcion_extraer_y_procesar_contenido(url_manual=prueba_url)
    driver.quit()


def main():
    opcion = mostrar_menu()

    if opcion == "1":
        driver = crear_driver()
        opcion_guardar_cookies(driver)
        driver.quit()
    elif opcion == "2":
        opcion_extraer_y_procesar_contenido()
    elif opcion == "3":
        opcion_extraer_y_resumir_contenido()
    else:
        print("❌ Opción no válida.")


if __name__ == "__main__":
    main()
    # main_dos()