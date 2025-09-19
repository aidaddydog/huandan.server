#!/usr/bin/env bash
# 在线一键安装（与历史命令一致）
set -euo pipefail
REPO="${REPO:-aidaddydog/huandan.server}"
BRANCH="${BRANCH:-main}"
APP_PORT="${APP_PORT:-8000}"
INSTALL_DIR="${INSTALL_DIR:-/opt/huandan}"
SERVICE_NAME="${SERVICE_NAME:-huandan}"
WITH_NGINX="${WITH_NGINX:-0}"

echo ">>> Bootstrap: repo=$REPO branch=$BRANCH port=$APP_PORT dir=$INSTALL_DIR service=$SERVICE_NAME nginx=$WITH_NGINX"
sudo apt-get update -y
sudo apt-get install -y git curl python3-venv python3-pip

APP_HOME="$INSTALL_DIR/src"
if [[ -d "$APP_HOME/.git" ]]; then
  echo ">>> 更新仓库 $APP_HOME"
  sudo git -C "$APP_HOME" fetch --all --prune
  sudo git -C "$APP_HOME" checkout "$BRANCH"
  sudo git -C "$APP_HOME" pull --ff-only origin "$BRANCH"
else
  echo ">>> 克隆仓库到 $APP_HOME"
  sudo mkdir -p "$INSTALL_DIR"
  sudo git clone -b "$BRANCH" "https://github.com/$REPO.git" "$APP_HOME"
fi
sudo chown -R $USER:$USER "$INSTALL_DIR"

cd "$APP_HOME"
if [[ ! -f ".deploy.env" ]]; then
  cat > .deploy.env <<EOF
APP_NAME="$SERVICE_NAME"
APP_PORT=$APP_PORT
APP_HOST="0.0.0.0"
APP_ENV="prod"
DATA_DIR="$INSTALL_DIR/data"
STORAGE_DIR="$INSTALL_DIR/storage"
UPDATES_DIR="$INSTALL_DIR/updates"
LOG_DIR="/var/log/$SERVICE_NAME"
EOF
fi

bash scripts/install.sh

if [[ "$WITH_NGINX" == "1" ]]; then
  echo ">>> 安装 Nginx 反代"
  sudo apt-get install -y nginx
  sudo bash -c "cat > /etc/nginx/sites-available/${SERVICE_NAME}.conf" <<NGX
server {
  listen 80;
  server_name _;
  location / {
    proxy_pass http://127.0.0.1:${APP_PORT};
    proxy_set_header Host \$host;
    proxy_set_header X-Real-IP \$remote_addr;
    proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto \$scheme;
  }
}
NGX
  sudo ln -sf /etc/nginx/sites-available/${SERVICE_NAME}.conf /etc/nginx/sites-enabled/${SERVICE_NAME}.conf
  sudo nginx -t && sudo systemctl restart nginx
fi

echo ">>> 完成： http://$(hostname -I | awk '{print $1}'):${APP_PORT}/  （健康检查：/health）"

