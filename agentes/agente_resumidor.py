#!/usr/bin/env python3
# agente_resumidor.py

import openai
from config import OPENAI_API_KEY, MODELO_OPENAI


class AgenteResumidor:
    """Agente que genera resúmenes técnicos amplios, claros y estructurados para apoyar exposiciones o clases."""

    openai.api_key = OPENAI_API_KEY

    @staticmethod
    def resumir_contenido(texto_original, titulo):
        """Genera un resumen técnico amplio basado en el contenido proporcionado."""

        if not texto_original or not texto_original.strip():
            print("ADVERTENCIA: El texto de entrada está vacío o es inválido.")
            return None

        prompt = (
            f"""
Genera un resumen bien estructurado del siguiente contenido de una transcripción.
TÍTULO: {titulo}
TRANSCRIPCIÓN:
{texto_original}
📌 Instrucciones:
- Incluye el **título una sola vez** como encabezado Markdown, en el formato: `# [emoji] {titulo}`
- Divide el contenido en secciones temáticas si aplica, usando subtítulos con formato Markdown (`##`) y emojis relevantes.
- Conserva el **tono explicativo original**. No lo simplifiques en exceso.
- **Evita repetir ideas o frases ya expresadas**. Resume de forma clara, sin redundancias.
- **Crea ejemplos relevantes cuando no existan en el texto**. Cada sección técnica debe incluir:
  - **Un ejemplo básico** y **uno avanzado de nivel profesional **.
  - **Preferentemente con código cuando aplique** (en Python, usando buenas prácticas).
  - Si no aplica código python utiliza la herramienta que creas que se debe utilizar de acuerdo al contenito.
- Los ejemplos deben estar en **párrafos explicativos completos**, e incluir bloques de código si corresponde.
- Si el contenido lo permite, agrega **sugerencias prácticas, subtemas relevantes o ideas que amplíen la información** original.

✅ Formato de salida:
- Solo **texto plano**. No usar Canvas ni formato enriquecido.
- Usa sintaxis Markdown visible: `#`, `##`, `*`, `-`, y triple backtick para bloques de código (```python).
- Usa **emojis apropiados** en títulos o subtítulos.
- No dejes **espacios en blanco innecesarios** entre secciones o bloques.
- El contenido debe estar **listo para guardarse como archivo `.md` sin edición adicional**.
- El resultado debe poder **copiarse y pegarse directamente**, manteniendo el formato Markdown.

        """
        )
        sytem_prompt = f"""
 Actúa como un asistente experto en gestión del conocimiento. Quiero que transformes el siguiente texto en una nota **conceptual**, escrita en un formato claro y útil para repaso en Obsidian.
 Aplica las siguientes reglas:

 1. Resume con lenguaje neutro, sin tono personal ni institucional.
 2. Destaca los **conceptos clave** y su aplicación práctica.
 3. Utiliza encabezados en estilo Markdown (`#`, `##`) para estructurar la nota.
 4. Omite frases promocionales, redundancias y llamadas a la acción innecesarias.
"""
        try:
            respuesta = openai.chat.completions.create(
                model=MODELO_OPENAI,
                messages=[
                    {"role": "system", "content": sytem_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4,
                max_tokens=1300
            )

            resumen = respuesta.choices[0].message.content.strip()
            print("OK: Resumen técnico amplio generado exitosamente.")
            return resumen

        except Exception as e:
            print(f"ERROR: Fallo al generar el resumen. Detalle: {e}")
            return None
