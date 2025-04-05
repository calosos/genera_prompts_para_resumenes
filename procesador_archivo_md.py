import os
import re
import json

def cargar_archivo(nombre_archivo):
    if not os.path.exists(nombre_archivo):
        print(f"❌ Archivo no encontrado: {nombre_archivo}")
        return None
    with open(nombre_archivo, "r", encoding="utf-8") as f:
        return f.read()

def guardar_archivo_modificado(nombre_original, contenido_modificado):
    try:
        os.makedirs("salida_procesados", exist_ok=True)
        nombre_base = os.path.basename(nombre_original)
        nuevo_nombre = f"procesado_{nombre_base.replace('.txt', '').replace('.md', '')}.md"
        ruta_salida = os.path.join("salida_limpia", nuevo_nombre)
        with open(ruta_salida, "w", encoding="utf-8") as f:
            f.write(contenido_modificado)
        print(f"\n✅ Archivo procesado guardado en: {ruta_salida}")
    except Exception as e:
        print(f"❌ Error al guardar el archivo procesado: {e}")

def cargar_subtitulos_json(ruta="subtitulos.json"):
    if not os.path.exists(ruta):
        print(f"⚠️ Archivo de subtítulos no encontrado: {ruta}")
        return []
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)

def aplicar_jerarquia(contenido, subtitulos):
    lineas = contenido.splitlines()
    resultado = []
    actual_es_subtitulo = False

    for linea in lineas:
        texto = linea.strip()
        if texto in subtitulos:
            resultado.append(f"## {texto}")
            actual_es_subtitulo = True
        elif actual_es_subtitulo and texto:
            resultado.append(f"### {texto}")
        else:
            resultado.append(texto)
            actual_es_subtitulo = False

    return "\n".join(resultado)

def procesar_contenido(contenido):
    lineas = contenido.splitlines()
    if not lineas:
        return ""

    lineas[0] = "# " + lineas[0].lstrip("#").strip()

    try:
        idx_corte = next(i for i, l in enumerate(lineas) if l.strip() == "Ocultar objetivos de aprendizaje")
        lineas = [lineas[0]] + lineas[idx_corte + 1:]
    except StopIteration:
        print("ℹ️ 'Ocultar objetivos de aprendizaje' no encontrado. Se conserva el contenido completo.")

    patrones = [
        r"^Vídeo.*$",
    r"^\d* .*$",
    r"^. Duration: \d* .+$",
    r"^Lectura•$",
    r"^Completado$",
    r"^Reanudar$",
    r"^Calificado$",
    r"^Cuestionario•\d.* preguntas$",
    r"^Complemento no calificado•$",
    r"^•Calificación:.*$",
    r"^Guía de estudio\: .*$",
    r"^Revisión\:.*$",
    r"^. Haz clic para reanudar\.$",
    r"^Cuestionario pr.ctico\: .*$",
    r"^Tarea de práctica•.*$",
    r"^Tarea calificada•.*$",
    r"^Vence el \d* de \w*. .*$",
    r"^laboratorio•$"

    ]

    try:
        idx_crono = next(i for i, l in enumerate(lineas) if l.strip() == "Cronograma del curso")
        lineas = lineas[:idx_crono]
    except StopIteration:
        pass

    return "\n".join([l for l in lineas if not any(re.fullmatch(pat, l.strip()) for pat in patrones)])

def limpiar_contenido(nombre_archivo_original):
    contenido = cargar_archivo(nombre_archivo_original)
    if contenido is None:
        return None
    return procesar_contenido(contenido)

def guardar_contenido_limpio(nombre_archivo_original, contenido_limpio):
    nombre_procesado = nombre_archivo_original.replace("salida_descarga", "salida_procesados")
    os.makedirs(os.path.dirname(nombre_procesado), exist_ok=True)
    with open(nombre_procesado, "w", encoding="utf-8") as f:
        f.write(contenido_limpio)
    print(f"✅ Contenido limpio guardado en: {nombre_procesado}")
    return nombre_procesado

def mostrar_subtitulos_detectados():
    subtitulos = cargar_subtitulos_json()
    print("\n📌 Puedes editar el archivo 'subtitulos.json' si deseas ajustar los encabezados.")
    print("📄 Subtítulos detectados actualmente:")
    for st in subtitulos:
        print(f"- {st}")
    return subtitulos
