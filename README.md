# 📘 Proyecto: Descarga y Procesamiento de Contenido de Coursera

Este proyecto permite automatizar la descarga de contenido de lecciones desde Coursera usando Selenium, limpiar el contenido para eliminar elementos irrelevantes, aplicar una jerarquía basada en subtítulos definidos, y guardar el contenido procesado en formato Markdown limpio.

---

## 🚀 ¿Qué hace este proyecto?

1. Inicia sesión en Coursera (manual) y guarda cookies para futuras sesiones.
2. Descarga el contenido HTML de una lección seleccionada.
3. Limpia el contenido eliminando líneas innecesarias (duraciones, botones, etiquetas).
4. Permite editar subtítulos que definen la jerarquía de secciones.
5. Aplica estructura Markdown jerarquizada a partir de esos subtítulos.
6. Guarda archivos procesados y listos para usar en Obsidian o Markdown viewer.

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

    python main.py

Elige una opción:

    1: Iniciar sesión manual en Coursera y guardar cookies.
    2: Usar cookies y pegar la URL de una lección para procesarla.

Revisa y edita `subtitulos.json` si deseas cambiar la jerarquía de secciones.

Presiona Enter para aplicar la jerarquía y guardar el archivo final.

---

## 🧱 Estructura de carpetas

descarga_info/  
├── main.py                       ← Menú principal e interacción  
├── coursera_utils.py            ← Login, cookies, extracción con Selenium  
├── procesador_archivo_md.py     ← Limpieza y jerarquía del contenido  
├── flujo_procesamiento.py       ← Orquesta la limpieza y procesamiento  
├── subtitulos.json              ← Define los encabezados jerárquicos  
├── salida_descarga/             ← Contenido crudo descargado  
│   └── .placeholder  
├── salida_procesados/           ← Contenido limpio y jerarquizado  
│   └── .placeholder  

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
└──────────────────────────────┘
```

---

## ✍️ Personalización

- Edita el archivo `subtitulos.json` para definir los títulos o secciones que deben convertirse en `##` o `###`.
- Puedes modificar `procesador_archivo_md.py` si deseas cambiar los patrones que se eliminan durante la limpieza.

---

## 🛡️ Licencia

Este proyecto es de uso libre para propósitos educativos o personales.

---

## 🤝 Contribuciones

¡Sugerencias, mejoras o PRs son bienvenidos!
