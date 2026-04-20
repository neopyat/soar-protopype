#!/bin/bash

echo "=============================="
echo "   SOAR Prototype Uninstall   "
echo "=============================="

# -------------------------
# Stop running process
# -------------------------
echo "[*] Stopping SOAR (if running)..."
pkill -f "main.py" 2>/dev/null

# -------------------------
# Remove virtual environment
# -------------------------
if [ -d "venv" ]; then
    echo "[*] Removing virtual environment..."
    rm -rf venv
else
    echo "[*] No virtual environment found"
fi

# -------------------------
# Optional: remove local data
# -------------------------
echo "[*] Remove local data (logs, storage)?"
read -p "(y/n): " confirm_data

if [[ "$confirm_data" == "y" ]]; then
    rm -rf backend/data 2>/dev/null
    rm -f backend/auth.log 2>/dev/null
    echo "[*] Local data removed"
fi

# -------------------------
# Optional: remove project
# -------------------------
echo "[*] Remove entire project folder?"
read -p "(y/n): " confirm_project

if [[ "$confirm_project" == "y" ]]; then
    cd ..
    rm -rf soar-prototype
    echo "[*] Project folder removed"
fi

# -------------------------
# Final
# -------------------------
echo "[*] Uninstall complete"