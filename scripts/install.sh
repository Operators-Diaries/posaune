#!/usr/bin/env bash

set -e

mkdir -p posaune

cd posaune

#======// Repository pullen //=====================================================================//

echo "=== Repository herunterladen ==="

REPO_URL="https://github.com/Operators-Diaries/posaune.git"

echo "Clone Repository"
git clone "$REPO_URL" .


#======// Environment //==========================================================================//

echo "=== Virtual Environment erstellen ==="

python3 -m venv venv

bash scripts/start.sh