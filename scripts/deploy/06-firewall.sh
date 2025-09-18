#!/usr/bin/env bash
set -Eeuo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPTS_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
source "$SCRIPTS_ROOT/lib/common.sh"
load_env
require_env PORT EXPOSE_MODE

step "防火墙放行（按需）"
allow_port_if_needed
ok "防火墙步骤完成（如直出已放行端口）"
