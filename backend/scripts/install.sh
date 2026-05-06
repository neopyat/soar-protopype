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
# REQUIREMENTS
# -------------------------
echo "[6/10] Installing Python packages..."

if [ ! -f "requirements.txt" ]; then
    cat <<EOF > requirements.txt
psutil
flask
sqlalchemy
EOF
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
# CREATE CONFIG
# -------------------------
echo "[8/10] Preparing configuration..."

if [ ! -f "config.json" ]; then
    python3 cli_setup.py
else
    echo "[*] config.json already exists"
fi

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


# #!/bin/bash

# echo "=================================="
# echo "      SOAR Ubuntu Installer"
# echo "=================================="
# echo ""

# # -------------------------
# # Python
# # -------------------------
# echo "[1/8] Checking Python3..."

# if ! command -v python3 >/dev/null 2>&1
# then
#     sudo apt update
#     sudo apt install -y python3 python3-pip python3-venv
# fi

# # -------------------------
# # System deps
# # -------------------------
# echo "[2/8] Installing system dependencies..."

# sudo apt install -y sqlite3

# # -------------------------
# # venv
# # -------------------------
# echo "[3/8] Creating virtual environment..."
# python3 -m venv venv

# # -------------------------
# # activate
# # -------------------------
# echo "[4/8] Activating venv..."
# source venv/bin/activate

# # -------------------------
# # pip
# # -------------------------
# echo "[5/8] Updating pip..."
# pip install --upgrade pip

# # -------------------------
# # requirements
# # -------------------------
# echo "[6/8] Installing requirements..."

# cat <<EOF > requirements.txt
# psutil
# EOF

# pip install -r requirements.txt

# # -------------------------
# # folders
# # -------------------------
# echo "[7/8] Preparing folders..."

# mkdir -p backend/data
# mkdir -p backend/database
# touch backend/auth.log

# # -------------------------
# # init DB
# # -------------------------
# echo "[8/8] Initializing database..."

# python - <<EOF
# from storage.db import Database
# Database()
# print("[*] Database initialized")
# EOF

# # -------------------------
# # CLI config
# # -------------------------
# echo ""
# echo "[*] Launching config wizard..."
# python cli_setup.py

# echo ""
# echo "[✓] Installation complete"
# echo ""
# echo "Run:"
# echo "source venv/bin/activate && python3 main.py"
