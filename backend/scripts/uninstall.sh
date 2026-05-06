#!/bin/bash

set -e

echo "======================================"
echo "         SOAR Uninstaller"
echo "======================================"
echo ""

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$PROJECT_ROOT"

# -------------------------
# CHECK ROOT
# -------------------------
if [[ $EUID -ne 0 ]]; then
    echo "[!] Run with sudo"
    exit 1
fi

# -------------------------
# STOP SERVICE
# -------------------------
echo "[1/8] Stopping SOAR service..."

systemctl stop soar >/dev/null 2>&1 || true

# -------------------------
# DISABLE SERVICE
# -------------------------
echo "[2/8] Disabling SOAR service..."

systemctl disable soar >/dev/null 2>&1 || true

# -------------------------
# REMOVE SERVICE FILE
# -------------------------
echo "[3/8] Removing systemd service..."

rm -f /etc/systemd/system/soar.service

systemctl daemon-reload

# -------------------------
# REMOVE FIREWALL RULES
# -------------------------
echo "[4/8] Removing SOAR firewall rules..."

nft flush chain inet soar blacklist >/dev/null 2>&1 || true
nft delete chain inet soar blacklist >/dev/null 2>&1 || true
nft delete table inet soar >/dev/null 2>&1 || true

# -------------------------
# REMOVE DATABASES
# -------------------------
echo "[5/8] Removing databases..."

rm -f database/*.db 2>/dev/null || true

# -------------------------
# REMOVE LOGS
# -------------------------
echo "[6/8] Removing logs..."

rm -rf logs

# -------------------------
# REMOVE VENV
# -------------------------
echo "[7/8] Removing virtual environment..."

rm -rf venv

# -------------------------
# OPTIONAL PROJECT REMOVAL
# -------------------------
echo "[8/8] Remove entire project directory?"
read -p "(y/n): " confirm

if [[ "$confirm" == "y" ]]; then

    cd ..

    PROJECT_NAME="$(basename "$PROJECT_ROOT")"

    rm -rf "$PROJECT_NAME"

    echo ""
    echo "[✓] Project directory removed"

else
    echo ""
    echo "[✓] SOAR uninstalled"
    echo "[*] Project files preserved"
fi


# #!/bin/bash

# echo "=============================="
# echo "   SOAR Prototype Uninstall   "
# echo "=============================="

# # -------------------------
# # Stop running process
# # -------------------------
# echo "[*] Stopping SOAR (if running)..."
# pkill -f "main.py" 2>/dev/null

# # -------------------------
# # Remove virtual environment
# # -------------------------
# if [ -d "venv" ]; then
#     echo "[*] Removing virtual environment..."
#     rm -rf venv
# else
#     echo "[*] No virtual environment found"
# fi

# # -------------------------
# # Optional: remove local data
# # -------------------------
# echo "[*] Remove local data (logs, storage)?"
# read -p "(y/n): " confirm_data

# if [[ "$confirm_data" == "y" ]]; then
#     rm -rf backend/data 2>/dev/null
#     rm -f backend/auth.log 2>/dev/null
#     echo "[*] Local data removed"
# fi

# # -------------------------
# # Optional: remove project
# # -------------------------
# echo "[*] Remove entire project folder?"
# read -p "(y/n): " confirm_project

# if [[ "$confirm_project" == "y" ]]; then
#     cd ..
#     rm -rf soar-prototype
#     echo "[*] Project folder removed"
# fi

# # -------------------------
# # Final
# # -------------------------
# echo "[*] Uninstall complete"