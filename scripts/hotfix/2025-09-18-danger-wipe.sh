#!/usr/bin/env bash
set -Eeuo pipefail
BASE="/opt/huandan-server"
cd "$BASE"

# 1) 给 main.py 注入两个危险接口：/admin/danger/wipe_pdfs 和 /admin/danger/wipe_orders
$BASE/.venv/bin/python - <<'PY'
import sys,io,os,re
fp="app/main.py"
s=open(fp,"r",encoding="utf-8").read()

code = r'''
# ------------------ DANGER ZONE：高危清空操作 ------------------
@app.post("/admin/danger/wipe_pdfs")
def danger_wipe_pdfs(request: Request, confirm: str = Form(""), db=Depends(get_db)):
    require_admin(request, db)
    if (confirm or "").strip() != "DELETE ALL PDF":
        return RedirectResponse("/admin/files?danger=badconfirm", status_code=302)
    # 删除磁盘所有 .pdf（包括未登记的孤儿文件）
    removed_files = 0
    try:
        for name in os.listdir(PDF_DIR):
            if name.lower().endswith(".pdf"):
                fp = os.path.join(PDF_DIR, name)
                if os.path.isfile(fp):
                    try:
                        os.remove(fp); removed_files += 1
                    except Exception:
                        pass
    except Exception:
        pass
    # 清空 TrackingFile 表
    removed_rows = db.query(TrackingFile).delete()
    db.commit()
    # 刷新版本 & 重写映射
    set_mapping_version(db); write_mapping_json(db)
    return RedirectResponse(f"/admin/files?danger=pdfs_cleared&files={removed_files}&rows={removed_rows}", status_code=302)

@app.post("/admin/danger/wipe_orders")
def danger_wipe_orders(request: Request, confirm: str = Form(""), db=Depends(get_db)):
    require_admin(request, db)
    if (confirm or "").strip() != "DELETE ALL ORDERS":
        return RedirectResponse("/admin/orders?danger=badconfirm", status_code=302)
    removed = db.query(OrderMapping).delete()
    db.commit()
    set_mapping_version(db); write_mapping_json(db)
    return RedirectResponse(f"/admin/orders?danger=orders_cleared&rows={removed}", status_code=302)
'''

if "def danger_wipe_pdfs(" not in s:
    s += "\n" + code + "\n"
    open(fp,"w",encoding="utf-8").write(s)
    print("patched: main.py (danger endpoints)")
else:
    print("exists: danger endpoints")
PY

# 2) 在 files.html（PDF 列表页）加入“危险：清空所有 PDF”按钮（带输入确认）
$BASE/.venv/bin/python - <<'PY'
fp="app/templates/files.html"
s=open(fp,"r",encoding="utf-8").read()
if "/admin/danger/wipe_pdfs" not in s:
    inj = '''
<form method="post" action="/admin/danger/wipe_pdfs" class="row" onsubmit="return confirm('⚠️ 危险操作：将删除服务器上所有 PDF 文件及其数据库记录，且不可恢复。确定继续？')">
  <input name="confirm" placeholder="输入 DELETE ALL PDF 以确认" style="flex:1">
  <button type="submit" class="danger">危险：清空所有 PDF</button>
</form>
'''
    s = s.replace("<h2>PDF 列表</h2>", "<h2>PDF 列表</h2>\n"+inj, 1)
    open(fp,"w",encoding="utf-8").write(s)
    print("patched: files.html (danger form)")
else:
    print("exists: danger form in files.html")
PY

# 3) 在 orders.html（订单列表页）加入“危险：清空全部订单映射”按钮（带输入确认）
$BASE/.venv/bin/python - <<'PY'
fp="app/templates/orders.html"
s=open(fp,"r",encoding="utf-8").read()
if "/admin/danger/wipe_orders" not in s:
    inj = '''
<form method="post" action="/admin/danger/wipe_orders" class="row" onsubmit="return confirm('⚠️ 危险操作：将删除全部订单映射（不影响 PDF 文件）。确定继续？')">
  <input name="confirm" placeholder="输入 DELETE ALL ORDERS 以确认" style="flex:1">
  <button type="submit" class="danger">危险：清空全部订单映射</button>
</form>
'''
    s = s.replace("<h2>订单列表</h2>", "<h2>订单列表</h2>\n"+inj, 1)
    open(fp,"w",encoding="utf-8").write(s)
    print("patched: orders.html (danger form)")
else:
    print("exists: danger form in orders.html")
PY

systemctl restart huandan.service
echo "OK. 已上线危险操作按钮。请刷新 /admin/files 与 /admin/orders 页面查看。"
