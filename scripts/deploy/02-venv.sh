#!/usr/bin/env bash
set -Eeuo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPTS_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_ROOT="$(cd "$SCRIPTS_ROOT/.." && pwd)"
source "$SCRIPTS_ROOT/lib/common.sh"
load_env
require_env HUANDAN_BASE PYBIN

step "创建/升级 Python 虚拟环境并安装依赖"
if [[ ! -d "$HUANDAN_BASE/.venv" ]]; then
  "$PYBIN" -m venv "$HUANDAN_BASE/.venv"
fi
# shellcheck disable=SC1091
source "$HUANDAN_BASE/.venv/bin/activate"
python -m pip install -U pip wheel
pip install -r "$REPO_ROOT/requirements.txt"
ok "Python 依赖安装完成"
