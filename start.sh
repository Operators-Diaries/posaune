#!/usr/bin/env bash

set -e

# Repository
echo "=== Repository herunterladen ==="

REPO_URL="https://github.com/Operators-Diaries/posaune.git"
TARGET_DIR="posaune"

if [ -d "$TARGET_DIR" ]; then
    echo "Repository existiert bereits – ziehe Updates"
    git -C "$TARGET_DIR" pull
else
    echo "Clone Repository"
    git clone "$REPO_URL" "$TARGET_DIR"
fi

# Python Installation
echo "=== Prüfe Python-Installation ==="

if ! command -v python3 &> /dev/null; then
    echo "Python3 nicht gefunden. Installation wird versucht..."

    sudo apt update
    sudo apt install -y python3 python3-pip

else
    echo "Python3 gefunden: $(python3 --version)"
fi

# Pip
echo "=== Stelle sicher, dass pip aktuell ist ==="
python3 -m pip install --upgrade pip

# Requirements
echo "=== Installiere/aktualisiere benötigte Pakete ==="

REQUIRED_PACKAGES=(
    flask
    requests
    gunicorn
)

python3 -m pip install -r requirements.txt

echo "=== Starte Flask-Server ==="

cd "$TARGET_DIR"

python3 app.py &

FLASK_PID=$!

sleep 3


echo "=== Öffne Browser im Vollbild ==="

URL="http://127.0.0.1:5000"

if command -v chromium &> /dev/null; then
    chromium --start-fullscreen "$URL" &
elif command -v google-chrome &> /dev/null; then
    google-chrome --start-fullscreen "$URL" &
elif command -v firefox &> /dev/null; then
    firefox --kiosk "$URL" &
else
    echo "Kein unterstützter Browser gefunden"
fi


echo "=== Setup abgeschlossen ==="
echo "Flask läuft mit PID $FLASK_PID"

wait $FLASK_PID