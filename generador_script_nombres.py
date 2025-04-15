import os
import unicodedata
from pathlib import Path

def normalizar_nombre(texto):
    """
    Convierte un texto en un nombre de archivo válido:
    - Sin acentos
    - Sin caracteres especiales
    - Con guiones bajos en lugar de espacios
    """
    texto = unicodedata.normalize("NFKD", texto).encode("ASCII", "ignore").decode("utf-8")
    texto = texto.replace(" ", "_")
    texto = ''.join(c for c in texto if c.isalnum() or c == '_')
    return texto


def generar_script_nombres(ruta_archivo_md, base_id, letra_modulo, carpeta_salida="salida_crea_archivos", nombre_script="generar_archivos.sh"):
    """
    Lee un archivo Markdown jerarquizado y genera un script .sh con nombres
    estructurados según jerarquía.

    base_id: número base (por ejemplo 3)
    letra_modulo: letra para representar el módulo (por ejemplo 'a')
    carpeta_salida: carpeta donde se guarda el script
    nombre_script: nombre del archivo script generado
    """
    with open(ruta_archivo_md, "r", encoding="utf-8") as f:
        lineas = f.readlines()

    Path(carpeta_salida).mkdir(parents=True, exist_ok=True)
    salida_script = Path(carpeta_salida) / nombre_script

    script_lines = []
    modulo_idx = 0
    subtema_idx = 0

    for linea in lineas:
        if linea.startswith("## "):
            modulo_idx += 1
            subtema_idx = 0
            titulo = linea.replace("## ", "").strip()
            nombre_archivo = f"{base_id}{letra_modulo}{modulo_idx}_{normalizar_nombre(titulo)}.md"
            script_lines.append(f"touch {nombre_archivo}")
        elif linea.startswith("### "):
            subtema_idx += 1
            letra_subtema = chr(96 + subtema_idx)  # 1 -> a, 2 -> b, etc.
            titulo = linea.replace("### ", "").strip()
            nombre_archivo = f"{base_id}{letra_modulo}{modulo_idx}{letra_subtema}_{normalizar_nombre(titulo)}.md"
            script_lines.append(f"touch {nombre_archivo}")

    salida_script.write_text("\n".join(script_lines), encoding="utf-8")

    print(f"✅ Script generado con {len(script_lines)} líneas en: {salida_script}")
    return salida_script
