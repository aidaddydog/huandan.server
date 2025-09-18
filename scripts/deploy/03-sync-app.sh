#!/usr/bin/env bash
# 作用：把仓库中的应用代码同步到 $HUANDAN_BASE（支持备份与清理）
# 说明：修复了原脚本把仓库根算到 /opt 的问题；自动识别 src/ 或 app/ 作为源码目录。
set -Eeuo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"/.. && pwd)"   # scripts/
source "$DIR/lib/common.sh"
load_env
require_env HUANDAN_BASE

step "同步应用文件（支持备份与清理）"

REPO_ROOT="$(cd "$DIR/.." && pwd)"   # ← 仅回退一级，正确指向仓库根 /opt/huandan
SRC_DIR=""                            # 将在下方判定为 $REPO_ROOT/src 或 $REPO_ROOT/app
TARGET_DIR="$HUANDAN_BASE"            # 默认把 src/ 的内容同步到基底目录

# 1) 选择源码目录：优先 src/，否则 app/
if [[ -d "$REPO_ROOT/src" ]]; then
  SRC_DIR="$REPO_ROOT/src"
  TARGET_DIR="$HUANDAN_BASE"
elif [[ -d "$REPO_ROOT/app" ]]; then
  SRC_DIR="$REPO_ROOT/app"
  TARGET_DIR="$HUANDAN_BASE/app"
  install -d "$TARGET_DIR"
else
  die "未找到源码目录：$REPO_ROOT/src 或 $REPO_ROOT/app
请检查你的仓库结构。你可以运行：
  ls -la $REPO_ROOT
  ls -la $REPO_ROOT/src || true
  ls -la $REPO_ROOT/app || true

如需查看部署日志（最后200行）：
  tail -n 200 /var/log/huandan-deploy.log"
fi

echo "仓库根：$REPO_ROOT"
echo "源码目录：$SRC_DIR"
echo "目标目录：$TARGET_DIR"

# 2) 交互：是否备份现有部署目录
read -r -p "是否对现有 $HUANDAN_BASE 做一次备份？(Y/n): " DO_BACKUP
DO_BACKUP=${DO_BACKUP:-Y}
if [[ "$DO_BACKUP" =~ ^[Yy]$ ]]; then
  TS="$(date +%Y%m%d-%H%M%S)"
  BK_DIR="/opt/backup"; install -d "$BK_DIR"
  BK_TGZ="$BK_DIR/huandan-server-$TS.tgz"
  if [[ -d "$HUANDAN_BASE" ]]; then
    tar -czf "$BK_TGZ" -C "$(dirname "$HUANDAN_BASE")" "$(basename "$HUANDAN_BASE")"
    ok "已备份到：$BK_TGZ"
  else
    warn "未发现 $HUANDAN_BASE，跳过备份。"
  fi
fi

# 3) 交互：是否清理可再生内容
read -r -p "是否清理可再生内容（venv、__pycache__）后再同步？(y/N): " DO_CLEAN
DO_CLEAN=${DO_CLEAN:-N}
if [[ "$DO_CLEAN" =~ ^[Yy]$ ]]; then
  rm -rf "$HUANDAN_BASE/.venv" || true
  find "$HUANDAN_BASE" -type d -name "__pycache__" -prune -exec rm -rf {} + || true
  ok "已清理可再生内容"
fi

# 4) 执行同步
#    -a：保留属性  -v：详情  --delete：删除目标端多余文件（谨慎使用）
#    根据源码目录不同，选择合适的目标路径：
if [[ "$SRC_DIR" == "$REPO_ROOT/src" ]]; then
  rsync -av --delete "$SRC_DIR/" "$TARGET_DIR/"
else
  # app/ → $HUANDAN_BASE/app/
  rsync -av --delete "$SRC_DIR/" "$TARGET_DIR/"
fi

ok "代码同步完成：$SRC_DIR → $TARGET_DIR"

# 5) 额外提示：常见静态/模板/运行时目录（如需要可在仓库中维护）
# 你也可以在仓库根提供 runtime/ templates/ static/ 等目录，再按需同步：
#   rsync -av "$REPO_ROOT/runtime/" "$HUANDAN_BASE/runtime/"
#   rsync -av "$REPO_ROOT/app/templates/" "$HUANDAN_BASE/app/templates/"
#   rsync -av "$REPO_ROOT/app/static/" "$HUANDAN_BASE/app/static/"

