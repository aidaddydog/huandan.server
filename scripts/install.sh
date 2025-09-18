#!/usr/bin/env bash
# =============================================================
# Huandan Server 一键部署脚本（中文进度 + 日志 + 覆盖更新 + systemd）
# 适配：Ubuntu 24.04 LTS（其他 Debian/Ubuntu 类似）
#
# 支持环境变量（可在命令前设置或用 env 传入）：
#   REPO=""              # Git 仓库地址（首次部署或需强制拉取时设置）
#   BRANCH="main"        # 拉取分支，默认 main
#   BASE="/opt/huandan-server"   # 代码目录
#   DATA="/opt/huandan-data"     # 数据目录（pdfs/uploads）
#   PORT="8000"          # 监听端口
#   HOST="0.0.0.0"       # 监听地址（为 0.0.0.0 时可放行 UFW）
#   PYBIN="python3"      # Python 解释器
#   SECRET_KEY="please-change-me" # FastAPI 会话密钥
#   AUTO_CLEAN=""        # yes=备份并覆盖；no=就地更新；空=交互询问
#   ENABLE_DANGER="0"    # 1=注入“危险清空”端点与按钮（默认 0 关闭）
# =============================================================
set -Eeuo pipefail

# ---------- 变量与默认值 ----------
REPO="${REPO:-}"
BRANCH="${BRANCH:-main}"
BASE="${BASE:-/opt/huandan-server}"
DATA="${DATA:-/opt/huandan-data}"
PORT="${PORT:-8000}"
HOST="${HOST:-0.0.0.0}"
PYBIN="${PYBIN:-python3}"
SECRET_KEY="${SECRET_KEY:-please-change-me}"
AUTO_CLEAN="${AUTO_CLEAN:-}"
ENABLE_DANGER="${ENABLE_DANGER:-0}"

TS="$(date +%Y%m%d-%H%M%S)"
LOG_DIR="/var/log/huandan"
INSTALL_LOG="$LOG_DIR/install-$TS.log"
BACKUP_ROOT="/opt/huandan-backups"
BACKUP_DIR="$BACKUP_ROOT/$TS"

mkdir -p "$LOG_DIR" "$BACKUP_ROOT"

# ---------- 输出与错误处理 ----------
TOTAL=11
STEP=0
step(){ STEP=$((STEP+1)); echo -e "==[$STEP/$TOTAL] $*"; }
ok(){ echo -e "✔ $*"; }
warn(){ echo -e "⚠ $*"; }
fail(){ echo -e "✘ $*"; exit 1; }

on_err(){
  echo "✘ 安装失败（第 $STEP 步）。详细日志：$INSTALL_LOG"
  echo "journalctl -u huandan.service -e -n 200   # 一键查看服务日志"
  exit 1
}
trap 'on_err' ERR

# 将输出同时写入日志文件
exec > >(tee -a "$INSTALL_LOG") 2>&1

echo "Huandan 一键部署启动 @ $TS"
echo "BASE=$BASE DATA=$DATA PORT=$PORT HOST=$HOST REPO=${REPO:-<none>} BRANCH=$BRANCH ENABLE_DANGER=$ENABLE_DANGER"

# ---------- 1. 前置检查 ----------
step "前置检查（root 与网络）"
[ "$(id -u)" -eq 0 ] || fail "请使用 root 运行"
ok "前置检查通过"

# ---------- 2. 系统依赖 ----------
step "安装系统依赖（git/python/ufw 等）"
export DEBIAN_FRONTEND=noninteractive
apt-get update -y
apt-get install -y --no-install-recommends \
  git curl ca-certificates tzdata openssh-server \
  python3-venv python3-pip rsync unzip ufw
ok "依赖安装完成"

# ---------- 3. 专用用户与目录 ----------
step "创建专用用户与目录（非 root 运行服务）"
id -u huandan >/dev/null 2>&1 || adduser --disabled-password --gecos "" huandan
install -d -m 755 "$BASE" "$DATA/pdfs" "$DATA/uploads"
chown -R huandan:huandan "$BASE" "$DATA"
ok "用户/目录就绪（huandan）"

# ---------- 4. 备份与覆盖策略 ----------
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
  install -d -m 755 "$BASE"
  chown -R huandan:huandan "$BASE"
  ok "已备份到：$BACKUP_DIR，并清理 $BASE"
else
  ok "选择就地更新（不删除现有目录）"
fi

# ---------- 5. 获取/更新代码（Git） ----------
step "获取/更新代码（Git）"
is_empty_dir(){ [ -z "$(ls -A "$1" 2>/dev/null)" ]; }

if [ -d "$BASE/.git" ]; then
  sudo -u huandan -H bash -lc "cd '$BASE' && git fetch --all --prune && (git checkout '$BRANCH' 2>/dev/null || true) && git pull --ff-only || true"
elif [ -n "$REPO" ]; then
  if is_empty_dir "$BASE"; then
    sudo -u huandan -H bash -lc "git clone -b '$BRANCH' '$REPO' '$BASE'"
    ok "已 clone $REPO@$BRANCH → $BASE"
  else
    TMPDIR="$(mktemp -d)"
    chown -R huandan:huandan "$TMPDIR"
    sudo -u huandan -H bash -lc "git clone -b '$BRANCH' '$REPO' '$TMPDIR'"
    rsync -a "$TMPDIR/". "$BASE/"
    rm -rf "$TMPDIR"
    ok "已在非空目录就地合并更新（临时 clone + rsync）"
  fi
else
  warn "未检测到 .git 且未提供 REPO，假定代码已就位"
fi
chown -R huandan:huandan "$BASE" "$DATA"
ok "代码准备完成"

# ---------- 6. Python 虚拟环境与依赖 ----------
step "创建/更新 Python 虚拟环境并安装依赖"
sudo -u huandan -H bash -lc "
  set -Eeuo pipefail
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

# ---------- 7. 可选：注入“危险清空”端点与按钮 ----------
step "（可选）注入『危险清空』端点（ENABLE_DANGER=$ENABLE_DANGER）"
if [ "$ENABLE_DANGER" = "1" ]; then
  sudo -u huandan -H bash -lc "
    python3 - <<'PY'
import os
fp=os.path.join('${BASE}','app','main.py')
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
  # 同步在页面加入危险按钮（带确认）
  sudo -u huandan -H bash -lc "
    python3 - <<'PY'
import os
root='${BASE}'
def patch(tpl, marker, inj):
    fp=os.path.join(root,'app','templates',tpl)
    s=open(fp,'r',encoding='utf-8').read()
    if marker in s: return
    s=s.replace('<h2>PDF 列表</h2>' if tpl=='files.html' else '<h2>订单列表</h2>', 
                ('<h2>PDF 列表</h2>' if tpl=='files.html' else '<h2>订单列表</h2>')+'\n'+inj, 1)
    open(fp,'w',encoding='utf-8').write(s)

inj_files = '''
<form method="post" action="/admin/danger/wipe_pdfs" class="row" onsubmit="return confirm('⚠️ 危险操作：将删除服务器上所有 PDF 文件及其数据库记录，且不可恢复。确定继续？')">
  <input name="confirm" placeholder="输入 DELETE ALL PDF 以确认" style="flex:1">
  <button type="submit" class="danger">危险：清空所有 PDF</button>
</form>
'''
inj_orders = '''
<form method="post" action="/admin/danger/wipe_orders" class="row" onsubmit="return confirm('⚠️ 危险操作：将删除全部订单映射（不影响 PDF 文件）。确定继续？')">
  <input name="confirm" placeholder="输入 DELETE ALL ORDERS 以确认" style="flex:1">
  <button type="submit" class="danger">危险：清空全部订单映射</button>
</form>
'''

patch('files.html','/admin/danger/wipe_pdfs', inj_files)
patch('orders.html','/admin/danger/wipe_orders', inj_orders)
PY
  "
  ok "已注入危险端点与页面按钮（带确认输入）"
else
  ok "跳过危险端点注入（如需：ENABLE_DANGER=1）"
fi

# ---------- 8. systemd ----------
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
Environment=SECRET_KEY=$SECRET_KEY
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

# ---------- 9. 重建 mapping.json ----------
step "重建 mapping.json（刷新列表版本号）"
sudo -u huandan -H env BASE="$BASE" HUANDAN_DATA="$DATA" "$BASE/.venv/bin/python" - <<'PY'
import os, sys
base = os.environ['BASE']
sys.path.insert(0, base)
from app.main import SessionLocal, write_mapping_json, set_mapping_version
db = SessionLocal(); set_mapping_version(db); write_mapping_json(db)
print("OK: mapping.json rebuilt & version bumped")
PY
ok "映射文件已重建"

# ---------- 10. 防火墙 ----------
step "防火墙放行（条件：UFW=active 且 HOST=0.0.0.0）"
if command -v ufw >/dev/null 2>&1 && ufw status | grep -q "Status: active" && [ "$HOST" = "0.0.0.0" ]; then
  ufw allow "$PORT/tcp" || true
  ok "已放行端口 $PORT/tcp"
else
  warn "未放行端口（UFW 未启用或 HOST 非 0.0.0.0）"
fi

# ---------- 11. 健康检查 ----------
step "健康检查（HTTP 200/HTML）"
sleep 1
if curl -fsS "http://127.0.0.1:$PORT/admin/login" | head -n 1 >/dev/null; then
  ok "服务健康：本机 127.0.0.1:$PORT 可访问"
else
  warn "健康检查未通过，请用日志命令排查"
fi

echo
ok "部署完成 ✅"
echo "后台地址：   http://<服务器IP>:$PORT/admin"
echo "首次初始化： http://<服务器IP>:$PORT/admin/bootstrap"
echo "数据目录：   $DATA  （pdfs/uploads）"
echo "服务日志：   journalctl -u huandan.service -e -n 200"
echo "安装日志：   $INSTALL_LOG"
exit 0
