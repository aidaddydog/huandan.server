#!/usr/bin/env bash
set -Eeuo pipefail
echo -e "\n=== Huandan QuickStart ==="
if [ ! -f /etc/huandan.env ]; then
  echo "未检测到 /etc/huandan.env，正在拷贝示例配置..."
  sudo cp config/env/huandan.env.example /etc/huandan.env
  echo "已复制示例配置到 /etc/huandan.env（请按需修改端口/目录/SESSION_SECRET）。"
fi
echo "开始一键部署..."
sudo bash scripts/deploy/deploy_all.sh
