Write-Host "=================================="
Write-Host "     SOAR Windows Installer"
Write-Host "=================================="
Write-Host ""

# -------------------------
# Python check
# -------------------------

Write-Host "[1/7] Checking Python..."

$pythonExists = Get-Command py -ErrorAction SilentlyContinue

if (-not $pythonExists) {
    Write-Host "[!] Python launcher not found."
    Write-Host "Install Python from https://python.org"
    exit
}

# -------------------------
# Create venv
# -------------------------

Write-Host "[2/7] Creating virtual environment..."

py -m venv venv

# -------------------------
# Activate
# -------------------------

Write-Host "[3/7] Activating venv..."

& .\venv\Scripts\Activate.ps1

# -------------------------
# Upgrade pip
# -------------------------

Write-Host "[4/7] Updating pip..."

python -m pip install --upgrade pip

# -------------------------
# Requirements
# -------------------------

Write-Host "[5/7] Installing requirements..."

if (!(Test-Path "requirements.txt")) {
    New-Item -ItemType File -Name requirements.txt | Out-Null
}

pip install -r requirements.txt

# -------------------------
# Prepare folders
# -------------------------

Write-Host "[6/7] Preparing folders..."

New-Item -ItemType Directory -Force -Path backend\data | Out-Null
New-Item -ItemType File -Force -Path backend\auth.log | Out-Null

# -------------------------
# Config wizard
# -------------------------

Write-Host "[7/7] Launching setup wizard..."

python cli_setup.py

Write-Host ""
Write-Host "Installation complete."
Write-Host ""
Write-Host "Run project:"
Write-Host "py main.py"