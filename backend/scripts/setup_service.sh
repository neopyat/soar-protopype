#!/bin/bash

set -e

echo "======================================"
echo "         SOAR Service Setup"
echo "======================================"
echo ""

# -------------------------
# CHECK ROOT
# -------------------------
if [[ $EUID -ne 0 ]]; then
    echo "[!] Run with sudo"
    exit 1
fi

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

SERVICE_FILE="/etc/systemd/system/soar.service"

# -------------------------
# CREATE SERVICE FILE
# -------------------------
echo "[1/4] Creating systemd service..."

cat <<EOF > "$SERVICE_FILE"
[Unit]
Description=SOAR Prototype Service
After=network.target

[Service]
Type=simple
WorkingDirectory=$PROJECT_ROOT
ExecStart=$PROJECT_ROOT/venv/bin/python3 $PROJECT_ROOT/main.py
Restart=always
RestartSec=5

User=root
Group=root

Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOF

# -------------------------
# RELOAD SYSTEMD
# -------------------------
echo "[2/4] Reloading systemd..."

systemctl daemon-reload

# -------------------------
# ENABLE SERVICE
# -------------------------
echo "[3/4] Enabling SOAR service..."

systemctl enable soar

# -------------------------
# FINAL STATUS
# -------------------------
echo "[4/4] Checking service..."

systemctl status soar --no-pager || true

echo ""
echo "[✓] SOAR service installed"

echo ""
echo "Useful commands:"
echo ""
echo "Start service:"
echo "sudo systemctl start soar"
echo ""
echo "Stop service:"
echo "sudo systemctl stop soar"
echo ""
echo "Restart service:"
echo "sudo systemctl restart soar"
echo ""
echo "Logs:"
echo "journalctl -u soar -f"