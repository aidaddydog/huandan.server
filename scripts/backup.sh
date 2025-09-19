#!/usr/bin/env bash
# 说明：备份代码与数据目录到 tar.gz（带中文提示）
set -Eeuo pipefail

BASE="${BASE:-/opt/huandan-server}"
DATA="${DATA:-/opt/huandan-data}"
OUT="${1:-/opt/huandan-backups/backup-$(date +%Y%m%d-%H%M%S).tar.gz}"

echo "==[1/2] 准备输出目录与参数 =="
mkdir -p "$(dirname "$OUT")"
echo "备份目标：$OUT"
echo "包含目录：$BASE  和  $DATA"

echo "==[2/2] 打包中（请稍候） =="
tar -czf "$OUT" -C / "$BASE" "${DATA#/}" 2>/dev/null
echo "✔ 备份完成：$OUT"
