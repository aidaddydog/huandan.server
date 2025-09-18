#!/usr/bin/env bash
# Huandan 在线一键部署引导（只需运行：bash <(curl -fsSL https://raw.githubusercontent.com/aidaddydog/huandan.server/main/scripts/bootstrap_online.sh)）
set -Eeuo pipefail

LOG=/var/log/huandan-bootstrap.log
exec > >(tee -a "$LOG") 2>&1

: "${BRANCH:=main}"
: "${REPO:=https://github.com/aidaddydog/huandan.server.git}"
: "${DEST:=/opt/huandan-server}"

step(){ echo "==> $*"; }
ok(){ echo "✔ $*"; }
die(){ echo "✘ $*"; exit 1; }
trap 'die "失败，详见 $LOG （或：journalctl -u huandan.service -e -n 200）"' ERR

[ "$(id -u)" -eq 0 ] || die "请用 root 运行"

step "安装系统依赖"
export DEBIAN_FRONTEND=noninteractive
apt-get update -y
apt-get install -y --no-install-recommends git curl ca-certificates tzdata python3-venv python3-pip ufw rsync unzip

step "获取代码到 $DEST（分支：$BRANCH）"
if [ -d "$DEST/.git" ]; then
  git -C "$DEST" fetch --all --prune
  git -C "$DEST" checkout "$BRANCH" || true
  git -C "$DEST" reset --hard "origin/$BRANCH"
  git -C "$DEST" clean -fd
else
  rm -rf "$DEST"
  git clone -b "$BRANCH" "$REPO" "$DEST"
fi
ok "代码准备完成"

step "准备 /etc/huandan.env"
if [ ! -f /etc/huandan.env ]; then
  install -Dm644 "$DEST/config/env/huandan.env.example" /etc/huandan.env
  ok "已写入 /etc/huandan.env（默认端口 8000，直出模式）"
else
  ok "/etc/huandan.env 已存在，保持不变"
fi

step "执行模块化部署（非交互）"
# 给 03-sync-app.sh 的两个提问喂两个空行 => 采用默认：备份=Y，清理=N
printf "\n\n" | bash "$DEST/scripts/deploy/deploy_all.sh"

ok "完成。后台：http://<服务器IP>:8000/admin  首次初始化：/admin/bootstrap"
