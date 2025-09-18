#!/usr/bin/env bash
# =============================================================
# Huandan Server 一键部署（root 直接运行服务；读取仓库内 .deploy.env）
# 目标：从仓库内直接执行 → 无需额外传参 → 一步到位
# 特性：
# - 自动识别 BASE=当前仓库根目录
# - 自动读取 .deploy.env（PORT/HOST/AUTO_CLEAN 等）
# - systemd 使用绝对路径（不在 unit 中展开 env）
# - 兜底创建 runtime/ 与 updates/，避免导入 app.main 时报错
# - 中文进度 + 安装日志 + 一行日志调取命令
# =============================================================

set -Eeuo pipefail

# ---------------- 基础与日志 ----------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd -P)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd -P 2>/dev/null || pwd -P)"
ENV_FILE="${ENV_FILE:-$REPO_ROOT/.deploy.env}"

TS="$(date +%Y%m%d-%H%M%S)"
LOG_DIR="/var/log/huandan"
INSTALL_LOG="$LOG_DIR/install-root-$TS.log"
BACKUP_ROOT="/opt/huandan-backups"
BACKUP_DIR="$BACKUP_ROOT/$TS"

mkdir -p "$LOG_DIR" "$BACKUP_ROOT"
exec > >(tee -a "$INSTALL_LOG") 2>&1

step(){ echo -e "==> $*"; }
ok(){ echo -e "✔ $*"; }
warn(){ echo -e "⚠ $*"; }
die(){ echo -e "✘ $*"; exit 1; }
trap 'echo -e "✘ 安装失败（见日志：$INSTALL_LOG）\njournalctl -u huandan.service -e -n 200"; exit 1' ERR

# ---------------- 默认配置（可被 .deploy.env / 环境变量覆盖） ----------------
REPO="${REPO:-}"                  # 若脚本在仓库内，无需设置；否则自动从 .git origin 获取
BRANCH="${BRANCH:-main}"
BASE="${BASE:-$REPO_ROOT}"        # 关键：默认以“当前仓库根目录”为 BASE
DATA="${DATA:-/opt/huandan-data}"
PORT="${PORT:-8000}"
HOST="${HOST:-0.0.0.0}"
PYBIN="${PYBIN:-python3}"
SECRET_KEY="${SECRET_KEY:-please-change-me}"
AUTO_CLEAN="${AUTO_CLEAN:-no}"

# 读取仓库内 .deploy.env
if [ -f "$ENV_FILE" ]; then
  set -a
  # shellcheck disable=SC1090
  . "$ENV_FILE"
  set +a
fi

# 若在 Git 仓库中，自动获取 origin 作为 REPO（便于后续 git pull/clone）
if [ -z "${REPO:-}" ] && [ -d "$REPO_ROOT/.git" ]; then
  REPO="$(git -C "$REPO_ROOT" remote get-url origin 2>/dev/null || true)"
fi

echo "BASE=$BASE DATA=$DATA PORT=$PORT HOST=$HOST REPO=${REPO:-<none>} BRANCH=$BRANCH"
[ "$(id -u)" -eq 0 ] || die "请使用 root 运行"

# ---------------- 1) 安装依赖 ----------------
step "1) 安装系统依赖（git/python/ufw 等）"
export DEBIAN_FRONTEND=noninteractive
apt-get update -y
apt-get install -y --no-install-recommends git curl ca-certificates tzdata python3-venv python3-pip rsync unzip ufw
ok "依赖安装完成"

# ---------------- 2) 目录就绪 ----------------
step "2) 目录就绪（含 runtime/ 与 updates/）"
install -d -m 755 "$BASE" "$BASE/runtime" "$BASE/updates" "$DATA/pdfs" "$DATA/uploads"
ok "目录准备完成"

# ---------------- 3) 备份策略 ----------------
step "3) 备份策略：$AUTO_CLEAN"
if [ "$AUTO_CLEAN" = "yes" ] && [ -d "$BASE" ]; then
  systemctl stop huandan.service 2>/dev/null || true
  mkdir -p "$BACKUP_DIR"
  rsync -a --delete --exclude='.venv' "$BASE/" "$BACKUP_DIR/huandan-server/" 2>/dev/null || true
  rsync -a "$DATA/" "$BACKUP_DIR/huandan-data/" 2>/dev/null || true
  rm -rf "$BASE" && mkdir -p "$BASE" "$BASE/runtime" "$BASE/updates"
  ok "已备份到：$BACKUP_DIR，并将执行覆盖安装"
else
  ok "就地更新（不清空目录）"
fi

# ---------------- 4) 获取/更新代码 ----------------
step "4) 获取/更新代码"
is_empty(){ [ -z "$(ls -A "$1" 2>/dev/null)" ]; }
if [ -d "$BASE/.git" ]; then
  git -C "$BASE" fetch --all --prune || true
  (git -C "$BASE" checkout "$BRANCH" 2>/dev/null || true)
  git -C "$BASE" pull --ff-only || true
elif [ -n "${REPO:-}" ]; then
  if is_empty "$BASE"; then
    git clone -b "$BRANCH" "$REPO" "$BASE"
  else
    tmp="$(mktemp -d)"; git clone -b "$BRANCH" "$REPO" "$tmp"; rsync -a "$tmp/". "$BASE/"; rm -rf "$tmp"
  fi
else
  warn "未检测到 .git 且未提供 REPO，假定代码已就位：$BASE"
fi
ok "代码准备完成"

# ---------------- 5) Python 依赖 ----------------
step "5) 创建/更新 Python 虚拟环境并安装依赖"
cd "$BASE"
$PYBIN -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate
pip install -U pip wheel
if [ -f requirements.txt ]; then
  pip install -r requirements.txt
else
  pip install 'uvicorn[standard]' fastapi jinja2 'sqlalchemy<2.0' 'passlib[bcrypt]' pandas openpyxl 'xlrd==1.2.0' aiofiles itsdangerous python-multipart
fi
ok "Python 依赖安装完成"

# ---------------- 6) 写 /etc/default/huandan（运行时配置） ----------------
step "6) 写入 /etc/default/huandan（运行时配置）"
cat > /etc/default/huandan <<ENV
# Managed by install_root.sh
HUANDAN_BASE="$BASE"
HUANDAN_DATA="$DATA"
PORT="$PORT"
HOST="$HOST"
SECRET_KEY="$SECRET_KEY"
PYTHONUNBUFFERED=1
ENV
chmod 0644 /etc/default/huandan
ok "配置文件写入完成：/etc/default/huandan"

# ---------------- 7) 写入 systemd 并启动（绝对路径） ----------------
step "7) 写入 systemd 并启动（root）"
cat > /etc/systemd/system/huandan.service <<UNIT
[Unit]
Description=Huandan Server (FastAPI)
After=network.target

[Service]
EnvironmentFile=-/etc/default/huandan
WorkingDirectory=$BASE
ExecStart=$BASE/.venv/bin/python $BASE/run.py
Restart=always
User=root
Group=root

[Install]
WantedBy=multi-user.target
UNIT

systemctl daemon-reload
systemctl enable --now huandan.service || true
systemctl --no-pager -l status huandan.service | sed -n '1,60p'

# ---------------- 8) 重建 mapping.json ----------------
step "8) 重建 mapping.json（修正 sys.path）"
mkdir -p "$BASE/runtime" "$BASE/updates"
env BASE="$BASE" HUANDAN_DATA="$DATA" "$BASE/.venv/bin/python" - <<'PY'
import os, sys
base = os.environ['BASE']
sys.path.insert(0, base)
from app.main import SessionLocal, write_mapping_json, set_mapping_version
db = SessionLocal(); set_mapping_version(db); write_mapping_json(db)
print("OK: mapping.json rebuilt & version bumped")
PY
ok "映射文件重建完成"

# ---------------- 9) UFW 放行（如启用且对外监听） ----------------
step "9) 防火墙放行（若 UFW=active 且 HOST=0.0.0.0）"
if command -v ufw >/dev/null 2>&1 && ufw status | grep -q "Status: active" && [ "$HOST" = "0.0.0.0" ]; then
  ufw allow "$PORT/tcp" || true
  ok "已放行端口 $PORT/tcp"
else
  warn "未放行端口（UFW 未启用或 HOST 非 0.0.0.0）"
fi

# ---------------- 10) 健康检查 ----------------
step "10) 健康检查"
sleep 1
if curl -fsS "http://127.0.0.1:$PORT/admin/login" | head -n 1 >/dev/null; then
  ok "服务健康：本机 127.0.0.1:$PORT 可访问"
else
  warn "健康检查未通过，请用下方日志命令排查"
fi

echo
ok "部署完成 ✅"
echo "后台： http://<服务器IP>:$PORT/admin"
echo "首次： /admin/bootstrap"
echo "日志： journalctl -u huandan.service -e -n 200"
echo "安装日志： $INSTALL_LOG"
