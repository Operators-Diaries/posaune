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

#======// Startlogik: korrektes Arbeitsverzeichnis sicherstellen //================================//

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
POSAUNE_DIR="$(dirname "$SCRIPT_DIR")"

cd "$POSAUNE_DIR"
echo "Arbeitsverzeichnis: $PWD"


#======// Repository pullen //=====================================================================//

head "Repository herunterladen"

# Repository überprüfen
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    fehler "Die Klonung des Repositorys fehlt oder ist fehlerhaft. Bitte installiere Posaune erneut"
    exit 1
fi

git reset --hard
git pull


#======// Pakete überprüfen //========================================================================//

# venv überprüfen
if [ ! -d "venv" ] || [ ! -f "venv/bin/activate" ]; then
    fehler "Das Virtual Environmentt fehlt oder ist fehlerhaft. Bitte installiere Posaune erneut"
    exit 1
fi

source venv/bin/activate

head "Pip aktualisieren"
python3 -m pip install --upgrade pip

head "Installiere/aktualisiere benötigte Pakete"
python3 -m pip install -r requirements.txt


#======// Server //==============================================================================//

head "Starte Flask-Server"

python3 main.py &

FLASK_PID=$!

#======// Website öffnen //========================================================================//

head "Öffne Browser im Vollbild"

chromium --start-fullscreen "http://127.0.0.1:5000" &

info "Setup abgeschlossen"
echo "Flask läuft mit PID $FLASK_PID"

wait $FLASK_PID