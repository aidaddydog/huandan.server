#!/usr/bin/env bash
set -Eeuo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"/.. && pwd)"
ROOT="$(cd "$DIR/../.." && pwd)"
source "$DIR/lib/common.sh"
load_env
require_env HUANDAN_BASE HUANDAN_DATA PORT

step "安装/覆盖 systemd 单元"
install -m 644 "$ROOT/config/systemd/huandan.service" /etc/systemd/system/huandan.service
systemctl daemon-reload
ok "systemd 已重载"
