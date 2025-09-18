#!/usr/bin/env bash
# scripts/bootstrap_online.sh
# 在线从零安装（新机器一行命令用）
set -Eeuo pipefail

REPO_URL="${REPO_URL:-https://github.com/aidaddydog/huandan.server.git}"
BRANCH="${BRANCH:-main}"
BASE="${BASE:-/opt/huandan-server}"

# 这几个默认最终也会进入 .deploy.env（如已有则不覆盖）
PORT_DEFAULT="${PORT_DEFAULT:-8000}"
HOST_DEFAULT="${HOST_DEFAULT:-0.0.0.0}"
AUTO_CLEAN_DEFAULT="${AUTO_CLEAN_DEFAULT:-no}"

apt-get update -y
apt-get install -y git curl python3-venv python3-pip ufw

mkdir -p "$(dirname "$BASE")"
if [ -d "$BASE/.git" ]; then
  git -C "$BASE" fetch --all --prune || true
  (git -C "$BASE" checkout "$BRANCH" 2>/dev/null || true)
  git -C "$BASE" pull --ff-only || true
else
  git clone -b "$BRANCH" "$REPO_URL" "$BASE"
fi

cd "$BASE"
mkdir -p scripts

# 写默认配置（若仓库内还没有 .deploy.env）
if [ ! -f .deploy.env ]; then
  cat > .deploy.env <<ENV
PORT=$PORT_DEFAULT
HOST=$HOST_DEFAULT
AUTO_CLEAN=$AUTO_CLEAN_DEFAULT
BRANCH=$BRANCH
REPO=$REPO_URL
DATA=/opt/huandan-data
SECRET_KEY=please-change-me
# BASE 默认自动识别为当前仓库根目录
ENV
fi

chmod +x scripts/install_root.sh
bash scripts/install_root.sh
