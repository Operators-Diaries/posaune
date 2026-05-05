#!/usr/bin/env bash

set -e

fehler() {
    printf "\e[1;37;41m FEHLER \e[0m %s\n" "$1" 
}
head() {
    printf "\e[1;38;2;255;255;255;48;2;0;191;255m %s \e[0m\n" "$1" 
}
info() {
    printf "\e[1;37;42m INFO \e[0m %s\n" "$1" 
}

mkdir -p posaune

cd posaune


#======// Installationen sicherstellen //==================================================//

head "Prüfe Installationen"

if command -v python3 &> /dev/null && command -v git &> /dev/null && python3 -m pip --version &> /dev/null && python3 -m venv --version &> /dev/null && command -v chromium &> /dev/null; then
    echo "Python: $(python3 --version)"
    echo "Git: $(git --version)"
    echo "Pip: $(python3 -m pip --version)"
    echo "Venv: $(python3 -m venv --version)"
    echo "Chromium: $(chromium --version)"
else
    info "Mindestens eine Installation fehlt"

    if command -v apt &> /dev/null; then
        sudo apt update
        sudo apt install -y python3 python3-pip git python3-venv chromium

    elif command -v dnf &> /dev/null; then
        sudo dnf install -y python3 python3-pip git python3-venv chromium

    elif command -v pacman &> /dev/null; then
        sudo pacman -Sy --noconfirm python python-pip git python3-venv chromium

    else
        fehler "Kein unterstützter Paketmanager gefunden. Bitte installiere apt, dnf oder pacman."
        exit 1
    fi

fi


#======// Repository klonen //=====================================================================//

head "Repository herunterladen"

REPO_URL="https://github.com/Operators-Diaries/posaune.git"

echo "Clone Repository"
git clone "$REPO_URL" .


#======// Environment //==========================================================================//

head "Virtual Environment erstellen"

python3 -m venv venv

bash scripts/start.sh