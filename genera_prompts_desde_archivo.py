import os
import re


def extraer_titulo_principal(lineas):
    for linea in lineas:
        if linea.startswith("# "):
            return linea.strip().replace("# ", "")
    return None


def sanitizar_nombre(texto):
    return re.sub(r'[^a-zA-Z0-9_]', '', texto.replace(" ", "_").lower())


def extraer_temas_y_subtemas(lineas):
    temas = []
    tema_actual = None
    for linea in lineas:
        if linea.startswith("## "):
            if tema_actual:
                temas.append(tema_actual)
            tema_actual = {"titulo": linea.strip().replace("## ", ""), "subtemas": []}
        elif linea.startswith("### ") and tema_actual:
            tema_actual["subtemas"].append(linea.strip().replace("### ", ""))
    if tema_actual:
        temas.append(tema_actual)
    return temas


def construir_prompt(titulo, subtemas):
    prompt = f"""Quiero una cheat sheet sobre el tema: {titulo} .

Debe incluir las siguientes secciones en formato Markdown:
"""
    for subtitulo in subtemas:
        prompt += f"\n# {subtitulo}  "
    prompt += """

📌 Estos son los temas mínimos, pero puedes agregar **subtemas relevantes** que enriquezcan el contenido.

📌 Asegúrate de incluir **al menos un ejemplo básico y uno avanzado** en cada sección técnica.

---

✅ El formato de salida debe cumplir los siguientes criterios:

- En **texto plano** (no usar canvas ni formato enriquecido)  
- Con **sintaxis Markdown visible** (`#`, `*`, `-`, ```python)  
- Con **emojis apropiados** en títulos o viñetas  
- El resultado debe poder **copiarse y pegarse directamente** sin perder el formato Markdown

📌 El contenido debe estar **estructurado**, **legible** y listo para guardarse como `.md` sin edición adicional.

📌 Guárdalo como un archivo `.md` y compárteme el archivo directamente 
"""
    return prompt


def generar_prompts_desde_archivo(nombre_archivo):
    with open(nombre_archivo, "r", encoding="utf-8") as f:
        lineas = f.readlines()

    titulo_principal = extraer_titulo_principal(lineas)
    if not titulo_principal:
        print("❌ No se encontró un título principal en el archivo.")
        return

    nombre_carpeta = sanitizar_nombre(titulo_principal)
    carpeta_salida = os.path.join("prompts_generados", nombre_carpeta)
    os.makedirs(carpeta_salida, exist_ok=True)

    temas = extraer_temas_y_subtemas(lineas)

    for i, tema in enumerate(temas, start=1):
        titulo = tema["titulo"]
        subtemas = tema["subtemas"]
        prompt = construir_prompt(titulo, subtemas)

        nombre_archivo_md = f"{i}_{sanitizar_nombre(titulo)}.md"
        ruta_salida = os.path.join(carpeta_salida, nombre_archivo_md)

        with open(ruta_salida, "w", encoding="utf-8") as f:
            f.write(prompt)

    print(f"✅ Se generaron {len(temas)} prompts en formato .md en: {carpeta_salida}/")
