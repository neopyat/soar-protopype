#!/bin/bash

set -e

echo "======================================"
echo "      SOAR Prototype Installer"
echo "======================================"
echo ""

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$PROJECT_ROOT"

# -------------------------
# CHECK ROOT
# -------------------------
if [[ $EUID -ne 0 ]]; then
    echo "[!] Run installer with sudo"
    exit 1
fi

# -------------------------
# SYSTEM UPDATE
# -------------------------
echo "[1/10] Updating packages..."

apt update

# -------------------------
# INSTALL DEPENDENCIES
# -------------------------
echo "[2/10] Installing dependencies..."

apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    sqlite3 \
    nftables \
    openssh-client

# -------------------------
# CREATE VENV
# -------------------------
echo "[3/10] Preparing virtual environment..."

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# -------------------------
# ACTIVATE VENV
# -------------------------
echo "[4/10] Activating virtual environment..."

source venv/bin/activate

# -------------------------
# UPDATE PIP
# -------------------------
echo "[5/10] Updating pip..."

pip install --upgrade pip

# -------------------------
# REQUIREMENTS VALIDATION
# -------------------------
echo "[6/10] Installing Python packages..."

if [ ! -f "requirements.txt" ]; then
    echo "[!] requirements.txt not found"
    exit 1
fi

pip install -r requirements.txt

# -------------------------
# CREATE DIRECTORIES
# -------------------------
echo "[7/10] Preparing directories..."

mkdir -p data
mkdir -p logs
mkdir -p database

touch logs/soar.log

# -------------------------
# CONFIGURATION WIZARD
# -------------------------
echo "[8/10] Launching configuration wizard..."

python3 cli_setup.py

# -------------------------
# FIREWALL SETUP
# -------------------------
echo "[9/10] Configuring firewall..."

bash scripts/setup_firewall.sh

# -------------------------
# SYSTEMD SERVICE
# -------------------------
echo "[10/10] Configuring systemd service..."

bash scripts/setup_service.sh

echo ""
echo "[✓] Installation completed successfully"

echo ""
echo "Start service:"
echo "sudo systemctl start soar"

echo ""
echo "Check status:"
echo "sudo systemctl status soar"

echo ""
echo "View logs:"
echo "journalctl -u soar -f"