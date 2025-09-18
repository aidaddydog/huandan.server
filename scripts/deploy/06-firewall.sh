#!/usr/bin/env bash
# 作用：放行服务端口（UFW），保障远程不掉线
# 说明：自动安装/启用 UFW（先放行 OpenSSH），放行 $PORT。幂等执行。
set -Eeuo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"/.. && pwd)"   # scripts/
source "$DIR/lib/common.sh"
load_env
require_env PORT

step "配置防火墙并放行端口：$PORT/tcp"

# 安装 UFW（若缺失）
if ! command -v ufw >/dev/null 2>&1; then
  apt-get update -y
  apt-get install -y --no-install-recommends ufw
fi

# 先放行 SSH，避免启用 UFW 时断连
ufw allow OpenSSH >/dev/null 2>&1 || true

# 启用 UFW（如未启用）
if ufw status | grep -q "Status: inactive"; then
  warn "UFW 当前未启用，将自动启用（已放行 OpenSSH）"
  ufw --force enable
fi

# 放行业务端口（幂等）
if ufw status | grep -E -q "[[:space:]]${PORT}/tcp[[:space:]]"; then
  ok "端口 ${PORT}/tcp 已在 UFW 规则中"
else
  ufw allow "${PORT}/tcp"
  ok "已放行端口：${PORT}/tcp"
fi

echo
echo "当前 UFW 规则（节选）："
ufw status numbered || true

echo
echo "如需查看 UFW 日志（若开启日志）："
echo "  tail -n 200 /var/log/ufw.log"
