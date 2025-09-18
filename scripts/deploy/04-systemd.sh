#!/usr/bin/env bash
set -Eeuo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"/.. && pwd)"   # scripts/
REPO_ROOT="$(cd "$DIR/.." && pwd)"                       # 修正，只退一级
source "$DIR/lib/common.sh"
load_env
require_env HUANDAN_BASE HUANDAN_DATA PORT

step "安装/覆盖 systemd 单元"

UNIT_SRC="$REPO_ROOT/config/systemd/huandan.service"
UNIT_DST="/etc/systemd/system/huandan.service"

if [[ ! -f "$UNIT_SRC" ]]; then
  die "未找到 unit 模板文件：$UNIT_SRC
请确认仓库里是否存在 config/systemd/huandan.service。"
fi

install -m 644 "$UNIT_SRC" "$UNIT_DST"
systemctl daemon-reload
ok "systemd 已重载"

echo
echo "已安装 unit: $UNIT_DST"
echo "如需立即启用并启动："
echo "  systemctl enable --now huandan.service"
echo "如需查看日志："
echo "  journalctl -u huandan.service -e -n 200"
