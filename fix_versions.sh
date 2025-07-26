#!/bin/bash

echo "🔍 Buscando manifests con versiones inválidas..."

# Buscar todos los manifests
find ~/odoo/custom_addons -type f -name '__manifest__.py' | while read -r file; do
  if grep -q "'version': '16.0" "$file"; then
    echo "🛠 Corrigiendo versión en: $file"
    sed -i "s/'version': '16.0/'version': '18.0/" "$file"
  fi
done

echo "✅ Todos los manifests fueron corregidos."
