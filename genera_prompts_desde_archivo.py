import os
import re


def extraer_titulo_principal(lineas):
    """
    Busca y devuelve el título principal de un archivo Markdown.
    Se asume que es la primera línea que empieza con "# ".
    """
    for linea in lineas:
        if linea.startswith("# "):
            return linea.strip().replace("# ", "")
    return None


def sanitizar_nombre(texto):
    """
    Convierte un texto en un nombre seguro para carpetas o archivos.
    Reemplaza espacios por guiones bajos y elimina caracteres no alfanuméricos.
    """
    return re.sub(r'[^a-zA-Z0-9_]', '', texto.replace(" ", "_").lower())


def extraer_temas_y_subtemas(lineas):
    """
    Extrae temas (##) y subtemas (###) de un archivo Markdown como una lista de diccionarios.
    Cada tema tiene un título y una lista de subtítulos.
    """
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
    """
    Construye un prompt en texto plano para generar una cheat sheet en formato Markdown.
    Incluye el tema principal y los subtemas como secciones.
    """
    prompt = f"""Quiero una cheat sheet sobre el tema: {titulo}.

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


def leer_lineas_desde_archivo(nombre_archivo):
    """
    Lee todas las líneas de un archivo de texto dado y las devuelve como lista.
    """
    with open(nombre_archivo, "r", encoding="utf-8") as f:
        return f.readlines()


def preparar_carpeta_salida(titulo_principal):
    """
    Crea la carpeta de salida para los prompts basándose en el título principal.
    Devuelve la ruta de la carpeta creada.
    """
    nombre_carpeta = sanitizar_nombre(titulo_principal)
    ruta = os.path.join("prompts_generados", nombre_carpeta)
    os.makedirs(ruta, exist_ok=True)
    return ruta


def guardar_prompt_en_archivo(prompt, carpeta_salida, index, titulo):
    """
    Guarda un prompt generado como archivo Markdown numerado y limpio.
    """
    nombre_archivo_md = f"{index}_{sanitizar_nombre(titulo)}.md"
    ruta_salida = os.path.join(carpeta_salida, nombre_archivo_md)
    with open(ruta_salida, "w", encoding="utf-8") as f:
        f.write(prompt)


def generar_prompts_desde_archivo(nombre_archivo):
    """
    Proceso principal: lee un archivo limpio con formato Markdown y genera un prompt .md
    por cada sección de nivel ## encontrada en el archivo.
    """
    lineas = leer_lineas_desde_archivo(nombre_archivo)
    titulo_principal = extraer_titulo_principal(lineas)

    if not titulo_principal:
        print("❌ No se encontró un título principal en el archivo.")
        return

    carpeta_salida = preparar_carpeta_salida(titulo_principal)
    temas = extraer_temas_y_subtemas(lineas)

    for i, tema in enumerate(temas, start=1):
        prompt = construir_prompt(tema["titulo"], tema["subtemas"])
        guardar_prompt_en_archivo(prompt, carpeta_salida, i, tema["titulo"])

    print(f"✅ Se generaron {len(temas)} prompts en formato .md en: {carpeta_salida}/")


# 🎯 Entry point para ejecución independiente
if __name__ == "__main__":
    archivo = input("📄 Ingresa la ruta del archivo .md limpio: ").strip()
    generar_prompts_desde_archivo(archivo)
