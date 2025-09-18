#!/usr/bin/env bash
set -Eeuo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPTS_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
# shellcheck disable=SC1090
source "$SCRIPTS_ROOT/lib/common.sh"
load_env
require_env HUANDAN_BASE HUANDAN_DATA PORT

step "安装系统依赖 & 准备目录"
apt_noninteractive
apt-get update -y
apt-get install -y --no-install-recommends tzdata curl unzip ca-certificates python3-venv rsync
ensure_user_group
ok "系统依赖与目录就绪"
