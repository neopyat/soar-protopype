#!/bin/bash

set -e

echo "======================================"
echo "        SOAR Firewall Setup"
echo "======================================"
echo ""

# -------------------------
# CHECK ROOT
# -------------------------
if [[ $EUID -ne 0 ]]; then
    echo "[!] Run with sudo"
    exit 1
fi

# -------------------------
# ENSURE NFTABLES
# -------------------------
echo "[1/4] Checking nftables..."

if ! command -v nft >/dev/null 2>&1; then
    echo "[!] nftables is not installed"
    exit 1
fi

# -------------------------
# ENABLE SERVICE
# -------------------------
echo "[2/4] Enabling nftables service..."

systemctl enable nftables >/dev/null 2>&1 || true
systemctl start nftables >/dev/null 2>&1 || true

# -------------------------
# CREATE SOAR TABLE
# -------------------------
echo "[3/4] Creating SOAR nftables structure..."

nft list table inet soar >/dev/null 2>&1 || \
nft add table inet soar

# -------------------------
# CREATE BLACKLIST CHAIN
# -------------------------
echo "[4/4] Creating blacklist chain..."

nft list chain inet soar blacklist >/dev/null 2>&1 || \
nft add chain inet soar blacklist \
'{ type filter hook input priority 0; policy accept; }'

echo ""
echo "[✓] Firewall setup completed"

echo ""
echo "[*] Current SOAR firewall rules:"
echo ""

nft list table inet soar || true