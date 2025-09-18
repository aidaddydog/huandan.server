#!/usr/bin/env bash
# 作用：创建/升级 Python 虚拟环境，并从正确的 requirements.txt 安装依赖
# 说明：修复了原脚本路径多跳一层的问题（从 scripts/deploy 回到仓库根应为 "$DIR/.."，而不是 "$DIR/../.."）
set -Eeuo pipefail

# ========== 计算脚本所在目录的上一级（即仓库根的 scripts/）==========
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"/.. && pwd)"

# 公共函数与环境变量（step/ok/die/load_env/require_env 等）
# common.sh 内应已提供中文进度输出与错误处理
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

# 4) 正确定位 requirements.txt
#    仅回退一级到仓库根目录（/opt/huandan），避免误跳到 /opt
REPO_ROOT="$(cd "$DIR/.." && pwd)"

# 优先使用仓库根的 requirements.txt；若不存在，则尝试 app/requirements.txt
REQ_FILE=""
if [[ -f "$REPO_ROOT/requirements.txt" ]]; then
  REQ_FILE="$REPO_ROOT/requirements.txt"
elif [[ -f "$REPO_ROOT/app/requirements.txt" ]]; then
  REQ_FILE="$REPO_ROOT/app/requirements.txt"
else
  die "未找到依赖文件：$REPO_ROOT/requirements.txt 或 $REPO_ROOT/app/requirements.txt
请确认仓库中存在 requirements.txt。若不确定，可执行：
  ls -l $REPO_ROOT/requirements.txt
  ls -l $REPO_ROOT/app/requirements.txt

如需调试本步骤日志，可执行（查看最后200行）：
  tail -n 200 /var/log/huandan-deploy.log  # 一键查看部署日志"
fi

echo "将使用依赖文件：$REQ_FILE"
pip install -r "$REQ_FILE"

ok "Python 依赖安装完成"
