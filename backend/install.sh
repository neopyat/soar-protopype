#!/bin/bash

echo "=============================="
echo "   SOAR Prototype Installer   "
echo "=============================="

# Python check
echo "[*] Checking Python..."
if ! command -v python3 &> /dev/null
then
    echo "[!] Python3 not found. Installing..."
    sudo apt update
    sudo apt install -y python3 python3-pip
fi

# pip update
echo "[*] Updating pip..."
python3 -m pip install --upgrade pip

# log file
echo "[*] Preparing log file..."
mkdir -p backend
touch backend/auth.log

echo "[*] Installation complete."
echo "[*] Next step: run CLI setup"