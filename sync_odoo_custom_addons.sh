#!/bin/bash

# === CONFIGURACIÓN ===
REPO_DIR="/home/asba/odoo"
BRANCH="18.0"
REMOTE="origin"
TARGET_DIR="custom_addons"

# === FUNCIÓN DE LOG ===
log() {
    echo -e "\033[1;32m[INFO]\033[0m $1"
}
warn() {
    echo -e "\033[1;33m[WARN]\033[0m $1"
}
error() {
    echo -e "\033[1;31m[ERROR]\033[0m $1"
}

# === INICIAR ===
cd "$REPO_DIR" || { error "No se pudo acceder a $REPO_DIR"; exit 1; }

# Asegurar que estamos en la rama correcta
git checkout $BRANCH > /dev/null || { error "No se pudo cambiar a la rama $BRANCH"; exit 1; }

log "Obteniendo últimos cambios desde $REMOTE/$BRANCH..."
git fetch $REMOTE $BRANCH

# Compara diferencias entre la rama local y remota, SOLO en custom_addons
CHANGED_FILES=$(git diff --name-only HEAD..$REMOTE/$BRANCH -- "$TARGET_DIR")

if [ -n "$CHANGED_FILES" ]; then
    log "Detectados cambios en '$TARGET_DIR':"
    echo "$CHANGED_FILES"
    
    read -p "¿Deseas actualizar '$TARGET_DIR' con los cambios remotos? (s/n): " RESPUESTA
    if [[ "$RESPUESTA" == "s" || "$RESPUESTA" == "S" ]]; then
        log "Descargando solo los cambios en '$TARGET_DIR'..."

        # Guarda los cambios actuales por si acaso
        git stash push -m "Respaldo antes de actualizar $TARGET_DIR" "$TARGET_DIR"

        # Extrae sólo esa carpeta desde remoto
        git checkout $REMOTE/$BRANCH -- "$TARGET_DIR"

        log "'$TARGET_DIR' actualizado desde $REMOTE/$BRANCH"
    else
        warn "Sincronización cancelada por el usuario."
    fi
else
    log "No hay cambios remotos en '$TARGET_DIR'. Nada que hacer."
fi

