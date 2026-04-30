#!/usr/bin/env bash

set -e


#======// Startlogik: korrektes Arbeitsverzeichnis sicherstellen //================================//

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
POSAUNE_DIR="$(dirname "$SCRIPT_DIR")"

cd "$POSAUNE_DIR"
echo "Arbeitsverzeichnis: $PWD"


#======// Repository pullen //=====================================================================//

echo "=== Repository herunterladen ==="

# Repository überprüfen
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "Die Installation von Posaune ist unvollständig. Bitte leere das Verzeichnis und installiere das Repository erneut."
    exit 1
fi

git reset --hard
git pull


#======// Pakete überprüfen //========================================================================//

# venv überprüfen
if [ ! -d "venv" ] || [ ! -f "venv/bin/activate" ]; then
    echo "Die Installation von Posaune ist unvollständig. Bitte leere das Verzeichnis und installiere das Repository erneut."
    exit 1
fi

source venv/bin/activate

echo "=== Pip aktualisieren ==="
python3 -m pip install --upgrade pip

echo "=== Installiere/aktualisiere benötigte Pakete ==="
python3 -m pip install -r requirements.txt


#======// Server //==============================================================================//

echo "=== Starte Flask-Server ==="

python3 main.py &

FLASK_PID=$!

#======// Website öffnen //========================================================================//

echo "=== Öffne Browser im Vollbild ==="

chromium --start-fullscreen "http://127.0.0.1:5000" &

echo "=== Setup abgeschlossen ==="
echo "Flask läuft mit PID $FLASK_PID"

wait $FLASK_PID