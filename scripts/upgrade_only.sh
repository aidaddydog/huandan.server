#!/usr/bin/env bash
set -euo pipefail
SERVICE_NAME="${SERVICE_NAME:-huandan}"
INSTALL_DIR="${INSTALL_DIR:-/opt/huandan}"
APP_HOME="${INSTALL_DIR}/src"
if [[ ! -d "$APP_HOME/.git" ]]; then echo "not found: $APP_HOME/.git"; exit 1; fi
echo ">>> 拉取最新代码..."
git -C "$APP_HOME" pull --ff-only
echo ">>> 重启服务..."
sudo systemctl restart ${SERVICE_NAME}.service
journalctl -u ${SERVICE_NAME}.service -e -n 50 --no-pager

