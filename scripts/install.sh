#!/usr/bin/env bash
# =============================================================
# Huandan Server 一键部署脚本（脚本内含中文释义与进度提示）
# 适配：Ubuntu 24.x（默认 24.04 LTS）
# 运行：root（建议以专用用户 huandan 运行服务）
#
# 支持的环境变量（可选）：
#   REPO=""            # 若服务器上尚未有代码，提供 Git 仓库地址即可自动 clone
#   BRANCH="main"      # clone 的分支，默认 main
#   BASE="/opt/huandan-server"   # 代码目录
#   DATA="/opt/huandan-data"     # 数据目录（pdfs/uploads）
#   PORT="8000"        # 服务端口
#   HOST="0.0.0.0"     # 监听地址（为 0.0.0.0 时将考虑放行 UFW 端口）
#   PYBIN="python3"    # Python 解释器
#   AUTO_CLEAN=""      # 覆盖安装：yes 静默备份覆盖；no 就地更新；空=交互询问
#   ENABLE_DANGER="0"  # 1=注入“危险清空”端点与按钮（默认 0 关闭）
# =============================================================
set -Eeuo pipefail

# ---------------- 变量默认值 ----------------
REPO="${REPO:-}"
BRANCH="${BRANCH:-main}"
BASE="${BASE:-/opt/huandan-server}"
DATA="${DATA:-/opt/huandan-data}"
PORT="${PORT:-8000}"
HOST="${HOST:-0.0.0.0}"
PYBIN="${PYBIN:-python3}"
AUTO_CLEAN="${AUTO_CLEAN:-}"
ENABLE_DANGER="${ENABLE_DANGER:-0}"

TS="$(date +%Y%m%d-%H%M%S)"
LOG_DIR="/var/log/huandan"
INSTALL_LOG="$LOG_DIR/install-$TS.log"
BACKUP_ROOT="/opt/huandan-backups"
BACKUP_DIR="$BACKUP_ROOT/$TS"
mkdir -p "$LOG_DIR" "$BACKUP_ROOT"

# ---------------- 进度/输出 ----------------
TOTAL=12
STEP=0
step(){ STEP=$((STEP+1)); echo -e "==[$STEP/$TOTAL] $*"; }
ok(){ echo -e "✔ $*"; }
warn(){ echo -e "⚠ $*"; }
err(){ echo -e "✘ $*"; }

on_err(){
  err "安装失败（第 $STEP 步）。详细日志：$INSTALL_LOG"
  echo "journalctl -u huandan.service -e -n 200   # 一键查看服务日志"
  exit 1
}
trap 'on_err' ERR

# 将输出同时写入日志文件
exec > >(tee -a "$INSTALL_LOG") 2>&1

echo "Huandan 一键部署启动 @ $TS"
echo "BASE=$BASE DATA=$DATA PORT=$PORT HOST=$HOST REPO=${REPO:-<none>} ENABLE_DANGER=$ENABLE_DANGER"

# ---------------- 0. 前置检查 ----------------
step "前置检查（root 与网络）"
if [ "$(id -u)" -ne 0 ]; then err "请使用 root 运行"; exit 1; fi
ok "前置检查通过"

# ---------------- 1. 安装系统依赖 ----------------
step "安装系统依赖（git/python/ufw 等）"
export DEBIAN_FRONTEND=noninteractive
apt-get update -y
apt-get install -y --no-install-recommends \
  git curl ca-certificates tzdata openssh-server \
  python3-venv python3-pip rsync unzip ufw
ok "依赖安装完成"

# ---------------- 2. 创建专用用户与目录 ----------------
step "创建专用用户与目录（非 root 运行服务）"
id -u huandan >/dev/null 2>&1 || adduser --disabled-password --gecos "" huandan
install -d -m 755 "$BASE" "$DATA/pdfs" "$DATA/uploads"
chown -R huandan:huandan "$BASE" "$DATA"
ok "用户/目录就绪（huandan）"

# ---------------- 3. 代码获取或更新 ----------------
step "获取/更新代码（Git）"
if [ -d "$BASE/.git" ]; then
  sudo -u huandan -H bash -lc "cd '$BASE' && git pull --ff-only"
elif [ -n "$REPO" ]; then
  sudo -u huandan -H bash -lc "git clone -b '$BRANCH' '$REPO' '$BASE'"
  ok "已 clone $REPO@$BRANCH → $BASE"
else
  warn "未检测到 .git 且未提供 REPO，假定代码已就位（如为首次部署请设置 REPO=…）"
fi
ok "代码准备完成"

# ---------------- 4. 备份与覆盖安装策略 ----------------
step "备份与覆盖安装策略"
DO_CLEAN="$AUTO_CLEAN"
if [ -z "$DO_CLEAN" ] && [ -t 0 ]; then
  read -r -p "是否『备份并覆盖安装』？(y/N) " yn || true
  DO_CLEAN=$([[ "$yn" =~ ^[Yy]$ ]] && echo "yes" || echo "no")
fi
if [ "${DO_CLEAN:-no}" = "yes" ]; then
  systemctl stop huandan.service 2>/dev/null || true
  mkdir -p "$BACKUP_DIR"
  rsync -a --delete --exclude='.venv' "$BASE/" "$BACKUP_DIR/huandan-server/" 2>/dev/null || true
  rsync -a "$DATA/" "$BACKUP_DIR/huandan-data/" 2>/dev/null || true
  rm -rf "$BASE"
  sudo -u huandan -H bash -lc "mkdir -p '$BASE'"
  ok "已备份到：$BACKUP_DIR，并清理旧版本目录"
else
  ok "选择就地更新（不会删除目录）"
fi

# ---------------- 5. Python 虚拟环境与依赖 ----------------
step "创建/更新 Python 虚拟环境并安装依赖"
sudo -u huandan -H bash -lc "
  cd '$BASE'
  $PYBIN -m venv .venv
  source .venv/bin/activate
  pip install -U pip wheel
  if [ -f requirements.txt ]; then
    pip install -r requirements.txt
  else
    pip install 'uvicorn[standard]' fastapi jinja2 'sqlalchemy<2.0' 'passlib[bcrypt]' pandas openpyxl 'xlrd==1.2.0' aiofiles itsdangerous python-multipart
  fi
"
ok "Python 依赖安装完成"

# ---------------- 6. 可选：注入危险清空端点 ----------------
step "（可选）注入『危险清空』端点（ENABLE_DANGER=$ENABLE_DANGER）"
if [ "$ENABLE_DANGER" = "1" ]; then
  sudo -u huandan -H bash -lc "
    python3 - <<'PY'
import os, re
base=os.environ.get('BASE','${BASE}')
fp=os.path.join(base,'app','main.py')
s=open(fp,'r',encoding='utf-8').read()
code=r'''
# ------------------ DANGER ZONE：高危清空操作 ------------------
@app.post("/admin/danger/wipe_pdfs")
def danger_wipe_pdfs(request: Request, confirm: str = Form(""), db=Depends(get_db)):
    require_admin(request, db)
    if (confirm or "").strip() != "DELETE ALL PDF":
        return RedirectResponse("/admin/files?danger=badconfirm", status_code=302)
    removed_files = 0
    try:
        for name in os.listdir(PDF_DIR):
            if name.lower().endswith(".pdf"):
                fp = os.path.join(PDF_DIR, name)
                if os.path.isfile(fp):
                    try:
                        os.remove(fp); removed_files += 1
                    except Exception: pass
    except Exception: pass
    removed_rows = db.query(TrackingFile).delete()
    db.commit()
    set_mapping_version(db); write_mapping_json(db)
    return RedirectResponse(f"/admin/files?danger=pdfs_cleared&files={removed_files}&rows={removed_rows}", status_code=302)

@app.post("/admin/danger/wipe_orders")
def danger_wipe_orders(request: Request, confirm: str = Form(""), db=Depends(get_db)):
    require_admin(request, db)
    if (confirm or "").strip() != "DELETE ALL ORDERS":
        return RedirectResponse("/admin/orders?danger=badconfirm", status_code=302)
    removed = db.query(OrderMapping).delete()
    db.commit()
    set_mapping_version(db); write_mapping_json(db)
    return RedirectResponse(f"/admin/orders?danger=orders_cleared&rows={removed}", status_code=302)
'''
if 'def danger_wipe_pdfs(' not in s:
    open(fp,'w',encoding='utf-8').write(s+'\n'+code+'\n')
PY
  "
  ok "已注入危险端点（页面将出现确认输入框与按钮）"
else
  ok "跳过危险端点注入（如需：ENABLE_DANGER=1）"
fi

# ---------------- 7. 写入 systemd 单元并启动 ----------------
step "写入 systemd 单元并启动服务"
cat > /etc/systemd/system/huandan.service <<UNIT
[Unit]
Description=Huandan Server (FastAPI)
After=network.target

[Service]
Environment=HUANDAN_BASE=$BASE
Environment=HUANDAN_DATA=$DATA
Environment=PORT=$PORT
Environment=HOST=$HOST
Environment=PYTHONUNBUFFERED=1
WorkingDirectory=$BASE
ExecStart=$BASE/.venv/bin/python $BASE/run.py
Restart=always
User=huandan
Group=huandan

[Install]
WantedBy=multi-user.target
UNIT

systemctl daemon-reload
systemctl enable --now huandan.service
systemctl --no-pager -l status huandan.service | sed -n '1,60p'
ok "systemd 已启用并启动"

# ---------------- 8. 重建 mapping.json （可选但推荐） ----------------
step "重建 mapping.json（刷新列表版本号）"
sudo -u huandan -H bash -lc "
  cd '$BASE'
  $BASE/.venv/bin/python - <<'PY'
import os, sys
base=os.environ.get('BASE','${BASE}')
sys.path.insert(0, base)
from app.main import SessionLocal, write_mapping_json, set_mapping_version
db=SessionLocal(); set_mapping_version(db); write_mapping_json(db)
print('OK: mapping.json rebuilt & version bumped')
PY
"
ok "映射文件已重建"

# ---------------- 9. 防火墙放行（UFW 已启用且对外监听时） ----------------
step "防火墙放行（条件：UFW=active 且 HOST=0.0.0.0）"
if command -v ufw >/dev/null 2>&1 && ufw status | grep -q "Status: active" && [ "$HOST" = "0.0.0.0" ]; then
  ufw allow "$PORT/tcp" || true
  ok "已放行端口 $PORT/tcp"
else
  warn "未放行端口（UFW 未启用或 HOST 非 0.0.0.0）"
fi

# ---------------- 10. 健康检查 ----------------
step "健康检查（HTTP 200/HTML）"
sleep 1
if curl -fsS "http://127.0.0.1:$PORT/admin/login" | head -n 1 >/dev/null; then
  ok "服务健康：本机 127.0.0.1:$PORT 可访问"
else
  warn "健康检查未通过，请用日志命令排查"
fi

# ---------------- 11. 输出关键信息 ----------------
step "部署完成，关键信息"
echo "后台地址：   http://<服务器IP>:$PORT/admin"
echo "首次初始化： http://<服务器IP>:$PORT/admin/bootstrap"
echo "数据目录：   $DATA  （pdfs/uploads）"
echo "服务日志：   journalctl -u huandan.service -e -n 200"
echo "安装日志：   $INSTALL_LOG"

# ---------------- 12. 结束 ----------------
ok "全部完成"
exit 0
