#!/usr/bin/env bash

set -e

mkdir -p posaune

cd posaune


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


#======// Repository klonen //=====================================================================//

echo "=== Repository herunterladen ==="

REPO_URL="https://github.com/Operators-Diaries/posaune.git"

echo "Clone Repository"
git clone "$REPO_URL" .


#======// Environment //==========================================================================//

echo "=== Virtual Environment erstellen ==="

python3 -m venv venv

bash scripts/start.sh