#!/usr/bin/env bash
# 中文通用函数库：进度提示、错误捕获、日志/防火墙/权限等
set -Eeuo pipefail

LOG="${LOG:-/var/log/huandan-deploy.log}"
: > "$LOG" || true

step()  { echo "[`date +%H:%M:%S`]【步骤】$*" | tee -a "$LOG"; }
ok()    { echo "[OK] $*" | tee -a "$LOG"; }
warn()  { echo "[WARN] $*" | tee -a "$LOG"; }
err()   { echo "[ERR] $*" | tee -a "$LOG"; }
die()   { err "$*"; echo -e "\n# 一键查看服务日志（最后200行）:\n  journalctl -u huandan.service -e -n 200"; exit 1; }

trap 'die "执行失败（行号 $LINENO）。你可以运行：tail -n 200 $LOG 查看部署日志。"' ERR

require_env() {
  local v; for v in "$@"; do
    [[ -n "${!v:-}" ]] || die "缺少必要环境变量：$v"
  done
}

load_env() {
  if [[ -f /etc/huandan.env ]]; then
    # shellcheck disable=SC1091
    source /etc/huandan.env
  else
    warn "未发现 /etc/huandan.env，使用默认变量；建议先从 config/env/huandan.env.example 复制。"
  fi
}

ensure_user_group() {
  id -u huandan &>/dev/null || useradd -r -s /usr/sbin/nologin -d /opt/huandan-server huandan
  mkdir -p "$HUANDAN_BASE" "$HUANDAN_DATA" "$HUANDAN_BASE/app/templates" "$HUANDAN_BASE/app/static" "$HUANDAN_BASE/runtime" "$HUANDAN_DATA/pdfs" "$HUANDAN_DATA/uploads"
  chown -R huandan:huandan "$HUANDAN_BASE" "$HUANDAN_DATA"
}

apt_noninteractive() {
  export DEBIAN_FRONTEND=noninteractive
}

allow_port_if_needed() {
  if [[ "${EXPOSE_MODE:-DIRECT}" == "DIRECT" ]]; then
    if command -v ufw &>/dev/null; then
      if ! ufw status | grep -qE "\b${PORT}/tcp\b"; then
        ufw allow "${PORT}/tcp" || true
        ok "已放行 UFW 端口 ${PORT}/tcp（直出模式）"
      fi
    else
      warn "未安装 UFW，跳过放行。"
    fi
  else
    ok "EXPOSE_MODE=${EXPOSE_MODE}，假定有反向代理，不直接放行应用端口。"
  fi
}

show_systemd_status() {
  systemctl --no-pager -l status huandan.service | sed -n '1,80p' || true
  echo -e "\n# 快速查看日志：journalctl -u huandan.service -e -n 200"
}
