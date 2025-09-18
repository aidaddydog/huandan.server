#!/usr/bin/env bash
# 作用：安装/覆盖 systemd 单元（huandan.service）
# 说明：修复原脚本根目录误算到 /opt 的问题；不存在模板时会自动生成一个可用的单元文件。
set -Eeuo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"/.. && pwd)"   # scripts/
REPO_ROOT="$(cd "$DIR/.." && pwd)"                       # ← 只回退一级，指向仓库根 /opt/huandan

source "$DIR/lib/common.sh"
load_env
require_env HUANDAN_BASE HUANDAN_DATA PORT PYBIN || true  # PYBIN 如未在 env 里设置也不致命

UNIT_SRC="$REPO_ROOT/config/systemd/huandan.service"
UNIT_DST="/etc/systemd/system/huandan.service"

step "安装/覆盖 systemd 单元"

# 若仓库里存在模板则优先使用
if [[ -f "$UNIT_SRC" ]]; then
  install -m 644 "$UNIT_SRC" "$UNIT_DST"
  ok "已安装仓库内的 unit: $UNIT_SRC -> $UNIT_DST"
else
  warn "未找到 $UNIT_SRC，将生成一个通用的 huandan.service 以保证服务可启动"

  # 兜底生成一个可用的 unit（使用 venv 的 python 运行 uvicorn）
  # 说明：
  # - WorkingDirectory 指向 $HUANDAN_BASE
  # - 默认从 app.main:app 启动（如你的入口不同，可在仓库模板里改）
  # - 日志写入 journalctl，可用下方一键命令查看
  cat > "$UNIT_DST" <<UNIT
[Unit]
Description=Huandan FastAPI Service
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=${HUANDAN_BASE}
Environment=PYTHONUNBUFFERED=1
Environment=PORT=${PORT}
ExecStart=${HUANDAN_BASE}/.venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port \${PORT}
Restart=on-failure
RestartSec=3
User=root
Group=root
# 限制可按需调整
LimitNOFILE=65535

[Install]
WantedBy=multi-user.target
UNIT

  chmod 644 "$UNIT_DST"
  ok "已生成通用 unit：$UNIT_DST"
fi

systemctl daemon-reload
ok "systemd 已重载"

# 可选：开机自启并立即启动
if systemctl is-enabled huandan.service >/dev/null 2>&1; then
  :
else
  systemctl enable huandan.service || true
fi

# 不强制立即启动，交由你的 99-restart/quickstart 统一控制；如需现在启动：
# systemctl restart huandan.service

echo
echo "如需现在立即启动并查看日志："
echo "  systemctl restart huandan.service"
echo "  journalctl -u huandan.service -e -n 200   # 一键查看服务日志（最后200行）"
