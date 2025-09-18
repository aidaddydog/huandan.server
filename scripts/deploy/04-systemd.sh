#!/usr/bin/env bash
set -Eeuo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPTS_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_ROOT="$(cd "$SCRIPTS_ROOT/.." && pwd)"
source "$SCRIPTS_ROOT/lib/common.sh"
load_env
require_env HUANDAN_BASE HUANDAN_DATA PORT

step "安装/覆盖 systemd 单元"
install -m 644 "$REPO_ROOT/config/systemd/huandan.service" /etc/systemd/system/huandan.service
systemctl daemon-reload
ok "systemd 已重载"
