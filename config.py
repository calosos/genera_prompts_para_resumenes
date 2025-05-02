from pathlib import Path
import os
from gestor_entorno_openai import GestorEntornoOpenAI

# --- Validar entorno y cargar API key ---
gestor = GestorEntornoOpenAI(env_filename=".env", nombre_variable="OPENAI_API_KEY", prefijo_valido="sk-")
if not gestor.preparar_entorno():
    raise EnvironmentError("Deteniendo ejecución: Problemas detectados en el entorno o la API key.")

OPENAI_API_KEY = gestor.api_key

# --- Carpetas de trabajo ---
BASE_DIR = Path(__file__).resolve().parent

CARPETA_RESUMENES = BASE_DIR / "resumenes_generados"

# --- Parámetros del modelo OpenAI ---
MODELO_OPENAI = "gpt-4o-mini"  # Elegido para rapidez y costo

# --- Otros parámetros ---
LONGITUD_PROMPT_RESUMEN = 300
MAX_TEXTO_PUBLICACION = 700
ENCODING = "utf-8"