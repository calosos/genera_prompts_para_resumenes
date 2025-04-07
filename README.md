# 📘 Proyecto: Descarga, Procesamiento y Generación de Prompts desde Coursera

Este proyecto automatiza la descarga de contenido desde Coursera y genera prompts en formato Markdown a partir de la estructura jerarquizada del contenido de las lecciones.

---

## 🚀 ¿Qué hace este proyecto?

1. Inicia sesión en Coursera (manual) y guarda cookies para futuras sesiones.
2. Descarga el contenido HTML de una lección seleccionada.
3. Limpia el contenido eliminando líneas innecesarias (duraciones, botones, etiquetas).
4. Permite editar subtítulos que definen la jerarquía de secciones.
5. Aplica estructura Markdown jerarquizada a partir de esos subtítulos.
6. Genera archivos `.md` con prompts para crear cheat sheets a partir del contenido estructurado.

---

## 🧰 Requisitos

- Python 3.8+
- Google Chrome
- ChromeDriver (https://chromedriver.chromium.org/)
- Paquetes: selenium

Instalación de dependencias:

```bash
pip install -r requirements.txt
```

---

## 🧑‍💻 ¿Cómo usarlo?

Ejecuta el script principal:

```bash
python main.py
```

Elige una opción:

    1: Iniciar sesión manual en Coursera y guardar cookies.
    2: Usar cookies y pegar la URL de una lección para procesarla.

Revisa y edita `subtitulos.json` si deseas cambiar la jerarquía de secciones.

Presiona Enter para aplicar la jerarquía y generar los prompts.

---

## 🧱 Estructura de carpetas

```
descarga_info/
├── main.py
├── coursera_utils.py
├── flujo_procesamiento.py
├── procesador_archivo_md.py
├── genera_prompts_desde_archivo.py
├── subtitulos.json
├── salida_descarga/
├── salida_procesados/
├── salida_limpia/
├── prompts_generados/
```

---

## 📊 Diagrama del flujo del sistema

```
┌────────────────────┐
│ Usuario elige opción│
└────────┬───────────┘
         ▼
┌──────────────────────────────┐
│ Opción 1: Login manual       │
│  ↳ Guarda cookies en JSON    │
└────────────┬────────────────┘
             │
             ▼
┌──────────────────────────────┐
│ Opción 2: Cargar cookies      │
│  ↳ Pide URL de lección        │
└────────────┬────────────────┘
             ▼
┌──────────────────────────────┐
│ Extrae contenido del sitio   │
│ Guarda en salida_descarga/  │
└────────────┬────────────────┘
             ▼
┌──────────────────────────────┐
│ Limpieza del contenido       │
│  ↳ Elimina basura            │
│  ↳ Guarda limpio             │
│    en salida_procesados/     │
└────────────┬────────────────┘
             ▼
┌──────────────────────────────┐
│ Muestra subtítulos actuales  │
│ Espera edición manual        │
└────────────┬────────────────┘
             ▼
┌──────────────────────────────┐
│ Aplica jerarquía Markdown    │
│ Guarda archivo final         │
└────────────┬────────────────┘
             ▼
┌──────────────────────────────┐
│ Genera prompts Markdown      │
│ Guarda en prompts_generados/ │
└──────────────────────────────┘
```

---

## ✍️ Personalización

- Edita el archivo `subtitulos.json` para definir los títulos o secciones que deben convertirse en `##` o `###`.
- Puedes modificar `procesador_archivo_md.py` o `genera_prompts_desde_archivo.py` para ajustar el formato de jerarquía o los prompts generados.

---

## 🛡️ Licencia

Este proyecto es de uso libre para propósitos educativos o personales.

---

## 🤝 Contribuciones

¡Sugerencias, mejoras o PRs son bienvenidos!
