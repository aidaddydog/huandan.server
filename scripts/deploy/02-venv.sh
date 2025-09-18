#!/usr/bin/env bash
# 作用：创建/升级 Python 虚拟环境，并从正确的 requirements.txt 安装依赖
# 说明：修复了原脚本路径多跳一层的问题（从 scripts/deploy 回到仓库根应为 "$DIR/.."）
set -Eeuo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"/.. && pwd)"   # => /opt/huandan/scripts
source "$DIR/lib/common.sh"
load_env
require_env HUANDAN_BASE PYBIN

step "创建/升级 Python 虚拟环境并安装依赖"

# 1) 创建虚拟环境（如不存在）
if [[ ! -d "$HUANDAN_BASE/.venv" ]]; then
  "$PYBIN" -m venv "$HUANDAN_BASE/.venv"
fi

# 2) 激活虚拟环境
# shellcheck disable=SC1091
source "$HUANDAN_BASE/.venv/bin/activate"

# 3) 升级基础工具
python -m pip install -U pip wheel

# 4) 正确定位 requirements.txt（仓库根或 app/）
REPO_ROOT="$(cd "$DIR/.." && pwd)"  # => /opt/huandan
REQ_FILE=""
if [[ -f "$REPO_ROOT/requirements.txt" ]]; then
  REQ_FILE="$REPO_ROOT/requirements.txt"
elif [[ -f "$REPO_ROOT/app/requirements.txt" ]]; then
  REQ_FILE="$REPO_ROOT/app/requirements.txt"
else
  die "未找到依赖文件：$REPO_ROOT/requirements.txt 或 $REPO_ROOT/app/requirements.txt
如需查看部署日志（最后200行）：
  tail -n 200 /var/log/huandan-deploy.log"
fi

echo "将使用依赖文件：$REQ_FILE"
pip install -r "$REQ_FILE"

ok "Python 依赖安装完成"
