#!/usr/bin/env bash
set -e
echo ">>> [1/12] 加载配置并准备目录..."
DEPLOY_ENV_FILE="$(dirname "$0")/../.deploy.env"
if [ -f "$DEPLOY_ENV_FILE" ]; then set -a; source "$DEPLOY_ENV_FILE"; set +a; fi
APP_DIR="$(cd "$(dirname "$0")/.."; pwd)"
mkdir -p "$APP_DIR/data" "$APP_DIR/storage/pdfs" "$APP_DIR/updates/client" "$APP_DIR/updates/jobs"
sudo mkdir -p "${LOG_DIR:-/var/log/huandan}" || true
sudo chown -R $USER:$USER "${LOG_DIR:-/var/log/huandan}" || true
echo ">>> [2/12] 安装依赖..."
sudo apt-get update -y && sudo apt-get install -y python3-venv python3-pip
echo ">>> [3/12] 创建虚拟环境并安装依赖..."
python3 -m venv "$APP_DIR/.venv"
source "$APP_DIR/.venv/bin/activate"
pip install --upgrade pip && pip install -r "$APP_DIR/requirements.txt"
echo ">>> [4/12] 初始化默认数据文件..."
[ -f "$APP_DIR/data/mapping.json" ] || echo '[]' > "$APP_DIR/data/mapping.json"
[ -f "$APP_DIR/updates/client/latest.json" ] || echo '{"version":"v0.0.0","url":"","notes":"","force":false}' > "$APP_DIR/updates/client/latest.json"
echo ">>> [5/12] 生成 systemd 单元..."
SERVICE_FILE="/etc/systemd/system/huandan.service"
sudo bash -c "cat > $SERVICE_FILE" <<EOF
[Unit]
Description=Huandan Server (FastAPI)
After=network.target
[Service]
Type=simple
WorkingDirectory=$APP_DIR
Environment=APP_HOST=${APP_HOST:-0.0.0.0}
Environment=APP_PORT=${APP_PORT:-8000}
ExecStart=$APP_DIR/.venv/bin/uvicorn app.main:app --host \$APP_HOST --port \$APP_PORT
Restart=always
RestartSec=3
StandardOutput=append:${LOG_DIR:-/var/log/huandan}/huandan.out.log
StandardError=append:${LOG_DIR:-/var/log/huandan}/huandan.err.log
[Install]
WantedBy=multi-user.target
EOF
echo ">>> [6/12] 启动服务..."
sudo systemctl daemon-reload
sudo systemctl enable huandan.service
sudo systemctl restart huandan.service
echo ">>> [7/12] 放行端口（UFW 可选）..."
if command -v ufw >/dev/null 2>&1; then sudo ufw allow ${APP_PORT:-8000}/tcp || true; fi
echo ">>> [8/12] 健康检查（/health）..."
sleep 2
curl -fsS "http://127.0.0.1:${APP_PORT:-8000}/health" >/dev/null && echo "健康检查通过" || echo "（提示）健康检查暂未通过，可稍等再试或查看日志"
echo ">>> [9/12] 访问入口: http://$(hostname -I | awk '{print $1}'):${APP_PORT:-8000}/"
echo ">>> [10/12] 服务日志：journalctl -u huandan.service -e -n 200"
echo ">>> [11/12] Nginx 反代：使用 bootstrap_online.sh --with-nginx 自动配置"
echo ">>> [12/12] 完成"

