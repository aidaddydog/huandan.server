#!/usr/bin/env bash
set -Eeuo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPTS_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
source "$SCRIPTS_ROOT/lib/common.sh"
load_env

step "启用并重启服务"
systemctl enable huandan.service
systemctl restart huandan.service
sleep 1
show_systemd_status
ok "服务已重启。后台地址： http://<服务器IP>:${PORT:-8000}/admin"
echo "首次初始化： http://<服务器IP>:${PORT:-8000}/admin/bootstrap"
