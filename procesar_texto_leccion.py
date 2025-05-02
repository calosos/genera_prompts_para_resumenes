import re


def obten_titulo(texto):
    """
    Extrae el título principal de una lección de Coursera en inglés o español.
    Busca después de frases como 'Play Video for' o 'Reproducir video para'.
    """
    lineas = texto.splitlines()

    for linea in lineas:
        # Frases típicas donde aparece el título
        if "Play Video for" in linea:
            return linea.replace("Play Video for", "").strip()
        elif "Reproducir video para" in linea:
            return linea.replace("Reproducir video para", "").strip()

    # fallback: si no se encuentra nada, intenta con una heurística
    for linea in lineas:
        if re.match(r"^[A-Z][a-z]+(\s+[A-Z][a-z]+)+$", linea.strip()):
            return linea.strip()

    return "titulo_desconocido"


def extraer_transcripcion(texto):
    """
    Extrae la transcripción desde la primera línea con timestamp (ej. '0:00'),
    elimina encabezados innecesarios y remueve frases finales como 'Me gusta', 'Compartir', 'Like', etc.
    """
    lineas = texto.splitlines()
    resultado = []
    capturando = False

    patron_timestamp = re.compile(r"^\d{1,2}:\d{2}$")
    basura_final = {"me gusta", "no me gusta", "compartir", "like", "dislike", "share"}

    for i in range(len(lineas)):
        linea = lineas[i].strip()

        if not capturando:
            if patron_timestamp.match(linea) and i + 1 < len(lineas):
                siguiente = lineas[i + 1].strip()
                if siguiente and re.search(r"[a-zA-Z]", siguiente):
                    capturando = True
                    resultado.append(linea)
        elif capturando:
            resultado.append(linea)

    # Elimina todas las líneas basura finales si coinciden con frases conocidas
    while resultado and resultado[-1].strip().lower() in basura_final:
        resultado.pop()

    return "\n".join(resultado).strip()


# Uso directo
if __name__ == "__main__":
    with open("contenido_crudo.txt", "r", encoding="utf-8") as f:
        texto = f.read()

    transcripcion = extraer_transcripcion(texto)

    with open("transcripcion_limpia.md", "w", encoding="utf-8") as f:
        f.write(transcripcion)

    print("✅ Transcripción limpia guardada en 'transcripcion_limpia.md'")
