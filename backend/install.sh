#!/bin/bash

echo "=================================="
echo "      SOAR Ubuntu Installer"
echo "=================================="
echo ""

# -------------------------
# Python
# -------------------------
echo "[1/8] Checking Python3..."

if ! command -v python3 >/dev/null 2>&1
then
    sudo apt update
    sudo apt install -y python3 python3-pip python3-venv
fi

# -------------------------
# System deps
# -------------------------
echo "[2/8] Installing system dependencies..."

sudo apt install -y sqlite3

# -------------------------
# venv
# -------------------------
echo "[3/8] Creating virtual environment..."
python3 -m venv venv

# -------------------------
# activate
# -------------------------
echo "[4/8] Activating venv..."
source venv/bin/activate

# -------------------------
# pip
# -------------------------
echo "[5/8] Updating pip..."
pip install --upgrade pip

# -------------------------
# requirements
# -------------------------
echo "[6/8] Installing requirements..."

cat <<EOF > requirements.txt
psutil
EOF

pip install -r requirements.txt

# -------------------------
# folders
# -------------------------
echo "[7/8] Preparing folders..."

mkdir -p backend/data
mkdir -p backend/database
touch backend/auth.log

# -------------------------
# init DB
# -------------------------
echo "[8/8] Initializing database..."

python - <<EOF
from storage.db import Database
Database()
print("[*] Database initialized")
EOF

# -------------------------
# CLI config
# -------------------------
echo ""
echo "[*] Launching config wizard..."
python cli_setup.py

echo ""
echo "[✓] Installation complete"
echo ""
echo "Run:"
echo "source venv/bin/activate && python3 main.py"

# #!/bin/bash

# echo "=================================="
# echo "      SOAR Ubuntu Installer"
# echo "=================================="
# echo ""

# # -------------------------
# # Python check
# # -------------------------

# echo "[1/7] Checking Python3..."

# if ! command -v python3 >/dev/null 2>&1
# then
#     echo "[!] Python3 not found."
#     echo "[*] Installing Python3..."

#     sudo apt update
#     sudo apt install -y python3 python3-pip python3-venv
# fi

# # -------------------------
# # Create venv
# # -------------------------

# echo "[2/7] Creating virtual environment..."

# python3 -m venv venv

# # -------------------------
# # Activate
# # -------------------------

# echo "[3/7] Activating venv..."

# source venv/bin/activate

# # -------------------------
# # Upgrade pip
# # -------------------------

# echo "[4/7] Updating pip..."

# python -m pip install --upgrade pip

# # -------------------------
# # Requirements
# # -------------------------

# echo "[5/7] Installing requirements..."

# if [ ! -f requirements.txt ]; then
#     touch requirements.txt
# fi

# pip install -r requirements.txt

# # -------------------------
# # Prepare folders
# # -------------------------

# echo "[6/7] Preparing folders..."

# mkdir -p backend/data
# touch backend/auth.log

# # -------------------------
# # Config wizard
# # -------------------------

# echo "[7/7] Launching setup wizard..."

# python cli_setup.py

# echo ""
# echo "Installation complete."
# echo ""
# echo "Run project:"
# echo "python3 main.py"

# #!/bin/bash

# echo "=============================="
# echo "   SOAR Prototype Installer   "
# echo "=============================="

# # -------------------------
# # Python check
# # -------------------------
# echo "[*] Checking Python..."
# if ! command -v python3 &> /dev/null
# then
#     echo "[!] Python3 not found. Installing..."
#     sudo apt update
#     sudo apt install -y python3 python3-pip python3-venv
# fi

# # -------------------------
# # Create virtual environment
# # -------------------------
# echo "[*] Creating virtual environment..."
# python3 -m venv venv

# echo "[*] Activating virtual environment..."
# source venv/bin/activate

# # -------------------------
# # Upgrade pip
# # -------------------------
# echo "[*] Updating pip..."
# pip install --upgrade pip

# # -------------------------
# # Install dependencies
# # -------------------------
# if [ ! -f "requirements.txt" ]; then
#     echo "[*] requirements.txt not found, creating minimal file..."
#     echo "" > requirements.txt
# fi

# echo "[*] Installing dependencies..."
# pip install -r requirements.txt

# # -------------------------
# # Final
# # -------------------------
# echo "[*] Installation complete."
# echo "[*] To activate environment manually: source venv/bin/activate"
# echo "[*] Next step: run CLI setup (python cli_setup.py)"