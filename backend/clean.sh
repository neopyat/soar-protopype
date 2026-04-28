#!/bin/bash

echo "=================================="
echo "      SOAR Cleanup Utility"
echo "=================================="

echo ""
echo "[1/7] Removing Python cache..."

find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete 2>/dev/null
find . -type f -name "*.pyo" -delete 2>/dev/null

echo "[2/7] Removing test/cache folders..."

rm -rf .pytest_cache
rm -rf .mypy_cache
rm -rf .ruff_cache

echo "[3/7] Removing virtual environments..."

rm -rf venv
rm -rf .venv

echo "[4/7] Removing runtime data..."

rm -f backend/data/*.gz
rm -f data/*.gz
rm -f ml_baseline.json

echo "[5/7] Removing temp/log files..."

rm -f *.tmp
rm -f *.log
rm -f Thumbs.db
find . -name ".DS_Store" -delete 2>/dev/null

echo "[6/7] Removing editor temp files..."

rm -rf .vscode/.ropeproject 2>/dev/null

echo "[7/7] Cleanup complete."

echo ""
echo "Project cleaned successfully."