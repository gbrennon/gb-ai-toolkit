#!/usr/bin/env bash
# install-systemd.sh — Install AI Toolkit systemd user services and timers
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SYSTEMD_DIR="${SCRIPT_DIR}/../systemd"
USER_SYSTEMD_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user"

mkdir -p "$USER_SYSTEMD_DIR"

echo "==> Installing systemd user units from $SYSTEMD_DIR"

for unit in "$SYSTEMD_DIR"/*.service "$SYSTEMD_DIR"/*.timer; do
    name="$(basename "$unit")"
    cp "$unit" "$USER_SYSTEMD_DIR/$name"
    echo "    $name"
done

systemctl --user daemon-reload

echo ""
echo "==> Enabling timers..."
for timer in "$SYSTEMD_DIR"/*.timer; do
    name="$(basename "$timer")"
    systemctl --user enable --now "$name"
    echo "    $name enabled & started"
done

echo ""
echo "Done. Check status with: systemctl --user status 'gb-*'"
