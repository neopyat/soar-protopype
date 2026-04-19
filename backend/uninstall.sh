#!/bin/bash

echo "[*] Stopping SOAR (if running)..."
pkill -f "main.py" 2>/dev/null

echo "[*] Removing virtual environment..."
rm -rf venv

echo "[*] Cleaning logs (optional)..."
rm -f /var/log/auth.log

echo "[*] Removing iptables rules (if any)..."
iptables -F

echo "[*] Removing project directory (optional)"
read -p "Delete project folder? (y/n): " confirm
if [[ $confirm == "y" ]]; then
    cd ..
    rm -rf soar-prototype
fi

echo "[*] Uninstall complete"