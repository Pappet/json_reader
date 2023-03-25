#!/bin/bash

# Setzen Sie den Namen Ihres Python-Skripts und den gewünschten Befehlsnamen
PYTHON_SCRIPT="main.py"
COMMAND_NAME="json_reader"

# Setzen Sie den Pfad zum Skript und den Zielpfad für den ausführbaren Befehl
SCRIPT_PATH="$(pwd)/${PYTHON_SCRIPT}"
TARGET_PATH="${HOME}/.local/bin/${COMMAND_NAME}"

# Erstellen Sie das Verzeichnis ~/.local/bin, falls es noch nicht existiert
mkdir -p "${HOME}/.local/bin"

# Machen Sie das Skript ausführbar
chmod +x "${PYTHON_SCRIPT}"

# Verschieben Sie das Skript in den $PATH, damit es systemweit verfügbar ist
ln -s "${SCRIPT_PATH}" "${TARGET_PATH}"

echo "Das Skript wurde erfolgreich installiert. Sie können es jetzt mit '${COMMAND_NAME}' ausführen."
