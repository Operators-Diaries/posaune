#!/usr/bin/env bash

set -e

cd "$TARGET_DIR"

#======// Python & Git sicherstellen //============================================================//

echo "=== Prüfe Installationen ==="

if command -v python3 &> /dev/null && command -v git &> /dev/null && python3 -m pip --version &> /dev/null; then
    echo "Python: $(python3 --version)"
    echo "Git: $(git --version)"
    echo "Pip: $(python3 -m pip --version)"
else
    echo "Mindestens eine Installation fehlt"
    echo "=== Prüfe Paketmanager ==="

    install_python_debian() {
        sudo apt update
        sudo apt install -y python3 python3-pip git
    }

    install_python_fedora() {
        sudo dnf install -y python3 python3-pip git
    }

    install_python_arch() {
        sudo pacman -Sy --noconfirm python python-pip git
    }

    if command -v apt &> /dev/null; then
        install_python_debian

    elif command -v dnf &> /dev/null; then
        install_python_fedora

    elif command -v pacman &> /dev/null; then
        install_python_arch

    else
        echo "Kein unterstützter Paketmanager gefunden"
        exit 1
    fi

fi

#======// Repository pullen //=====================================================================//

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


#======// Requirements //========================================================================//

echo "=== Virtual Environment erstellen ==="
cd "$TARGET_DIR"
python3 -m venv venv
source venv/bin/activate

echo "=== Stelle sicher, dass pip aktuell ist ==="
python3 -m pip install --upgrade pip

echo "=== Installiere/aktualisiere benötigte Pakete ==="

python3 -m pip install -r requirements.txt


#======// Server //==============================================================================//

echo "=== Starte Flask-Server ==="

python3 app.py &

FLASK_PID=$!

sleep 3


#======// Website öffnen //========================================================================//

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