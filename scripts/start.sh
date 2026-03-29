#!/usr/bin/env bash

set -e

#======// Startlogik: korrektes Arbeitsverzeichnis sicherstellen //================================//

TARGET_NAME="posaune"

if [[ -n "${BASH_SOURCE[0]}" && -f "${BASH_SOURCE[0]}" ]]; then
    # Skript liegt als Datei vor -> Ordner der Datei ist das Ziel
    WORK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
else
    # Skript läuft gepiped -> aktuelles Verzeichnis ist der Ausgangspunkt
    if [[ "$(basename "$PWD")" == "$TARGET_NAME" ]]; then
        WORK_DIR="$PWD"
    else
        WORK_DIR="$PWD/$TARGET_NAME"
        mkdir -p "$WORK_DIR"
    fi
fi

cd "$WORK_DIR"
echo "Arbeitsverzeichnis: $PWD"


#======// Python, Git & Chromium sicherstellen //==================================================//

echo "=== Prüfe Installationen ==="

if command -v python3 &> /dev/null && command -v git &> /dev/null && python3 -m pip --version &> /dev/null && python3 -m venv --version &> /dev/null && command -v chromium &> /dev/null; then
    echo "Python: $(python3 --version)"
    echo "Git: $(git --version)"
    echo "Pip: $(python3 -m pip --version)"
    echo "Venv: $(python3 -m venv --version)"
    echo "Chromium: $(chromium --version)"
else
    echo "Mindestens eine Installation fehlt"
    echo "=== Prüfe Paketmanager ==="

    if command -v apt &> /dev/null; then
        sudo apt update
        sudo apt install -y python3 python3-pip git python3.12-venv chromium

    elif command -v dnf &> /dev/null; then
        sudo dnf install -y python3 python3-pip git python3.12-venv chromium

    elif command -v pacman &> /dev/null; then
        sudo pacman -Sy --noconfirm python python-pip git python3.12-venv chromium

    else
        echo "Kein unterstützter Paketmanager gefunden"
        exit 1
    fi

fi

#======// Repository pullen //=====================================================================//

echo "=== Repository herunterladen ==="

REPO_URL="https://github.com/Operators-Diaries/posaune.git"

if [ -d ".git" ]; then
    echo "Repository existiert bereits – ziehe Updates"
    git reset --hard
    git pull
else
    echo "Clone Repository"
    git clone "$REPO_URL" .
fi


#======// Requirements //========================================================================//

echo "=== Virtual Environment erstellen ==="

python3 -m venv venv
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

URL="http://127.0.0.1:5000"

chromium --start-fullscreen "$URL" &

echo "=== Setup abgeschlossen ==="
echo "Flask läuft mit PID $FLASK_PID"

wait $FLASK_PID