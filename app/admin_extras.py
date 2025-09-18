#!/usr/bin/env python3
import os, shutil, subprocess, shlex
from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates

# ==== 路径与模板 ====
BASE_DIR = os.environ.get("HUANDAN_BASE", os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
TEMPLATE_ROOT = os.path.join(BASE_DIR, "app", "templates")
os.makedirs(TEMPLATE_ROOT, exist_ok=True)

templates = Jinja2Templates(directory=TEMPLATE_ROOT)
try:
    templates.env.auto_reload = True  # 模板保存即生效
except Exception:
    pass

router = APIRouter()

# ==== 简易管理员校验（不依赖 main.py，避免循环导入） ====
def require_admin_simple(request: Request):
    if not request.session.get("admin_user"):
        # 与原逻辑一致：未登录则 302 到登录页
        raise HTTPException(status_code=302, detail="redirect", headers={"Location": "/admin/login"})

# ==== 执行命令 ====
def run_cmd(cmd: str, cwd: Optional[str] = None, timeout: int = 120):
    p = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()

# ==== Git 状态 ====
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
            if len(parts) >= 2:
                ahead, behind = int(parts[0]), int(parts[1])
    _, local_log, _  = run_cmd('git log -1 --date=iso --pretty=format:"%h %cd %s"', cwd=repo)
    _, remote_log, _ = run_cmd(f'git log -1 origin/{branch} --date=iso --pretty=format:"%h %cd %s"', cwd=repo) if branch else (0,"","")

    info.update({
        "branch": branch or "",
        "origin": origin or "",
        "ahead": ahead,
        "behind": behind,
        "local": (local_log or "").strip('"'),
        "remote": (remote_log or "").strip('"'),
    })
    return info

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

    cmds = [
        "git fetch --all --prune",
        "git checkout $(git rev-parse --abbrev-ref HEAD) || true",
        "git reset --hard origin/$(git rev-parse --abbrev-ref HEAD)",
        "git clean -fd"
    ]
    for c in cmds:
        rc, out, err = run_cmd(c, cwd=BASE_DIR)
        if rc != 0:
            return PlainTextResponse(f"更新失败：{c}\n\n{out}\n{err}", status_code=500)

    # 调用仓库安装脚本（幂等：重写 unit/依赖/映射）
    rc, out, err = run_cmd(f"bash {shlex.quote(os.path.join(BASE_DIR,'scripts','install_root.sh'))}", cwd=BASE_DIR, timeout=1800)
    if rc != 0:
        return PlainTextResponse(f"install 脚本执行失败：\n{out}\n{err}", status_code=500)
    return RedirectResponse("/admin/update?ok=1", status_code=302)

# ------------------ 模板编辑器 ------------------
def _safe_template_rel(path: str) -> str:
    p = (path or "").replace("\\", "/").lstrip("/")
    if ".." in p or not p.endswith(".html"):
        raise HTTPException(status_code=400, detail="非法模板路径")
    return p

def _safe_template_abs(path: str) -> str:
    rel = _safe_template_rel(path)
    abs_path = os.path.abspath(os.path.join(TEMPLATE_ROOT, rel))
    troot = os.path.abspath(TEMPLATE_ROOT) + os.sep
    if not (abs_path.startswith(troot) or abs_path == os.path.abspath(TEMPLATE_ROOT)):
        raise HTTPException(status_code=400, detail="非法模板路径")
    return abs_path

def _list_templates() -> List[str]:
    out = []
    for root, _, files in os.walk(TEMPLATE_ROOT):
        for f in files:
            if f.endswith(".html"):
                abs_p = os.path.join(root, f)
                rel_p = os.path.relpath(abs_p, TEMPLATE_ROOT).replace("\\","/")
                out.append(rel_p)
    out.sort()
    return out

@router.get("/admin/templates", response_class=HTMLResponse)
def templates_list(request: Request):
    require_admin_simple(request)
    files = _list_templates()
    return templates.TemplateResponse("templates_list.html", {"request": request, "files": files})

@router.get("/admin/templates/edit", response_class=HTMLResponse)
def templates_edit(request: Request, path: str):
    require_admin_simple(request)
    abs_p = _safe_template_abs(path)
    if not os.path.exists(abs_p):
        raise HTTPException(status_code=404, detail="模板不存在")
    content = open(abs_p, "r", encoding="utf-8").read()
    return templates.TemplateResponse("templates_edit.html", {"request": request, "path": path, "content": content})

@router.post("/admin/templates/save")
def templates_save(request: Request, path: str = Form(...), content: str = Form(...)):
    require_admin_simple(request)
    abs_p = _safe_template_abs(path)
    # 备份
    backup_dir = os.path.join(BASE_DIR, "updates", "template-backups", datetime.utcnow().strftime("%Y%m%d-%H%M%S"))
    os.makedirs(os.path.join(backup_dir, os.path.dirname(path)), exist_ok=True)
    if os.path.exists(abs_p):
        shutil.copy2(abs_p, os.path.join(backup_dir, path))
    # 保存
    os.makedirs(os.path.dirname(abs_p), exist_ok=True)
    with open(abs_p, "w", encoding="utf-8") as f:
        f.write(content)
    return RedirectResponse(f"/admin/templates/edit?path={path}&saved=1", status_code=302)
