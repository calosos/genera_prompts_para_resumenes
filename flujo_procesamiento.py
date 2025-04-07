from procesador_archivo_md import (
    limpiar_contenido,
    guardar_contenido_limpio,
    mostrar_subtitulos_detectados,
    cargar_subtitulos_json,
    aplicar_jerarquia,
    guardar_archivo_modificado
)
from genera_prompts_desde_archivo import generar_prompts_desde_archivo


def procesar_archivo_guardado(nombre_archivo_original):
    contenido_limpio = limpiar_contenido(nombre_archivo_original)
    if contenido_limpio is None:
        return

    nombre_procesado = guardar_contenido_limpio(nombre_archivo_original, contenido_limpio)
    mostrar_subtitulos_detectados()

    input("\nPresiona Enter cuando estés listo para aplicar la jerarquía...")

    subtitulos_actualizados = cargar_subtitulos_json()
    contenido_final = aplicar_jerarquia(contenido_limpio, subtitulos_actualizados)

    ruta_salida = guardar_archivo_modificado(nombre_procesado, contenido_final)

    print(f"✅ Archivo jerarquizado guardado en: {nombre_procesado}")

    print("\n📚 Generando prompts a partir del archivo procesado...")
    generar_prompts_desde_archivo(ruta_salida)

