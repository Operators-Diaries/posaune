#======// Startlogik: korrektes Arbeitsverzeichnis sicherstellen //===========//

$TARGET_NAME = "posaune"

# Prüfen, ob Skript als Datei läuft oder gepiped wurde
if ($MyInvocation.MyCommand.Path) {
    # Skript läuft als Datei → Verzeichnis der Datei verwenden
    $SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
    $WORK_DIR = $SCRIPT_DIR
}
else {
    # Skript wurde gepiped (iwr | iex)
    $CURRENT_DIR = Get-Location
    $CURRENT_NAME = Split-Path $CURRENT_DIR -Leaf

    if ($CURRENT_NAME -eq $TARGET_NAME) {
        $WORK_DIR = $CURRENT_DIR
    }
    else {
        $WORK_DIR = Join-Path $CURRENT_DIR $TARGET_NAME
        if (-not (Test-Path $WORK_DIR)) {
            New-Item -ItemType Directory -Path $WORK_DIR | Out-Null
        }
    }
}

Set-Location $WORK_DIR
Write-Host "Arbeitsverzeichnis: $(Get-Location)"


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

if (Test-Path ".git") {
    Write-Host "Repository existiert bereits – ziehe Updates"
    git reset --hard
    git pull
} else {
    git clone "https://github.com/Operators-Diaries/posaune.git" .
}

#======// Requirements //======================================================//

Write-Host "=== Virtual Environment erstellen ==="

python -m venv venv

. .\venv\Scripts\Activate.ps1

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
    
    Start-Process "http://127.0.0.1:5000"
    Write-Host "Standardbrowser geöffnet (Edge nicht gefunden)"
} else {
    Start-Process $EdgePath -ArgumentList "--kiosk http://127.0.0.1:5000 --edge-kiosk-type=fullscreen"
}

Write-Host "=== Setup abgeschlossen ==="