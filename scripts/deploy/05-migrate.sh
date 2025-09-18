#!/usr/bin/env bash
# 作用：生成/刷新映射 mapping.json 并写入版本信息
# 说明：在导入 app.main 前，确保 runtime/ 等目录存在，避免静态挂载时报错。
set -Eeuo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"/.. && pwd)"   # scripts/
source "$DIR/lib/common.sh"
load_env
require_env HUANDAN_BASE

step "重建映射 mapping.json 并刷新版本"

# 选择 Python 解释器
PY="$HUANDAN_BASE/.venv/bin/python"
if [[ ! -x "$PY" ]]; then
  PY="$(command -v python3 || true)"
fi
[[ -x "$PY" ]] || die "找不到 Python 解释器：$PY"

# 预建关键目录（避免 import app.main 时 StaticFiles 抛错）
install -d -m 755 "$HUANDAN_BASE/runtime" "$HUANDAN_BASE/updates" || true
install -d -m 755 "$HUANDAN_BASE/app/templates" "$HUANDAN_BASE/app/static" || true

# 调用项目方法进行生成/刷新（兼容降级）
"$PY" - <<'PYCODE'
import os, sys, importlib

base = os.environ.get("HUANDAN_BASE", "/opt/huandan-server")
sys.path.insert(0, base)

# 再保险：确保运行期目录存在
for d in ("runtime", "updates", "app", os.path.join("app","templates"), os.path.join("app","static")):
    os.makedirs(os.path.join(base, d), exist_ok=True)

try:
    m = importlib.import_module("app.main")
except Exception as e:
    print(f"[WARN] 导入 app.main 失败：{e}")
    # 降级策略：至少确保 mapping.json 存在
    mf = os.path.join(base, "runtime", "mapping.json")
    os.makedirs(os.path.dirname(mf), exist_ok=True)
    if not os.path.exists(mf):
        open(mf, "w", encoding="utf-8").write("{}")
    print("[OK] 已降级创建空 mapping.json")
    raise

# 优先调用项目函数（若存在）
called = False
for name in ("write_mapping_json", "set_mapping_version"):
    if hasattr(m, name):
        try:
            print(f"[INFO] 调用 {name}()")
            getattr(m, name)()
            called = True
        except Exception as e:
            print(f"[WARN] {name} 执行失败：{e}")

# 兜底：保证 mapping.json 至少存在
mf = os.path.join(base, "runtime", "mapping.json")
os.makedirs(os.path.dirname(mf), exist_ok=True)
if not os.path.exists(mf):
    open(mf, "w", encoding="utf-8").write("{}")

print("[OK] mapping.json 已就绪" + ("（已调用项目方法）" if called else "（兼容降级）"))
PYCODE

ok "映射与版本处理完成"

echo
echo "若遇到异常，一键查看部署日志："
echo "  tail -n 200 /var/log/huandan-deploy.log"
