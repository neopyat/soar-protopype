#!/bin/bash

set -e

echo "======================================"
echo "         SOAR Cleanup Utility"
echo "======================================"
echo ""

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$PROJECT_ROOT"

# -------------------------
# STOP SERVICE
# -------------------------
echo "[1/9] Stopping SOAR service..."

systemctl stop soar >/dev/null 2>&1 || true

# -------------------------
# REMOVE PYTHON CACHE
# -------------------------
echo "[2/9] Removing Python cache..."

find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
find . -type f -name "*.pyo" -delete 2>/dev/null || true

# -------------------------
# REMOVE TOOL CACHE
# -------------------------
echo "[3/9] Removing tool cache..."

rm -rf .pytest_cache
rm -rf .mypy_cache
rm -rf .ruff_cache

# -------------------------
# PREPARE LOGS
# -------------------------
echo "[4/9] Cleaning logs..."

mkdir -p logs

rm -f logs/*.log 2>/dev/null || true

touch logs/soar.log

# -------------------------
# CLEAN RUNTIME DATA
# -------------------------
echo "[5/9] Cleaning runtime data..."

mkdir -p data
mkdir -p database

rm -f data/*.gz 2>/dev/null || true
rm -f ml_baseline.json 2>/dev/null || true

# -------------------------
# CLEAN DATABASE
# -------------------------
echo "[6/9] Cleaning database..."

rm -f database/*.db 2>/dev/null || true

# -------------------------
# RESET FIREWALL RULES
# -------------------------
echo "[7/9] Resetting SOAR firewall rules..."

nft flush chain inet soar blacklist >/dev/null 2>&1 || true

# -------------------------
# REMOVE TEMP FILES
# -------------------------
echo "[8/9] Removing temporary files..."

find . -name "*.tmp" -delete 2>/dev/null || true
find . -name ".DS_Store" -delete 2>/dev/null || true
find . -name "Thumbs.db" -delete 2>/dev/null || true

# -------------------------
# FINAL
# -------------------------
echo "[9/9] Cleanup completed"

echo ""
echo "[✓] SOAR runtime state cleaned"

echo ""
echo "Preserved:"
echo "  • venv"
echo "  • config.json"
echo "  • systemd service"
echo "  • nftables structure"

echo ""
echo "Restart service:"
echo "sudo systemctl start soar"