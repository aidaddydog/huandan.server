#!/usr/bin/env bash
# Huandan Server 极简一键部署（root 直接运行服务）
# 用途：追求一步到位，少出错。安全性弱于专用用户方案。

set -Eeuo pipefail

# ===== 可调变量 =====
REPO="${REPO:-}"                    # 首次部署或想强制从 Git 拉取时填：https://github.com/<owner>/<repo>.git
BRANCH="${BRANCH:-main}"
BASE="${BASE:-/opt/huandan-server}" # 代码目录
DATA="${DATA:-/opt/huandan-data}"   # 数据目录（pdfs/uploads）
PORT="${PORT:-8000}"
HOST="${HOST:-0.0.0.0}"
PYBIN="${PYBIN:-python3}"
SECRET_KEY="${SECRET_KEY:-please-change-me}"
AUTO_CLEAN="${AUTO_CLEAN:-no}"      # yes=备份并覆盖；no=就地更新

TS="$(date +%Y%m%d-%H%M%S)"
LOG_DIR="/var/log/huandan"
INSTALL_LOG="$LOG_DIR/install-root-$TS.log"
BACKUP_ROOT="/opt/huandan-backups"
BACKUP_DIR="$BACKUP_ROOT/$TS"

mkdir -p "$LOG_DIR" "$BACKUP_ROOT"
exec > >(tee -a "$INSTALL_LOG") 2>&1

step(){ echo "==> $*"; }

step "1) 安装依赖"
export DEBIAN_FRONTEND=noninteractive
apt-get update -y
apt-get install -y --no-install-recommends git curl ca-certificates tzdata python3-venv python3-pip rsync unzip ufw

step "2) 目录就绪"
install -d -m 755 "$BASE" "$DATA/pdfs" "$DATA/uploads"

step "3) 备份策略：$AUTO_CLEAN"
if [ "$AUTO_CLEAN" = "yes" ] && [ -d "$BASE" ]; then
  systemctl stop huandan.service 2>/dev/null || true
  mkdir -p "$BACKUP_DIR"
  rsync -a --delete --exclude='.venv' "$BASE/" "$BACKUP_DIR/huandan-server/" 2>/dev/null || true
  rsync -a "$DATA/" "$BACKUP_DIR/huandan-data/" 2>/dev/null || true
  rm -rf "$BASE" && mkdir -p "$BASE"
  echo "已备份到：$BACKUP_DIR，并覆盖安装"
fi

step "4) 获取/更新代码"
is_empty_dir(){ [ -z "$(ls -A "$1" 2>/dev/null)" ]; }
if [ -d "$BASE/.git" ]; then
  (cd "$BASE" && git fetch --all --prune && (git checkout "$BRANCH" 2>/dev/null || true) && git pull --ff-only || true)
elif [ -n "${REPO}" ]; then
  if is_empty_dir "$BASE"; then
    git clone -b "$BRANCH" "$REPO" "$BASE"
  else
    tmp="$(mktemp -d)"; git clone -b "$BRANCH" "$REPO" "$tmp"; rsync -a "$tmp/". "$BASE/"; rm -rf "$tmp"
  fi
else
  echo "未检测到 .git 且未提供 REPO，假定代码已就位"
fi

step "5) Python 依赖"
cd "$BASE"
$PYBIN -m venv .venv
source .venv/bin/activate
pip install -U pip wheel
if [ -f requirements.txt ]; then
  pip install -r requirements.txt
else
  pip install 'uvicorn[standard]' fastapi jinja2 'sqlalchemy<2.0' 'passlib[bcrypt]' pandas openpyxl 'xlrd==1.2.0' aiofiles itsdangerous python-multipart
fi

step "6) 写入 systemd 并启动（root）"
cat > /etc/systemd/system/huandan.service <<UNIT
[Unit]
Description=Huandan Server (FastAPI)
After=network.target

[Service]
Environment=HUANDAN_BASE=$BASE
Environment=HUANDAN_DATA=$DATA
Environment=PORT=$PORT
Environment=HOST=$HOST
Environment=SECRET_KEY=$SECRET_KEY
Environment=PYTHONUNBUFFERED=1
WorkingDirectory=$BASE
ExecStart=$BASE/.venv/bin/python $BASE/run.py
Restart=always
User=root
Group=root

[Install]
WantedBy=multi-user.target
UNIT

systemctl daemon-reload
systemctl enable --now huandan.service
systemctl --no-pager -l status huandan.service | sed -n '1,60p'

step "7) 重建 mapping.json（修正 sys.path）"
env BASE="$BASE" HUANDAN_DATA="$DATA" "$BASE/.venv/bin/python" - <<'PY'
import os, sys
base = os.environ['BASE']
sys.path.insert(0, base)
from app.main import SessionLocal, write_mapping_json, set_mapping_version
db = SessionLocal(); set_mapping_version(db); write_mapping_json(db)
print("OK: mapping.json rebuilt & version bumped")
PY

step "8) UFW 放行（若已启用且对外监听）"
if command -v ufw >/dev/null 2>&1 && ufw status | grep -q "Status: active" && [ "$HOST" = "0.0.0.0" ]; then
  ufw allow "$PORT/tcp" || true
fi

step "9) 健康检查"
sleep 1
curl -fsS "http://127.0.0.1:$PORT/admin/login" | head -n 1 >/dev/null && echo "OK - 本机可访问"

echo
echo "✅ 部署完成"
echo "后台： http://<服务器IP>:$PORT/admin"
echo "初始化：/admin/bootstrap"
echo "日志： journalctl -u huandan.service -e -n 200"
echo "安装日志：$INSTALL_LOG"
