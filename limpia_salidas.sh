#!/bin/bash

# Script para limpiar archivos y carpetas de trabajo
# Carlos Ortiz – 2025

# 1. Borrar .md y .sh en carpetas específicas
carpetas=(
  "salida_crea_archivos"
  "salida_descarga"
  "salida_limpia"
  "salida_procesados"
  "resumenes_generados"
)

for carpeta in "${carpetas[@]}"; do
  echo "🧹 Limpiando archivos .md y .sh en: $carpeta"
  find "$carpeta" -type f \( -name "*.md" -o -name "*.sh" \) -exec rm -f {} \;
done

# 2. Mantener solo las 3 subcarpetas más recientes en prompts_generados
echo "🧹 Limpiando subcarpetas antiguas en prompts_generados (manteniendo 3 más recientes)..."

subcarpetas=( $(find prompts_generados/* -maxdepth 0 -type d -printf "%T@ %p\n" | sort -n | awk '{print $2}') )

total=${#subcarpetas[@]}
a_borrar=$((total - 3))

if [ $a_borrar -gt 0 ]; then
  for ((i=0; i<a_borrar; i++)); do
    echo "   ❌ Eliminando: ${subcarpetas[$i]}"
    rm -rf "${subcarpetas[$i]}"
  done
else
  echo "   ✅ Menos de 4 subcarpetas, no se elimina ninguna."
fi

echo "✅ Limpieza general completada."
