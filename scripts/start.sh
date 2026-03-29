#!/usr/bin/env bash

set -e


#======// Startlogik: korrektes Arbeitsverzeichnis sicherstellen //================================//

TARGET_NAME="posaune"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORK_DIR="$(dirname "$SCRIPT_DIR")"

cd "$WORK_DIR"
echo "Arbeitsverzeichnis: $PWD"


#======// Repository pullen //=====================================================================//

echo "=== Repository herunterladen ==="

REPO_URL="https://github.com/Operators-Diaries/posaune.git"

git reset --hard
git pull


#======// Requirements //========================================================================//

source venv/bin/activate

echo "=== Pip aktualisieren ==="
python3 -m pip install --upgrade pip

echo "=== Installiere/aktualisiere benötigte Pakete ==="

python3 -m pip install -r requirements.txt


#======// Server //==============================================================================//

echo "=== Starte Flask-Server ==="

python3 main.py &

FLASK_PID=$!

sleep 3


#======// Website öffnen //========================================================================//

echo "=== Öffne Browser im Vollbild ==="

chromium --start-fullscreen "http://127.0.0.1:5000" &

echo "=== Setup abgeschlossen ==="
echo "Flask läuft mit PID $FLASK_PID"

wait $FLASK_PID