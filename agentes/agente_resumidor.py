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
            f"""Eres un asistente especializado en generar resúmenes técnicos claros, estructurados y amplios para apoyar exposiciones o clases.\n\n"
Genera una resumen sobre el tema: {titulo}
TEXTO A RESUMIR:
{texto_original}
\n📌 Asegúrate de incluir **al menos un ejemplo básico y uno avanzado a un nivel profesional** en cada sección técnica.
📌 Conserva todo el código y usa la librería de openai 
---

✅ El formato de salida debe cumplir los siguientes criterios:
- Recuerda conservar todo el código
- En **texto plano** (no usar canvas ni formato enriquecido)  
- Con **sintaxis Markdown visible** (`#`, `*`, `-`, ```python)  
- Con **emojis apropiados** en títulos o viñetas  
- El resultado debe poder **copiarse y pegarse directamente** sin perder el formato Markdown

📌 El contenido debe estar **estructurado**, **legible** y listo para guardarse como `.md` sin edición adicional.
        """
        )

        try:
            respuesta = openai.chat.completions.create(
                model=MODELO_OPENAI,
                messages=[
                    {"role": "system", "content": "Eres un asistente experto en generar resúmenes técnicos amplios para clases y exposiciones."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4,
                max_tokens=1000
            )

            resumen = respuesta.choices[0].message.content.strip()
            print("OK: Resumen técnico amplio generado exitosamente.")
            return resumen

        except Exception as e:
            print(f"ERROR: Fallo al generar el resumen. Detalle: {e}")
            return None
