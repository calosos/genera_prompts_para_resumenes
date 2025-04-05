import time
import json
import os
from datetime import datetime
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

CHROME_DRIVER_PATH = "/usr/bin/chromedriver"  # ⬅️ Reemplaza esto por tu ruta real
COOKIES_FILE = "coursera_cookies.json"

def guardar_cookies(driver):
    cookies = driver.get_cookies()
    with open(COOKIES_FILE, "w") as f:
        json.dump(cookies, f)
    print("✅ Cookies guardadas correctamente.")

def cargar_cookies(driver):
    with open(COOKIES_FILE, "r") as f:
        cookies = json.load(f)
        for cookie in cookies:
            driver.add_cookie(cookie)

def cerrar_modal_traduccion(driver):
    try:
        botones = driver.find_elements(By.XPATH, "//button")
        for boton in botones:
            texto = boton.text.strip().lower()
            if "continuar" in texto:
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", boton)
                driver.execute_script("arguments[0].click();", boton)
                print("🔘 Modal de traducción cerrado.")
                time.sleep(1)
                return
        print("ℹ️ Botón 'Continuar' no fue encontrado (puede que el modal no esté visible).")
    except Exception as e:
        print(f"⚠️ Error al cerrar modal de traducción: {e}")

def expandir_secciones(driver):
    try:
        # Forzar scroll hasta el final para cargar más contenido
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        # Buscar botones colapsables visibles con íconos o estado aria-expanded
        botones = driver.find_elements(By.XPATH, "//button[.//svg or @aria-expanded='false']")

        print(f"🔍 Detectados {len(botones)} botones potenciales de sección.")

        for boton in botones:
            try:
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", boton)
                driver.execute_script("arguments[0].click();", boton)
                time.sleep(0.4)
            except Exception as e:
                print(f"⚠️ No se pudo hacer clic en un botón: {e}")
    except Exception as e:
        print(f"⚠️ Error al buscar o expandir secciones: {e}")

def extraer_contenido(driver, url):
    driver.get(url)
    time.sleep(5)
    cerrar_modal_traduccion(driver)
    expandir_secciones(driver)
    time.sleep(2)
    try:
        contenido = driver.find_element(By.TAG_NAME, "main").text
        return contenido
    except Exception as e:
        return f"⚠️ No se pudo extraer el contenido: {e}"

def main():
    print("¿Qué deseas hacer?")
    print("1. Guardar cookies (login manual)")
    print("2. Usar cookies guardadas y extraer contenido")
    opcion = input("Ingresa 1 o 2: ").strip()
    # opcion = '2'
    driver = webdriver.Chrome(service=Service(CHROME_DRIVER_PATH))

    if opcion == "1":
        driver.get("https://www.coursera.org")
        print("➡️ Inicia sesión manualmente en la ventana abierta.")
        input("Presiona Enter cuando hayas terminado el login...")
        guardar_cookies(driver)

    elif opcion == "2":
        if not os.path.exists(COOKIES_FILE):
            print("❌ No hay cookies guardadas. Ejecuta la opción 1 primero.")
            driver.quit()
            return

        driver.get("https://www.coursera.org")
        cargar_cookies(driver)
        driver.refresh()
        time.sleep(2)

        url = input("🔗 Pega la URL de la lección que quieres extraer: ").strip()
        contenido = extraer_contenido(driver, url)

        parsed_url = urlparse(url)
        partes_path = parsed_url.path.strip("/").split("/")
        nombre_clave = "-".join(partes_path[1:]).replace(" ", "-")

        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        os.makedirs("salida_descarga", exist_ok=True)
        archivo = f"salida_descarga/{nombre_clave}_{timestamp}.md"

        with open(archivo, "w", encoding="utf-8") as f:
            f.write(contenido)

        print(f"✅ Contenido guardado en: {archivo}")

    else:
        print("❌ Opción no válida.")

    driver.quit()

if __name__ == "__main__":
    main()
