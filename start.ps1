$TARGET_DIR = "posaune"
$REPO_URL = "https://github.com/Operators-Diaries/posaune.git"
$URL = "http://127.0.0.1:5000"

#======// Python & Git sicherstellen //============================================================//

Write-Host "=== Prüfe Installationen ==="

try {
    $pyver = python --version 2>&1
    Write-Host "Python: $pyver"
} catch {
    Write-Host "Python nicht gefunden. Bitte installieren von https://www.python.org/downloads/ und erneut starten."
    exit 1
}

try {
    $pipver = python -m pip --version 2>&1
    Write-Host "Pip: $pipver"
} catch {
    python -m ensurepip --upgrade
    $pipver = python -m pip --version 2>&1
    Write-Host "Pip: $pipver"
}

try {
    $gitver = git --version 2>&1
    Write-Host "Git: $gitver"
} catch {
    winget install --id Git.Git -e --source winget
    $gitver = git --version 2>&1
    Write-Host "Git: $gitver"
    exit 1
}

#======// Repository pullen //==================================================//

Write-Host "=== Repository herunterladen ==="

if (Test-Path $TARGET_DIR) {
    Write-Host "Repository existiert bereits – ziehe Updates"
    Push-Location $TARGET_DIR
    git reset --hard
    git pull
    Pop-Location
} else {
    git clone $REPO_URL $TARGET_DIR
}

#======// Requirements //========================================================================//

Write-Host "=== Virtual Environment erstellen ==="

Push-Location $TARGET_DIR
python -m venv venv

powershell -ExecutionPolicy Bypass -File .\venv\Scripts\Activate.ps1

Write-Host "=== Pip aktualisieren ==="
python -m pip install --upgrade pip

Write-Host "=== Installiere/aktualisiere benötigte Pakete ==="
python -m pip install -r requirements.txt

#======// Server starten //====================================================//

Write-Host "=== Starte Flask-Server ==="
Start-Process python -ArgumentList "main.py"
Start-Sleep -Seconds 3

#======// Website öffnen //====================================================//

Write-Host "=== Öffne Browser im Vollbild ==="

$EdgePath = "$env:ProgramFiles (x86)\Microsoft\Edge\Application\msedge.exe"
if (-Not (Test-Path $EdgePath)) {
    
    Start-Process $URL
    Write-Host "Standardbrowser geöffnet (Edge nicht gefunden)"
} else {
    Start-Process $EdgePath -ArgumentList "--kiosk $URL --edge-kiosk-type=fullscreen"
}

Write-Host "=== Setup abgeschlossen ==="

Pop-Location