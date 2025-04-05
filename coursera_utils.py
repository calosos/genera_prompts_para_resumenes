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


def crear_driver():
    try:
        return webdriver.Chrome(service=Service(CHROME_DRIVER_PATH))
    except Exception as e:
        print(f"❌ Error al crear el driver de Chrome: {e}")
        raise


def guardar_cookies(driver):
    try:
        cookies = driver.get_cookies()
        with open(COOKIES_FILE, "w") as f:
            json.dump(cookies, f)
        print("✅ Cookies guardadas correctamente.")
    except Exception as e:
        print(f"❌ Error al guardar cookies: {e}")


def cargar_cookies(driver):
    try:
        with open(COOKIES_FILE, "r") as f:
            cookies = json.load(f)
            for cookie in cookies:
                driver.add_cookie(cookie)
    except Exception as e:
        print(f"❌ Error al cargar cookies: {e}")


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
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
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
    try:
        driver.get(url)
        time.sleep(5)
        cerrar_modal_traduccion(driver)
        expandir_secciones(driver)
        time.sleep(2)
        contenido = driver.find_element(By.TAG_NAME, "main").text
        return contenido
    except Exception as e:
        return f"⚠️ No se pudo extraer el contenido: {e}"


def generar_nombre_archivo(url):
    try:
        parsed_url = urlparse(url)
        partes_path = parsed_url.path.strip("/").split("/")
        nombre_clave = "-".join(partes_path[1:]).replace(" ", "-")
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        return f"salida_descarga/{nombre_clave}_{timestamp}.md"
    except Exception as e:
        print(f"❌ Error al generar nombre de archivo: {e}")
        return "salida_descarga/contenido_descargado.md"
