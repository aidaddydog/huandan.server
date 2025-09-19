#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, re, shutil, subprocess, shlex
from datetime import datetime
from typing import Optional, List, Dict, Tuple
from fastapi import APIRouter, Request, Form, HTTPException, Query
from fastapi.responses import HTMLResponse, RedirectResponse, PlainTextResponse, Response
from fastapi.templating import Jinja2Templates

# ==== 路径 ====
BASE_DIR = os.environ.get("HUANDAN_BASE", os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
TPL_ROOT = os.path.join(BASE_DIR, "app", "templates")
STATIC_ROOT = os.path.join(BASE_DIR, "app", "static")
os.makedirs(TPL_ROOT, exist_ok=True)
os.makedirs(STATIC_ROOT, exist_ok=True)

# ==== 模板引擎（热重载）====
templates = Jinja2Templates(directory=TPL_ROOT)
try:
    templates.env.auto_reload = True
except Exception:
    pass

router = APIRouter()

# ==== 中文名映射（找不到时再用）====
FRIENDLY_MAP: Dict[str, str] = {
    "login.html": "登录页面",
    "layout.html": "通用布局",
    "dashboard.html": "仪表盘",
    "upload_orders.html": "导入订单",
    "choose_columns.html": "订单列选择",
    "preview_orders.html": "订单预览确认",
    "upload_pdf.html": "导入 PDF",
    "orders.html": "订单列表",
    "files.html": "PDF 列表",
    "clients.html": "客户端访问码",
    "settings.html": "系统设置",
    "update.html": "在线升级",
    "templates_list.html": "模板列表",
    "templates_edit.html": "模板编辑",
    "style.css": "站点样式",
}

# ==== 管理校验（不依赖 main.py，避免循环导入）====
def require_admin_simple(request: Request):
    if not request.session.get("admin_user"):
        raise HTTPException(status_code=302, detail="redirect", headers={"Location": "/admin/login"})

# ==== 命令执行 ====
def run_cmd(cmd: str, cwd: Optional[str] = None, timeout: int = 180):
    p = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()

# ==== Git 信息 ====
def git_status_info(repo: str):
    if not os.path.isdir(os.path.join(repo, ".git")):
        return {"mode": "nogit"}
    info = {"mode": "git", "repo": repo}
    rc, branch, _ = run_cmd("git rev-parse --abbrev-ref HEAD", cwd=repo)
    if rc != 0: branch = ""
    rc, origin, _ = run_cmd("git remote get-url origin", cwd=repo)
    run_cmd("git fetch --all --prune", cwd=repo)
    ahead = behind = 0
    if branch:
        rc, counts, _ = run_cmd(f"git rev-list --left-right --count HEAD...origin/{branch}", cwd=repo)
        if rc == 0 and counts:
            parts = counts.replace("\t"," ").split()
            if len(parts)>=2:
                ahead, behind = int(parts[0]), int(parts[1])
    _, local_log, _  = run_cmd('git log -1 --date=iso --pretty=format:"%h %cd %s"', cwd=repo)
    _, remote_log, _ = run_cmd(f'git log -1 origin/{branch} --date=iso --pretty=format:"%h %cd %s"', cwd=repo) if branch else (0,"","")
    info.update({
        "branch": branch or "", "origin": origin or "",
        "ahead": ahead, "behind": behind,
        "local": (local_log or "").strip('"'), "remote": (remote_log or "").strip('"'),
    })
    return info

# ==== 解析中文名：优先文件头注释（HTML/CSS/JS），否则 FRIENDLY_MAP 否则文件名 ====
def parse_cn_name(abs_path: str, rel_path: str) -> str:
    name_from_map = FRIENDLY_MAP.get(os.path.basename(rel_path))
    try:
        with open(abs_path, "r", encoding="utf-8", errors="ignore") as f:
            head = f.read(2048)
        m = re.search(r"<!--\s*(?:name|title)\s*:\s*(.*?)\s*-->", head, flags=re.I)
        if m and m.group(1).strip(): return m.group(1).strip()
        m = re.search(r"/\*\s*name\s*:\s*(.*?)\s*\*/", head, flags=re.I)
        if m and m.group(1).strip(): return m.group(1).strip()
        m = re.search(r"//\s*name\s*:\s*(.*)", head, flags=re.I)
        if m and m.group(1).strip(): return m.group(1).strip()
    except Exception:
        pass
    return name_from_map or os.path.basename(rel_path)

# ==== 扫描模板/静态 ====
ALLOW_TPL_EXT = {".html"}
ALLOW_STATIC_EXT = {".css", ".js"}

def _scan_dir(root: str, allow_ext: set) -> List[Tuple[str, str, float, int]]:
    out = []
    for r, _, files in os.walk(root):
        for fn in files:
            ext = os.path.splitext(fn)[1].lower()
            if ext not in allow_ext: continue
            abs_p = os.path.join(r, fn)
            rel_p = os.path.relpath(abs_p, root).replace("\\","/")
            st = os.stat(abs_p)
            out.append((rel_p, abs_p, st.st_mtime, st.st_size))
    out.sort()
    return out

def _list_all_files():
    tpls = _scan_dir(TPL_ROOT, ALLOW_TPL_EXT)
    assets = _scan_dir(STATIC_ROOT, ALLOW_STATIC_EXT)
    return tpls, assets

# ==== 路径安全 ====
def _safe_abs(kind: str, rel: str) -> str:
    rel = (rel or "").replace("\\", "/").lstrip("/")
    if ".." in rel or rel.startswith("/"): raise HTTPException(status_code=400, detail="非法路径")
    if kind == "tpl":
        abs_p = os.path.abspath(os.path.join(TPL_ROOT, rel))
        if not abs_p.startswith(os.path.abspath(TPL_ROOT)+os.sep) and abs_p != os.path.abspath(TPL_ROOT):
            raise HTTPException(status_code=400, detail="非法模板路径")
        if os.path.splitext(abs_p)[1].lower() not in ALLOW_TPL_EXT:
            raise HTTPException(status_code=400, detail="仅允许 .html")
        return abs_p
    elif kind == "static":
        abs_p = os.path.abspath(os.path.join(STATIC_ROOT, rel))
        if not abs_p.startswith(os.path.abspath(STATIC_ROOT)+os.sep) and abs_p != os.path.abspath(STATIC_ROOT):
            raise HTTPException(status_code=400, detail="非法静态路径")
        if os.path.splitext(abs_p)[1].lower() not in ALLOW_STATIC_EXT:
            raise HTTPException(status_code=400, detail="仅允许 .css / .js")
        return abs_p
    raise HTTPException(status_code=400, detail="未知类型")

# ------------------ 在线升级 ------------------
@router.get("/admin/update", response_class=HTMLResponse)
def update_page(request: Request):
    require_admin_simple(request)
    info = git_status_info(BASE_DIR)
    oneliner = "bash <(curl -fsSL https://raw.githubusercontent.com/aidaddydog/huandan.server/main/scripts/bootstrap_online.sh)"
    return templates.TemplateResponse("update.html", {"request": request, "info": info, "oneliner": oneliner})

@router.post("/admin/update/git_pull")
def update_git_pull(request: Request):
    require_admin_simple(request)
    if not os.path.isdir(os.path.join(BASE_DIR, ".git")):
        raise HTTPException(status_code=400, detail="当前目录不是 git 仓库，无法 git pull")
    for c in [
        "git fetch --all --prune",
        "git checkout $(git rev-parse --abbrev-ref HEAD) || true",
        "git reset --hard origin/$(git rev-parse --abbrev-ref HEAD)",
        "git clean -fd"
    ]:
        rc, out, err = run_cmd(c, cwd=BASE_DIR)
        if rc != 0:
            return PlainTextResponse(f"更新失败：{c}\n\n{out}\n{err}", status_code=500)
    rc, out, err = run_cmd(f"bash {shlex.quote(os.path.join(BASE_DIR,'scripts','install_root.sh'))}", cwd=BASE_DIR, timeout=1800)
    if rc != 0:
        return PlainTextResponse(f"install 脚本失败：\n{out}\n{err}", status_code=500)
    return RedirectResponse("/admin/update?ok=1", status_code=302)

# ------------------ 预览上下文（避免模板缺变量 500） ------------------
def _preview_ctx(request: Request):
    return {
        "request": request, "preview": True,
        "stats": {"order_count":0,"file_count":0,"client_count":0,"version":"preview","server_version":"preview","client_recommend":"","o_days":"30","f_days":"30"},
        "rows": [], "files": [], "columns": [],
        "q": "", "page": 1, "pages": 1, "total": 0, "page_size": 100,
        "err": "", "error": "",
    }

# ------------------ 模板列表（含 SSH Key 操作与推送） ------------------
def _ssh_dir(): return os.path.join(os.path.expanduser("~"), ".ssh")
def _ssh_paths():
    d = _ssh_dir()
    return {"dir": d, "key": os.path.join(d,"id_ed25519"), "pub": os.path.join(d,"id_ed25519.pub"), "cfg": os.path.join(d,"config")}

def _ssh_info():
    ps = _ssh_paths()
    have_key = os.path.exists(ps["key"]) and os.path.exists(ps["pub"])
    pub = ""
    if have_key:
        try: pub = open(ps["pub"], "r", encoding="utf-8").read().strip()
        except Exception: pub = ""
    rc, who, _ = run_cmd("whoami")
    return {"have_key": have_key, "pubkey": pub, "paths": ps, "whoami": who or "root"}

def _origin_info():
    info = git_status_info(BASE_DIR)
    origin = info.get("origin","")
    if origin.startswith("git@github.com:"): otype = "ssh"
    elif origin.startswith("https://github.com"): otype = "https"
    else: otype = "other"
    return {"origin": origin, "type": otype, "branch": info.get("branch")}

def _owner_repo_from_origin(origin: str) -> Optional[str]:
    if origin.startswith("git@github.com:"): t = origin.split(":",1)[1]
    elif origin.startswith("https://github.com/"): t = origin.split("github.com/",1)[1]
    else: return None
    return t[:-4] if t.endswith(".git") else t

def _ensure_ssh_config():
    ps = _ssh_paths()
    os.makedirs(ps["dir"], exist_ok=True)
    cfg = f"""Host github.com
  HostName github.com
  User git
  IdentityFile {ps["key"]}
  IdentitiesOnly yes
  StrictHostKeyChecking accept-new
"""
    open(ps["cfg"], "w", encoding="utf-8").write(cfg)
    os.chmod(ps["dir"], 0o700)
    for f,mode in [(ps["key"],0o600),(ps["pub"],0o644),(ps["cfg"],0o600)]:
        if os.path.exists(f):
            try: os.chmod(f, mode)
            except Exception: pass

@router.get("/admin/templates", response_class=HTMLResponse)
def templates_list(request: Request, pushed: Optional[str]=None, err: Optional[str]=None, keymsg: Optional[str]=None, test: Optional[str]=None, switched: Optional[str]=None):
    require_admin_simple(request)
    tpls, assets = _list_all_files()
    tpl_rows = [{"kind":"tpl","rel":rel,"cn":parse_cn_name(abs_p, rel),"mtime":mtime,"size":size} for rel,abs_p,mtime,size in tpls]
    ast_rows = [{"kind":"static","rel":rel,"cn":parse_cn_name(abs_p, rel),"mtime":mtime,"size":size} for rel,abs_p,mtime,size in assets]
    info = git_status_info(BASE_DIR); sshi = _ssh_info(); ori = _origin_info()
    return templates.TemplateResponse("templates_list.html", {"request": request,"tpls": tpl_rows,"assets": ast_rows,"info": info,"ssh": sshi,"origin": ori,"pushed": pushed or "","err": err or "","keymsg": keymsg or "","test": test or "","switched": switched or ""})

# ------------------ 模板编辑 / 保存 ------------------
@router.get("/admin/templates/edit", response_class=HTMLResponse)
def templates_edit(request: Request, kind: str = Query(..., pattern="^(tpl|static)$"), path: str = Query(...)):
    require_admin_simple(request)
    abs_p = _safe_abs(kind, path)
    content = open(abs_p, "r", encoding="utf-8", errors="ignore").read()
    return templates.TemplateResponse("templates_edit.html", {"request": request,"kind": kind, "path": path, "cn": parse_cn_name(abs_p, path), "content": content})

@router.post("/admin/templates/save")
def templates_save(request: Request, kind: str = Form(...), path: str = Form(...), content: str = Form(...)):
    require_admin_simple(request)
    abs_p = _safe_abs(kind, path)
    backup_dir = os.path.join(BASE_DIR, "updates", "template-backups", datetime.utcnow().strftime("%Y%m%d-%H%M%S"))
    os.makedirs(os.path.join(backup_dir, os.path.dirname(path)), exist_ok=True)
    if os.path.exists(abs_p): shutil.copy2(abs_p, os.path.join(backup_dir, path))
    os.makedirs(os.path.dirname(abs_p), exist_ok=True)
    with open(abs_p, "w", encoding="utf-8") as f: f.write(content)
    return RedirectResponse(f"/admin/templates/edit?kind={kind}&path={path}&saved=1", status_code=302)

# ------------------ 预览（真实 Request + 安全上下文） ------------------
@router.get("/admin/templates/preview", response_class=HTMLResponse)
def templates_preview(request: Request, kind: str = Query(..., pattern="^(tpl|static)$"), path: str = Query(...)):
    abs_p = _safe_abs(kind, path)
    if not os.path.exists(abs_p): raise HTTPException(status_code=404, detail="模板不存在")
    ext = os.path.splitext(abs_p)[1].lower()
    if kind == "tpl" and ext == ".html":
        ctx = _preview_ctx(request)
        try:
            return templates.TemplateResponse(path, ctx)
        except Exception as e:
            raw = open(abs_p, "r", encoding="utf-8", errors="ignore").read()
            def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
            html = f"""<!doctype html><meta charset="utf-8"><title>预览失败</title>
<h3>渲染出错</h3><pre>{esc(str(e))}</pre>
<h3>原始模板</h3><pre style="white-space:pre-wrap">{esc(raw)}</pre>"""
            return HTMLResponse(content=html, status_code=200)
    if kind == "static" and ext in {".css",".js"}:
        rel = path
        if ext == ".css":
            html = f'<!doctype html><meta charset="utf-8"><title>CSS 预览</title><link rel="stylesheet" href="/static/{rel}"><div style="padding:16px">CSS 已加载（请在实际页面查看最终效果）。</div>'
        else:
            html = f'<!doctype html><meta charset="utf-8"><title>JS 预览</title><script src="/static/{rel}"></script><div style="padding:16px">JS 已加载（输出看控制台）。</div>'
        return HTMLResponse(content=html, status_code=200)
    return PlainTextResponse("暂不支持此类型预览", status_code=400)

# ------------------ 一键回传到仓库（git add/commit/push） ------------------
@router.post("/admin/templates/git_push")
def templates_git_push(request: Request, message: str = Form("web-edit: update templates")):
    require_admin_simple(request)
    if not os.path.isdir(os.path.join(BASE_DIR, ".git")):
        return RedirectResponse("/admin/templates?err=此目录不是 git 仓库，无法推送", status_code=302)
    run_cmd(f'git add {shlex.quote(os.path.relpath(TPL_ROOT, BASE_DIR))} {shlex.quote(os.path.relpath(STATIC_ROOT, BASE_DIR))}', cwd=BASE_DIR)
    rc, out, err = run_cmd(f'git commit -m {shlex.quote(message)}', cwd=BASE_DIR)
    if rc != 0 and "nothing to commit" in (out+err).lower():
        return RedirectResponse("/admin/templates?pushed=0&err=没有变更", status_code=302)
    rc, out, err = run_cmd('git push -u origin HEAD:$(git rev-parse --abbrev-ref HEAD)', cwd=BASE_DIR)
    if rc != 0:
        return RedirectResponse(f"/admin/templates?pushed=0&err=推送失败：{(out or err)[:300]}", status_code=302)
    return RedirectResponse("/admin/templates?pushed=1", status_code=302)

# ------------------ SSH Key：在“模板列表”里一键操作 ------------------
@router.post("/admin/templates/ssh/generate")
def templates_ssh_generate(request: Request):
    require_admin_simple(request)
    ps = _ssh_paths()
    os.makedirs(ps["dir"], exist_ok=True)
    if not os.path.exists(ps["key"]):
        rc, out, err = run_cmd(f'ssh-keygen -t ed25519 -C "server@huandan" -N "" -f {shlex.quote(ps["key"])}')
        if rc != 0:
            return RedirectResponse(f"/admin/templates?keymsg=生成失败：{(out or err)[:200]}", status_code=302)
    _ensure_ssh_config()
    return RedirectResponse("/admin/templates?keymsg=已生成或已存在（请将上方公钥添加到 GitHub）", status_code=302)

@router.post("/admin/templates/ssh/test")
def templates_ssh_test(request: Request):
    require_admin_simple(request)
    _ensure_ssh_config()
    rc, out, err = run_cmd('ssh -T git@github.com -o BatchMode=yes -o StrictHostKeyChecking=accept-new', timeout=20)
    msg = (out or "") + ("\n" + err if err else "")
    ok = ("successfully authenticated" in msg) or ("Hi " in msg)
    return RedirectResponse(f"/admin/templates?test={'1' if ok else '0'}&keymsg={shlex.quote(msg[:300])}", status_code=302)

@router.post("/admin/templates/ssh/switch_to_ssh")
def templates_ssh_switch(request: Request):
    require_admin_simple(request)
    ori = git_status_info(BASE_DIR).get("origin","")
    pair = _owner_repo_from_origin(ori)
    if not pair:
        return RedirectResponse("/admin/templates?err=无法解析远端地址，手动设置 origin 后再试", status_code=302)
    _ensure_ssh_config()
    new = f"git@github.com:{pair}.git"
    rc, out, err = run_cmd(f"git remote set-url origin {shlex.quote(new)}", cwd=BASE_DIR)
    if rc != 0:
        return RedirectResponse(f"/admin/templates?err=切换失败：{(out or err)[:200]}", status_code=302)
    return RedirectResponse("/admin/templates?switched=1", status_code=302)
