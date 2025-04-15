from procesador_archivo_md import (
    limpiar_contenido,
    guardar_contenido_limpio,
    mostrar_subtitulos_detectados,
    cargar_subtitulos_json,
    aplicar_jerarquia,
    guardar_archivo_modificado
)
from genera_prompts_desde_archivo import generar_prompts_desde_archivo
from generador_script_nombres import generar_script_nombres, normalizar_nombre


def procesar_archivo_guardado(nombre_archivo_original):
    # 1. Limpiar el contenido original
    contenido_limpio = limpiar_contenido(nombre_archivo_original)
    if contenido_limpio is None:
        return

    # 2. Guardar contenido limpio
    nombre_procesado = guardar_contenido_limpio(nombre_archivo_original, contenido_limpio)

    # 3. Mostrar subtítulos detectados
    mostrar_subtitulos_detectados()

    input("\nPresiona Enter cuando estés listo para aplicar la jerarquía...")

    # 4. Aplicar jerarquía
    subtitulos_actualizados = cargar_subtitulos_json()
    contenido_final = aplicar_jerarquia(contenido_limpio, subtitulos_actualizados)

    # 5. Guardar archivo jerarquizado
    ruta_salida = guardar_archivo_modificado(nombre_procesado, contenido_final)

    # 6. Permitir edición manual
    print('*'*50)
    print(f"\n📝 Puedes editar manualmente el archivo generado si lo deseas: \n")
    print('*' * 50)
    print(f"📄 Archivo jerarquizado: {ruta_salida}")
    input("✏️ Abre el archivo ahora. Presiona Enter cuando hayas terminado de editar...")

    # 7. Mostrar contenido editado
    print("\n📄 Contenido actual del archivo editado:\n" + "-"*50)
    with open(ruta_salida, "r", encoding="utf-8") as f:
        print(f.read())
    print("-"*50)

    # 8. Confirmar y generar script de nombres
    confirmar = input("¿Está correcto el contenido del archivo? (s/n): ").strip().lower()
    if confirmar == "s":
        base_id = input("🔢 Ingresa el identificador base (por ejemplo 3): ").strip()
        letra_modulo = input("🔠 Ingresa la letra del módulo (por ejemplo a): ").strip()

        # Obtener el nombre del módulo como nombre del archivo .sh
        titulo_principal = contenido_final.splitlines()[0].replace("# ", "").strip()
        nombre_script = f"{normalizar_nombre(titulo_principal)}.sh"

        generar_script_nombres(ruta_salida, base_id, letra_modulo, nombre_script=nombre_script)

    else:
        print("ℹ️ No se generó el archivo .sh porque no se confirmó la edición.")

    # 9. Generar prompts
    print("\n📚 Generando prompts a partir del archivo procesado...")
    generar_prompts_desde_archivo(ruta_salida)
