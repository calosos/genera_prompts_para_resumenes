import os
import re
import sys


def cargar_archivo(nombre_archivo):
    if not os.path.exists(nombre_archivo):
        print(f"❌ Archivo no encontrado: {nombre_archivo}")
        return None
    with open(nombre_archivo, "r", encoding="utf-8") as f:
        return f.read()


def guardar_archivo_modificado(nombre_original, contenido_modificado):
    os.makedirs("salida_procesados", exist_ok=True)

    nombre_base = os.path.basename(nombre_original)
    nuevo_nombre = f"procesado_{nombre_base.replace('.txt', '').replace('.md', '')}.md"
    ruta_salida = os.path.join("salida_procesados", nuevo_nombre)

    with open(ruta_salida, "w", encoding="utf-8") as f:
        f.write(contenido_modificado)

    print(f"\n✅ Archivo procesado guardado en: {ruta_salida}")


def procesar_contenido(contenido):
    lineas = contenido.splitlines()
    if not lineas:
        return ""

    # Convertir primera línea a título
    lineas[0] = "# " + lineas[0].lstrip("#").strip()

    # Eliminar desde línea 1 hasta "Ocultar objetivos de aprendizaje", solo si existe
    try:
        idx_corte = next(
            i for i, linea in enumerate(lineas)
            if re.fullmatch(r"Ocultar objetivos de aprendizaje", linea.strip())
        )
        # Aplicar corte solo si la expresión fue encontrada
        lineas = [lineas[0]] + lineas[idx_corte + 1:]
        # if len(lineas) > 1:
        #     lineas[1] = "## " + lineas[1].lstrip("#").strip()
    except StopIteration:
        print("ℹ️ 'Ocultar objetivos de aprendizaje' no encontrado. Se conserva el contenido completo.")

    # Reglas para eliminar solo líneas individuales
    patrones_a_eliminar = [
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
        r"^laboratorio•$",

    ]

    # Cortar todas las líneas posteriores a "Cronograma del curso" si existe
    try:
        idx_cronograma = next(
            i for i, linea in enumerate(lineas)
            if re.fullmatch(r"Cronograma del curso", linea.strip())
        )
        lineas = lineas[:idx_cronograma]
    except StopIteration:
        pass  # Si no se encuentra, no se hace nada

    lineas_filtradas = []
    for linea in lineas:
        if any(re.fullmatch(pat, linea.strip()) for pat in patrones_a_eliminar):
            continue
        lineas_filtradas.append(linea)

    return "\n".join(lineas_filtradas)


def main():
    if len(sys.argv) < 2:
        print("❌ Debes pasar el nombre del archivo como argumento.")
        print("📌 Ejemplo: python limpiar_contenido.py archivo.md")
        return

    nombre_archivo = sys.argv[1]
    contenido = cargar_archivo(nombre_archivo)

    if contenido is None:
        return

    contenido_procesado = procesar_contenido(contenido)

    guardar_archivo_modificado(nombre_archivo, contenido_procesado)

    # print("\n--- Vista previa (primeras 10 líneas) ---\n")
    # for i, linea in enumerate(contenido_procesado.splitlines()):
    #     if i >= 10:
    #         break
    #     print(linea)


if __name__ == "__main__":
    main()