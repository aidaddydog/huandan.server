#!/usr/bin/env bash
set -Eeuo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPTS_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
source "$SCRIPTS_ROOT/lib/common.sh"
load_env
require_env HUANDAN_BASE

step "重建映射 mapping.json 并刷新版本"
"$HUANDAN_BASE/.venv/bin/python" - <<'PY'
import sys, os
base=os.environ.get("HUANDAN_BASE","/opt/huandan-server")
sys.path.insert(0, base)
from app.main import SessionLocal, write_mapping_json, set_mapping_version
db=SessionLocal(); set_mapping_version(db); write_mapping_json(db)
print("OK: mapping.json rebuilt & version bumped")
PY
ok "映射构建完成"
