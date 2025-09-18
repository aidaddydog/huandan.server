#!/usr/bin/env bash
set -Eeuo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPTS_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_ROOT="$(cd "$SCRIPTS_ROOT/.." && pwd)"
source "$SCRIPTS_ROOT/lib/common.sh"
load_env
require_env HUANDAN_BASE HUANDAN_DATA

step "同步应用文件（支持备份与清理）"
read -r -p "是否对现有 ${HUANDAN_BASE} 做一次备份？(Y/n): " a; a=${a:-Y}
if [[ "$a" =~ ^[Yy]$ ]]; then
  ts="$(date +%Y%m%d%H%M%S)"
  tar czf "/root/huandan-backup-${ts}.tgz" -C "$(dirname "$HUANDAN_BASE")" "$(basename "$HUANDAN_BASE")" || true
  ok "已备份到 /root/huandan-backup-${ts}.tgz"
fi

read -r -p "是否清理可再生内容（venv、__pycache__）后再同步？(y/N): " b; b=${b:-N}
if [[ "$b" =~ ^[Yy]$ ]]; then
  rm -rf "$HUANDAN_BASE/.venv" "$HUANDAN_BASE"/**/__pycache__ 2>/dev/null || true
  ok "已清理可再生内容"
fi

rsync -av --delete   "$REPO_ROOT/src/" "$HUANDAN_BASE/"   --exclude ".venv"   --exclude "__pycache__"   | tee -a "$LOG"

chown -R huandan:huandan "$HUANDAN_BASE"
ok "应用文件同步完成"
