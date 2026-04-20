#!/bin/bash

echo "=============================="
echo "   SOAR Prototype Installer   "
echo "=============================="

# -------------------------
# Python check
# -------------------------
echo "[*] Checking Python..."
if ! command -v python3 &> /dev/null
then
    echo "[!] Python3 not found. Installing..."
    sudo apt update
    sudo apt install -y python3 python3-pip python3-venv
fi

# -------------------------
# Create virtual environment
# -------------------------
echo "[*] Creating virtual environment..."
python3 -m venv venv

echo "[*] Activating virtual environment..."
source venv/bin/activate

# -------------------------
# Upgrade pip
# -------------------------
echo "[*] Updating pip..."
pip install --upgrade pip

# -------------------------
# Install dependencies
# -------------------------
if [ ! -f "requirements.txt" ]; then
    echo "[*] requirements.txt not found, creating minimal file..."
    echo "" > requirements.txt
fi

echo "[*] Installing dependencies..."
pip install -r requirements.txt

# -------------------------
# Final
# -------------------------
echo "[*] Installation complete."
echo "[*] To activate environment manually: source venv/bin/activate"
echo "[*] Next step: run CLI setup (python cli_setup.py)"