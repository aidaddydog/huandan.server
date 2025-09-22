# app/main.py
import os, zipfile, re, shutil, time, math, json, traceback
import subprocess, shlex, threading, uuid, asyncio
from datetime import datetime, timedelta
from typing import Optional, List, Tuple

from fastapi import FastAPI, Request, UploadFile, File, Form, Depends, HTTPException, Query
from fastapi.responses import (
    HTMLResponse, RedirectResponse, FileResponse, PlainTextResponse,
    JSONResponse, Response, StreamingResponse
)
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from sqlalchemy import create_engine, Column, String, Integer, Boolean, DateTime, Text, select
from sqlalchemy.orm import sessionmaker, declarative_base

from passlib.hash import bcrypt
import pandas as pd

# ---------------- 基本路径 ----------------
BASE_DIR = os.environ.get("HUANDAN_BASE", os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
DATA_DIR = os.environ.get("HUANDAN_DATA", "/opt/huandan-data")

PDF_DIR = os.path.join(DATA_DIR, "pdfs")
UP_DIR  = os.path.join(DATA_DIR, "uploads")
ZIP_DIR = os.path.join(DATA_DIR, "pdf_zips")
os.makedirs(PDF_DIR, exist_ok=True)
os.makedirs(UP_DIR,  exist_ok=True)
os.makedirs(ZIP_DIR, exist_ok=True)

# 确保静态/更新/运行时目录存在
os.makedirs(os.path.join(BASE_DIR, "app", "static"), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "app", "templates"), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "updates"), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "runtime"), exist_ok=True)

# ---------------- 应用/挂载 ----------------
app = FastAPI(title="换单服务端")
app.add_middleware(SessionMiddleware, secret_key=os.environ.get("SECRET_KEY","huandan-secret-key"))

app.mount("/static",  StaticFiles(directory=os.path.join(BASE_DIR, "app", "static")),  name="static")
app.mount("/updates", StaticFiles(directory=os.path.join(BASE_DIR, "updates")),       name="updates")
app.mount("/runtime", StaticFiles(directory=os.path.join(BASE_DIR, "runtime")),       name="runtime")

templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "app", "templates"))
try:
    templates.env.auto_reload = True
except Exception:
    pass

from app.admin_extras import router as admin_extras_router
app.include_router(admin_extras_router)

# ---------------- 数据库 ----------------
engine = create_engine(
    f"sqlite:///{os.path.join(BASE_DIR,'huandan.sqlite3')}",
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

class MetaKV(Base):
    __tablename__ = "meta"
    key = Column(String(64), primary_key=True)
    value = Column(Text)

class AdminUser(Base):
    __tablename__ = "admin_users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(64), unique=True)
    password_hash = Column(String(256))
    is_active = Column(Boolean, default=True)

class ClientAuth(Base):
    __tablename__ = "client_auth"
    id = Column(Integer, primary_key=True, autoincrement=True)
    code_hash = Column(String(256))
    code_plain = Column(String(16))
    description = Column(String(128), default="")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_used = Column(DateTime, nullable=True)
    fail_count = Column(Integer, default=0)
    locked_until = Column(DateTime, nullable=True)

class OrderMapping(Base):
    __tablename__ = "order_mapping"
    order_id = Column(String(128), primary_key=True)
    tracking_no = Column(String(128), index=True)
    updated_at = Column(DateTime, default=datetime.utcnow)

class TrackingFile(Base):
    __tablename__ = "tracking_file"
    tracking_no = Column(String(128), primary_key=True)
    file_path = Column(Text)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

# —— 启动时初始化数据库 ——
@app.on_event("startup")
def _init_db():
    try:
        Base.metadata.create_all(bind=engine, checkfirst=True)
    except Exception as e:
        print("DB init warn:", e)

# ---------------- 工具函数 ----------------
def now_iso(): return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

def to_iso(dt: Optional[datetime]) -> str:
    if not dt: return ""
    try: return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    except Exception: return ""

def canon_tracking(s: str) -> str:
    s = (s or "").strip()
    s = re.sub(r"[^A-Za-z0-9_.-]+", "_", s)
    s = re.sub(r"_+", "_", s)
    s = s.strip("._")
    return s[:128]

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

def get_kv(db, key, default=""):
    obj = db.get(MetaKV, key)
    return obj.value if obj and obj.value is not None else default

def set_kv(db, key, value):
    obj = db.get(MetaKV, key)
    if not obj:
        obj = MetaKV(key=key, value=str(value)); db.add(obj)
    else:
        obj.value = str(value)
    db.commit()

def set_mapping_version(db): set_kv(db, "mapping_version", now_iso())
def get_mapping_version(db):
    v = get_kv(db, "mapping_version", "")
    if not v:
        set_mapping_version(db); v = get_kv(db,"mapping_version","")
    return v

def _build_mapping_payload(db):
    map_rows = db.query(OrderMapping).all()
    file_rows = db.query(TrackingFile).all()
    tf_by_tn = {f.tracking_no: f for f in file_rows}
    payload, seen = [], set()
    for r in map_rows:
        tn_norm = canon_tracking(r.tracking_no or "")
        tf = tf_by_tn.get(tn_norm) or tf_by_tn.get(r.tracking_no or "")
        u = r.updated_at
        if tf and tf.uploaded_at: u = max([x for x in (u, tf.uploaded_at) if x is not None])
        payload.append({"order_id": r.order_id, "tracking_no": tn_norm, "updated_at": to_iso(u)})
        seen.add(tn_norm)
    for f in file_rows:
        tn_norm = canon_tracking(f.tracking_no or "")
        if tn_norm in seen: continue
        payload.append({"order_id": "", "tracking_no": tn_norm, "updated_at": to_iso(f.uploaded_at)})
    return {"version": get_mapping_version(db), "mappings": payload}

def write_mapping_json(db):
    data = _build_mapping_payload(db)
    fp = os.path.join(DATA_DIR, "mapping.json")
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ---------------- 进度管理（SSE/轮询） ----------------
PROGRESS = {}
PROG_LOCK = threading.Lock()
PROG_TTL_SEC = 3600

def new_progress(tag="task") -> str:
    pid = uuid.uuid4().hex
    with PROG_LOCK:
        PROGRESS[pid] = {"stage": "init", "pct": 0, "note": "", "ok": True, "done": False, "tag": tag, "ts": time.time()}
    return pid

def set_progress(pid: str, stage=None, pct=None, note=None, ok=None, done=None):
    with PROG_LOCK:
        s = PROGRESS.get(pid)
        if not s: return
        if stage is not None: s["stage"]=stage
        if pct   is not None: s["pct"]=max(0, min(100, int(pct)))
        if note  is not None: s["note"]=str(note)[:200]
        if ok    is not None: s["ok"]=bool(ok)
        if done  is not None: s["done"]=bool(done)
        s["ts"] = time.time()

def _gc_progress():
    now=time.time()
    with PROG_LOCK:
        for k in list(PROGRESS.keys()):
            if now - PROGRESS[k]["ts"] > PROG_TTL_SEC:
                PROGRESS.pop(k, None)

def sse_event(data: str, event: str = None) -> bytes:
    buf = ""
    if event: buf += f"event: {event}\n"
    for line in data.splitlines():
        buf += f"data: {line}\n"
    buf += "\n"
    return buf.encode("utf-8")

@app.get("/admin/progress/new")
def progress_new(tag: str = "task"):
    pid = new_progress(tag=tag)
    return {"id": pid}

@app.get("/admin/progress/get")
def progress_get(id: str):
    _gc_progress()
    with PROG_LOCK:
        s = PROGRESS.get(id)
    if not s: return {"missing": True}
    return s

@app.get("/admin/progress/stream")
async def progress_stream(id: str):
    async def generator():
        while True:
            _gc_progress()
            with PROG_LOCK:
                s = PROGRESS.get(id)
            if not s:
                yield sse_event(json.dumps({"missing": True}), "gone"); return
            yield sse_event(json.dumps(s), "progress")
            if s.get("done"):
                yield sse_event(json.dumps(s), "done"); return
            await asyncio.sleep(0.8)
    return StreamingResponse(generator(), media_type="text/event-stream",
                             headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})

# ---------------- ZIP 构建与列出 ----------------
def _date_str(d: datetime.date) -> str:
    try: return d.strftime("%Y-%m-%d")
    except Exception: return str(d)

def _date_str_compact(d: datetime.date) -> str:
    try: return d.strftime("%Y%m%d")
    except Exception: return str(d).replace("-","")

def _calc_etag(fp: str) -> str:
    st = os.stat(fp)
    return f'W/"{int(st.st_mtime)}-{st.st_size}"'

def _calc_sha256(fp: str) -> str:
    try:
        import hashlib
        h = hashlib.sha256()
        with open(fp, "rb") as f:
            for chunk in iter(lambda: f.read(1024*1024), b""): h.update(chunk)
        return h.hexdigest()
    except Exception:
        return ""

def build_daily_pdf_zip(db, target_date: Optional[datetime.date]=None, progress_cb=None) -> str:
    """重建 target_date 的日归档 ZIP。progress_cb(idx, total, tracking?) 可选。"""
    if target_date is None: target_date = datetime.utcnow().date()
    start_dt = datetime(target_date.year, target_date.month, target_date.day)
    end_dt   = start_dt + timedelta(days=1)
    files = db.query(TrackingFile).filter(
        TrackingFile.uploaded_at >= start_dt,
        TrackingFile.uploaded_at <  end_dt
    ).all()
    zip_name = f"pdfs-{_date_str_compact(target_date)}.zip"
    fp_zip   = os.path.join(ZIP_DIR, zip_name)
    if not files:
        return fp_zip
    tmp_zip = fp_zip + ".tmp"
    try:
        total=len(files)
        with zipfile.ZipFile(tmp_zip, "w", compression=zipfile.ZIP_DEFLATED) as z:
            for i, f in enumerate(files, start=1):
                try:
                    if not f.file_path or (not os.path.exists(f.file_path)): continue
                    arcname = f"{canon_tracking(f.tracking_no)}.pdf"
                    z.write(f.file_path, arcname)
                finally:
                    if progress_cb:
                        try: progress_cb(i, total, f.tracking_no)
                        except Exception: pass
        os.makedirs(os.path.dirname(fp_zip), exist_ok=True)
        if os.path.exists(fp_zip):
            try: os.replace(tmp_zip, fp_zip)
            except Exception:
                try: os.remove(fp_zip)
                except Exception: pass
                os.replace(tmp_zip, fp_zip)
        else:
            os.replace(tmp_zip, fp_zip)
    finally:
        try:
            if os.path.exists(tmp_zip): os.remove(tmp_zip)
        except Exception: pass
    return fp_zip

def list_pdf_zip_dates() -> list:
    out=[]
    if not os.path.isdir(ZIP_DIR): return out
    for name in os.listdir(ZIP_DIR):
        if not name.startswith("pdfs-") or not name.endswith(".zip"): continue
        dpart=name[len("pdfs-"):-len(".zip")]
        if len(dpart)==8 and dpart.isdigit():
            d=f"{dpart[0:4]}-{dpart[4:6]}-{dpart[6:8]}"
        elif len(dpart)==10 and dpart[4]=='-' and dpart[7]=='-':
            d=dpart
        else:
            continue
        fp=os.path.join(ZIP_DIR,name)
        try:
            size=os.path.getsize(fp); mtime=os.path.getmtime(fp)
        except Exception:
            size=0; mtime=0
        out.append({"date": d, "zip_name": name, "size": size, "mtime": mtime})
    try:
        out.sort(key=lambda x: x.get("date",""), reverse=True)
    except Exception:
        pass
    return out

# ---------------- ZIP 接口（客户端） ----------------
def _parse_range(hval: str, file_size: int) -> Optional[Tuple[int,int]]:
    if not hval: return None
    hval=hval.strip()
    if not hval.lower().startswith("bytes="): return None
    rs = hval.split("=",1)[1].strip()
    if "," in rs: return None  # 不支持多段
    if "-" not in rs: return None
    start_s, end_s = rs.split("-",1)
    if start_s=="":
        # 后缀 bytes：最后 N 字节
        try:
            length=int(end_s)
            if length<=0: return None
        except Exception:
            return None
        start=max(0, file_size - length)
        end=file_size-1
        return (start, end)
    try:
        start=int(start_s)
    except Exception:
        return None
    if end_s=="":
        end=file_size-1
    else:
        try: end=int(end_s)
        except Exception: return None
    if start> end or start>=file_size: return None
    return (start, min(end, file_size-1))

@app.get("/api/v1/pdf-zips/dates")
def api_pdf_zip_dates(code: str = Query(""), db=Depends(get_db)):
    c = verify_code(db, code)
    if not c: raise HTTPException(status_code=403, detail="invalid code")
    dates_db=set()
    try:
        rows=db.query(TrackingFile.uploaded_at).all()
        for (u,) in rows:
            if not u: continue
            dates_db.add(u.strftime("%Y-%m-%d"))
    except Exception:
        pass
    lst=list_pdf_zip_dates()
    dates_zip={x.get("date") for x in lst}
    for d in sorted(dates_db):
        if d not in dates_zip:
            lst.append({"date": d, "zip_name": f"pdfs-{d.replace('-','')}.zip", "size": 0, "mtime": 0})
    try:
        today=datetime.utcnow().date()
        if today.strftime("%Y-%m-%d") in dates_db:
            build_daily_pdf_zip(db, today)
    except Exception:
        pass
    try:
        lst.sort(key=lambda x: x.get("date",""), reverse=True)
    except Exception:
        pass
    return {"dates": lst}

@app.get("/api/v1/pdf-zips/daily")
def api_pdf_zip_daily(
    request: Request,
    date: Optional[str] = Query(None),
    code: str = Query(""),
    db=Depends(get_db),
):
    c = verify_code(db, code)
    if not c: raise HTTPException(status_code=403, detail="invalid code")
    if not date:
        d = datetime.utcnow().date()
    else:
        s=str(date).strip()
        if re.fullmatch(r"\d{8}", s):
            d=datetime(int(s[0:4]), int(s[4:6]), int(s[6:8])).date()
        elif re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
            d=datetime(int(s[0:4]), int(s[5:7]), int(s[8:10])).date()
        else:
            raise HTTPException(status_code=400, detail="invalid date")
    fp = os.path.join(ZIP_DIR, f"pdfs-{_date_str_compact(d)}.zip")
    if not os.path.exists(fp):
        try: fp = build_daily_pdf_zip(db, d)
        except Exception: pass
    if not os.path.exists(fp):
        raise HTTPException(status_code=404, detail="zip not found")

    etag = _calc_etag(fp)
    sha  = _calc_sha256(fp)
    size = os.path.getsize(fp)
    headers = {
        "ETag": etag, "Cache-Control": "no-cache",
        "X-Checksum-Sha256": sha if sha else "",
        "Accept-Ranges": "bytes",
        "X-Accel-Buffering": "no",
        "Content-Type": "application/zip",
        "Content-Disposition": f'attachment; filename="{os.path.basename(fp)}"',
    }

    # 304 短路
    inm = (request.headers.get("if-none-match") or "").strip()
    if (not request.headers.get("range")) and inm == etag and request.method != "HEAD":
        return Response(status_code=304, headers=headers)

    # HEAD：只发头
    if request.method == "HEAD":
        headers["Content-Length"] = str(size)
        return Response(status_code=200, headers=headers)

    # Range 支持（断点续传）
    rng = _parse_range(request.headers.get("range"), size)
    if rng:
        # If-Range 检查（如不匹配则忽略 Range）
        ifr = (request.headers.get("if-range") or "").strip()
        if ifr and ifr != etag:
            rng = None
    if rng:
        start, end = rng
        length = end - start + 1
        def file_iter():
            with open(fp, "rb") as f:
                f.seek(start)
                remaining = length
                chunk=1024*1024
                while remaining>0:
                    data=f.read(min(chunk, remaining))
                    if not data: break
                    remaining -= len(data)
                    yield data
        headers.update({
            "Content-Range": f"bytes {start}-{end}/{size}",
            "Content-Length": str(length),
        })
        return StreamingResponse(file_iter(), status_code=206, headers=headers, media_type="application/zip")
    else:
        # 全量
        headers["Content-Length"] = str(size)
        return FileResponse(fp, headers=headers, media_type="application/zip", filename=os.path.basename(fp))

# 兼容旧客户端路由
@app.get("/api/v1/packs/pdf/dates")
def api_pdf_zip_dates_compat(code: str = Query(""), db=Depends(get_db)):
    return api_pdf_zip_dates(code=code, db=db)

@app.get("/api/v1/packs/pdf/day")
def api_pdf_zip_day_compat(d: Optional[str] = Query(None), code: str = Query(""), request: Request = None, db=Depends(get_db)):
    return api_pdf_zip_daily(request=request, date=d, code=code, db=db)

# ---------------- 管理端：ZIP 列表/重建/下载 ----------------
def require_admin(request: Request, db):
    if not request.session.get("admin_user"):
        raise HTTPException(status_code=302, detail="redirect", headers={"Location": "/admin/login"})

@app.get("/admin/zips", response_class=HTMLResponse)
def admin_zips(request: Request, db=Depends(get_db)):
    require_admin(request, db)
    items = list_pdf_zip_dates()
    # 附加 etag/mtime_str
    out=[]
    for x in items:
        fp=os.path.join(ZIP_DIR, x["zip_name"])
        etag = _calc_etag(fp) if os.path.exists(fp) else ""
        mtime_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(x.get("mtime") or 0)) if x.get("mtime") else "-"
        out.append({**x, "etag": etag, "mtime_str": mtime_str, "exists": os.path.exists(fp)})
    return templates.TemplateResponse("zips.html", {"request": request, "rows": out})

@app.post("/admin/zips/rebuild")
def admin_zips_rebuild(request: Request, date: str = Form(...), pid: str = Form(""), db=Depends(get_db)):
    require_admin(request, db)
    # 解析日期
    s=str(date).strip()
    if re.fullmatch(r"\d{8}", s):
        d=datetime(int(s[0:4]), int(s[4:6]), int(s[6:8])).date()
    elif re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
        d=datetime(int(s[0:4]), int(s[5:7]), int(s[8:10])).date()
    else:
        raise HTTPException(status_code=400, detail="invalid date")

    if not pid: pid=new_progress("rebuild_zip")
    def _task():
        try:
            def cb(i,total,tn):
                set_progress(pid, stage="repackaging", pct=int(i*100/max(1,total)), note=str(tn))
            set_progress(pid, stage="repackaging", pct=0, note=_date_str(d))
            build_daily_pdf_zip(db, d, progress_cb=cb)
            set_progress(pid, stage="done", pct=100, done=True, note=_date_str(d))
        except Exception as e:
            set_progress(pid, stage="error", pct=100, ok=False, done=True, note=str(e))
    threading.Thread(target=_task, daemon=True).start()
    return JSONResponse({"ok": True, "id": pid})

@app.get("/admin/zip/download")
def admin_zip_download(request: Request, date: str = Query(...), db=Depends(get_db)):
    require_admin(request, db)
    # 和上面解析一致
    s=str(date).strip()
    if re.fullmatch(r"\d{8}", s):
        d=datetime(int(s[0:4]), int(s[4:6]), int(s[6:8])).date()
    elif re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
        d=datetime(int(s[0:4]), int(s[5:7]), int(s[8:10])).date()
    else:
        raise HTTPException(status_code=400, detail="invalid date")
    fp = os.path.join(ZIP_DIR, f"pdfs-{_date_str_compact(d)}.zip")
    if not os.path.exists(fp):
        try: fp = build_daily_pdf_zip(db, d)
        except Exception: pass
    if not os.path.exists(fp):
        raise HTTPException(status_code=404, detail="zip not found")
    return FileResponse(fp, media_type="application/zip", filename=os.path.basename(fp))

# ---------------- 管理端其它页面/登录 ----------------
@app.get("/admin/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/admin/login")
def login_do(request: Request, username: str = Form(...), password: str = Form(...), db=Depends(get_db)):
    u = db.execute(select(AdminUser).where(AdminUser.username==username, AdminUser.is_active==True)).scalar_one_or_none()
    if not u or not bcrypt.verify(password, u.password_hash):
        return templates.TemplateResponse("login.html", {"request": request, "error": "账户或密码错误"})
    request.session["admin_user"] = username
    return RedirectResponse("/admin", status_code=302)

@app.get("/admin/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/admin/login", status_code=302)

# ---------------- 在线升级/模板编辑（保持不变，略） ----------------
def run_cmd(cmd: str, cwd: Optional[str] = None, timeout: int = 60):
    p = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()

def git_status_info(base: str):
    repo = base
    git_dir = os.path.join(repo, ".git")
    if not os.path.isdir(git_dir):
        return {"mode": "nogit"}
    info = {"mode": "git", "repo": repo}
    _, branch, _ = run_cmd("git rev-parse --abbrev-ref HEAD", cwd=repo)
    _, origin, _ = run_cmd("git remote get-url origin", cwd=repo)
    run_cmd("git fetch --all --prune", cwd=repo)
    _, counts, _ = run_cmd(f"git rev-list --left-right --count HEAD...origin/{branch}", cwd=repo)
    ahead = behind = 0
    if counts:
        parts = counts.replace("\t"," ").split()
        if len(parts)>=2:
            ahead, behind = int(parts[0]), int(parts[1])
    _, local_log, _  = run_cmd('git log -1 --date=iso --pretty=format:"%h %cd %s"', cwd=repo)
    _, remote_log, _ = run_cmd(f'git log -1 origin/{branch} --date=iso --pretty=format:"%h %cd %s"', cwd=repo)
    info.update({
        "branch": branch or "",
        "origin": origin or "",
        "ahead": ahead,
        "behind": behind,
        "local": local_log.strip('"'),
        "remote": remote_log.strip('"'),
    })
    return info

@app.get("/admin/update", response_class=HTMLResponse)
def update_page(request: Request, db=Depends(get_db)):
    require_admin(request, db)
    info = git_status_info(BASE_DIR)
    oneliner = "bash <(curl -fsSL https://raw.githubusercontent.com/aidaddydog/huandan.server/main/scripts/bootstrap_online.sh)"
    return templates.TemplateResponse("update.html", {"request": request, "info": info, "oneliner": oneliner})

@app.post("/admin/update/git_pull")
def update_git_pull(request: Request, db=Depends(get_db)):
    require_admin(request, db)
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
    rc, out, err = run_cmd(f"bash {shlex.quote(os.path.join(BASE_DIR,'scripts','install_root.sh'))}", cwd=BASE_DIR, timeout=1800)
    if rc != 0:
        return PlainTextResponse(f"install 脚本执行失败：\n{out}\n{err}", status_code=500)
    return RedirectResponse("/admin/update?ok=1", status_code=302)

# ---- 模板编辑器 / 订单导入 / 文件管理（保持原接口，增进度） ----

TEMPLATE_ROOT = os.path.join(BASE_DIR, "app", "templates")

def _safe_template_rel(path: str) -> str:
    p = (path or "").replace("\\", "/").lstrip("/")
    if ".." in p or not p.endswith(".html"):
        raise HTTPException(status_code=400, detail="非法模板路径")
    return p

def _safe_template_abs(path: str) -> str:
    rel = _safe_template_rel(path)
    abs_path = os.path.abspath(os.path.join(TEMPLATE_ROOT, rel))
    if not abs_path.startswith(os.path.abspath(TEMPLATE_ROOT)+os.sep) and abs_path != os.path.abspath(TEMPLATE_ROOT):
        raise HTTPException(status_code=400, detail="非法模板路径")
    return abs_path

def _list_templates():
    out = []
    for root, _, files in os.walk(TEMPLATE_ROOT):
        for f in files:
            if f.endswith(".html"):
                abs_p = os.path.join(root, f)
                rel_p = os.path.relpath(abs_p, TEMPLATE_ROOT).replace("\\","/")
                out.append(rel_p)
    out.sort()
    return out

@app.get("/admin/templates", response_class=HTMLResponse)
def templates_list(request: Request, db=Depends(get_db)):
    require_admin(request, db)
    files = _list_templates()
    return templates.TemplateResponse("templates_list.html", {"request": request, "files": files})

@app.get("/admin/templates/edit", response_class=HTMLResponse)
def templates_edit(request: Request, path: str, db=Depends(get_db)):
    require_admin(request, db)
    abs_p = _safe_template_abs(path)
    if not os.path.exists(abs_p):
        raise HTTPException(status_code=404, detail="模板不存在")
    content = open(abs_p, "r", encoding="utf-8").read()
    return templates.TemplateResponse("templates_edit.html", {"request": request, "path": path, "content": content})

@app.post("/admin/templates/save")
def templates_save(request: Request, path: str = Form(...), content: str = Form(...), db=Depends(get_db)):
    require_admin(request, db)
    abs_p = _safe_template_abs(path)
    backup_dir = os.path.join(BASE_DIR, "updates", "template-backups", datetime.utcnow().strftime("%Y%m%d-%H%M%S"))
    os.makedirs(os.path.join(backup_dir, os.path.dirname(path)), exist_ok=True)
    if os.path.exists(abs_p):
        shutil.copy2(abs_p, os.path.join(backup_dir, path))
    os.makedirs(os.path.dirname(abs_p), exist_ok=True)
    with open(abs_p, "w", encoding="utf-8") as f:
        f.write(content)
    return RedirectResponse(f"/admin/templates/edit?path={path}&saved=1", status_code=302)

# ---- 导入订单（3步：文件→列映射→预览与确认） ----
@app.get("/admin/upload-orders", response_class=HTMLResponse)
def upload_orders_page(request: Request, db=Depends(get_db)):
    require_admin(request, db)
    return templates.TemplateResponse("upload_orders.html", {"request": request})

@app.post("/admin/upload-orders-step1", response_class=HTMLResponse)
async def upload_orders_step1(request: Request, file: UploadFile = File(...), db=Depends(get_db)):
    require_admin(request, db)
    tmp = os.path.join(UP_DIR, f"orders-{int(time.time())}-{re.sub(r'[^A-Za-z0-9_.-]+','_',file.filename)}")
    with open(tmp, "wb") as f:
        # 流式保存，便于超大文件
        while True:
            chunk = await file.read(1024*1024)
            if not chunk: break
            f.write(chunk)
    try:
        if tmp.lower().endswith(".csv"): df = pd.read_csv(tmp, nrows=1)
        else: df = pd.read_excel(tmp, nrows=1)
    except Exception as e:
        return templates.TemplateResponse("upload_orders.html", {"request": request, "err": f"读取失败：{e}"})
    request.session["last_orders_tmp"] = tmp
    return templates.TemplateResponse("choose_columns.html", {"request": request, "columns": list(df.columns)})

@app.post("/admin/upload-orders-step2", response_class=HTMLResponse)
def upload_orders_step2(request: Request, order_col: str = Form(...), tracking_col: str = Form(...), db=Depends(get_db)):
    require_admin(request, db)
    tmp = request.session.get("last_orders_tmp")
    if not tmp or not os.path.exists(tmp): return RedirectResponse("/admin/upload-orders", status_code=302)
    if tmp.lower().endswith(".csv"): df = pd.read_csv(tmp, dtype=str)
    else: df = pd.read_excel(tmp, dtype=str)
    df = df.fillna("")
    prev = df[[order_col, tracking_col]].head(50).values.tolist()
    request.session["orders_cols"] = {"order": order_col, "tracking": tracking_col}
    return templates.TemplateResponse("preview_orders.html", {"request": request, "rows": prev})

@app.post("/admin/upload-orders-step3")
def upload_orders_write(request: Request, progress_id: str = Form(""), db=Depends(get_db)):
    require_admin(request, db)
    tmp = request.session.get("last_orders_tmp")
    cols = request.session.get("orders_cols") or {}
    if not tmp or not os.path.exists(tmp) or "order" not in cols or "tracking" not in cols:
        return RedirectResponse("/admin/upload-orders", status_code=302)
    if tmp.lower().endswith(".csv"): df = pd.read_csv(tmp, dtype=str)
    else: df = pd.read_excel(tmp, dtype=str)
    df = df.fillna("")
    total = len(df)
    pid = progress_id or new_progress("import_orders")
    set_progress(pid, stage="writing", pct=0, note=f"0/{total}")
    count = 0
    now = datetime.utcnow()
    try:
        for i, r in df.iterrows():
            oid = str(r[cols["order"]]).strip()
            tn  = canon_tracking(str(r[cols["tracking"]]).strip())
            if oid and tn:
                m = db.get(OrderMapping, oid)
                if not m:
                    m = OrderMapping(order_id=oid, tracking_no=tn, updated_at=now); db.add(m)
                else:
                    m.tracking_no = tn; m.updated_at = now
                count += 1
            if (i+1) % 200 == 0 or (i+1)==total:
                db.commit()
                set_progress(pid, stage="writing", pct=int((i+1)*100/max(1,total)), note=f"{i+1}/{total}")
        set_mapping_version(db); write_mapping_json(db)
        set_progress(pid, stage="done", pct=100, done=True, note=f"{count} rows")
    except Exception as e:
        db.rollback()
        set_progress(pid, stage="error", pct=100, done=True, ok=False, note=str(e))
        return PlainTextResponse(f"写入失败：{e}", status_code=500)
    finally:
        try: os.remove(tmp)
        except Exception: pass
        request.session.pop("last_orders_tmp", None); request.session.pop("orders_cols", None)
    return RedirectResponse(f"/admin/orders?ok={count}&pid={pid}", status_code=302)

# ---- PDF 上传/列表/删除（上传含进度 + 解压 + 重打包） ----
@app.get("/admin/upload-pdf", response_class=HTMLResponse)
def upload_pdf_page(request: Request, db=Depends(get_db)):
    require_admin(request, db)
    return templates.TemplateResponse("upload_pdf.html", {"request": request})

@app.post("/admin/upload-pdf")
async def upload_pdf_zip(request: Request, zipfile_upload: UploadFile = File(...), progress_id: str = Form(""), db=Depends(get_db)):
    require_admin(request, db)
    pid = progress_id or new_progress("upload_pdfs")
    total_len = int(request.headers.get("content-length") or 0)
    tmp_zip = os.path.join(UP_DIR, f"pdfs-{int(time.time())}-{re.sub(r'[^A-Za-z0-9_.-]+','_',zipfile_upload.filename)}")
    os.makedirs(os.path.dirname(tmp_zip), exist_ok=True)
    # 1) 上传进度（流式落盘）
    set_progress(pid, stage="uploading", pct=0, note=zipfile_upload.filename)
    read_bytes=0
    with open(tmp_zip, "wb") as f:
        while True:
            chunk = await zipfile_upload.read(1024*1024)
            if not chunk: break
            f.write(chunk); read_bytes += len(chunk)
            if total_len>0:
                pct = min(95, int(read_bytes*100/total_len))
                set_progress(pid, stage="uploading", pct=pct, note=f"{read_bytes//(1024*1024)}MB")
            else:
                # 无总长时，仅刷新提示
                set_progress(pid, stage="uploading", pct=min(95, PROGRESS[pid]["pct"]+1), note=f"{read_bytes//(1024*1024)}MB")

    saved=0; skipped=0
    # 2) 解压进度
    set_progress(pid, stage="extracting", pct=0, note="scanning...")
    try:
        with zipfile.ZipFile(tmp_zip, "r") as z:
            infos=[i for i in z.infolist() if not i.is_dir() and i.filename.lower().endswith(".pdf")]
            total_bytes = sum(i.file_size for i in infos) or 1
            done_bytes = 0
            for info in infos:
                tracking = canon_tracking(os.path.splitext(os.path.basename(info.filename))[0])
                if not tracking: skipped += 1; continue
                target = os.path.join(PDF_DIR, f"{tracking}.pdf")
                os.makedirs(os.path.dirname(target), exist_ok=True)
                with z.open(info) as src, open(target,"wb") as dst:
                    while True:
                        buf = src.read(1024*256)
                        if not buf: break
                        dst.write(buf); done_bytes += len(buf)
                        set_progress(pid, stage="extracting", pct=min(99, int(done_bytes*100/total_bytes)), note=tracking)
                tf = db.get(TrackingFile, tracking)
                if not tf:
                    tf = TrackingFile(tracking_no=tracking, file_path=target, uploaded_at=datetime.utcnow()); db.add(tf)
                else:
                    tf.file_path = target; tf.uploaded_at = datetime.utcnow()
                saved += 1
        db.commit()
        set_mapping_version(db); write_mapping_json(db)
    except Exception as e:
        db.rollback()
        set_progress(pid, stage="error", pct=100, ok=False, done=True, note=f"解压失败: {e}")
        try: os.remove(tmp_zip)
        except Exception: pass
        return PlainTextResponse(f"处理失败：{e}", status_code=500)

    # 3) 重建当日 ZIP（重打包进度）
    try:
        today=datetime.utcnow().date()
        def cb(i,total,tn): set_progress(pid, stage="repackaging", pct=int(i*100/max(1,total)), note=str(tn))
        build_daily_pdf_zip(db, today, progress_cb=cb)
    except Exception as e:
        set_progress(pid, stage="warn", pct=100, note=f"重建ZIP失败: {e}")
    finally:
        set_progress(pid, stage="done", pct=100, done=True, note=f"导入{saved}，跳过{skipped}")
        try: os.remove(tmp_zip)
        except Exception: pass

    return RedirectResponse(f"/admin/files?ok={saved}&skipped={skipped}&pid={pid}", status_code=302)

@app.get("/admin/files", response_class=HTMLResponse)
def list_files(request: Request, q: Optional[str]=None, page: int=1, db=Depends(get_db)):
    require_admin(request, db); cleanup_expired(db)
    page_size=100
    query = db.query(TrackingFile)
    if q: query = query.filter(TrackingFile.tracking_no.like(f"%{q}%"))
    total = query.count()
    rows = query.order_by(TrackingFile.uploaded_at.desc()).offset((page-1)*page_size).limit(page_size).all()
    pages = max(1, math.ceil(total/page_size))
    return templates.TemplateResponse("files.html", {"request": request, "rows": rows, "q": q, "page": page, "pages": pages, "total": total, "page_size": page_size})

@app.post("/admin/files/batch_delete_all")
def file_batch_delete_all(request: Request, q: str = Form(""), db=Depends(get_db)):
    require_admin(request, db)
    targets = db.query(TrackingFile).filter(TrackingFile.tracking_no.like(f"%{q}%")).all() if q else db.query(TrackingFile).all()
    cnt=0
    for tf in targets:
        try:
            if tf.file_path and os.path.exists(tf.file_path): os.remove(tf.file_path)
        except Exception: pass
        db.delete(tf); cnt+=1
    db.commit()
    if cnt>0: set_mapping_version(db); write_mapping_json(db)
    return RedirectResponse(f"/admin/files?ok={cnt}&q={q}", status_code=302)

@app.get("/admin/file/{tracking_no}")
def admin_file_download(tracking_no: str, request: Request, db=Depends(get_db)):
    require_admin(request, db)
    def _find(tr):
        cand = [tr, canon_tracking(tr)]
        for t in cand:
            fp = os.path.join(PDF_DIR, f"{t}.pdf")
            if os.path.exists(fp): return fp
        tn = f"{tr}.pdf".lower()
        for name in os.listdir(PDF_DIR):
            if name.lower()==tn: return os.path.join(PDF_DIR,name)
        return None
    fp = _find(tracking_no)
    if not fp: raise HTTPException(status_code=404, detail="file not found")
    return FileResponse(fp, media_type="application/pdf", filename=os.path.basename(fp))

# ---- 订单列表/批删 / 客户端访问码 / 设置 / 对齐（不变） ----
@app.get("/admin/orders", response_class=HTMLResponse)
def list_orders(request: Request, q: Optional[str]=None, page: int=1, db=Depends(get_db)):
    require_admin(request, db); cleanup_expired(db)
    page_size=100
    query = db.query(OrderMapping)
    if q: query = query.filter(OrderMapping.order_id.like(f"%{q}%"))
    total = query.count()
    rows = query.order_by(OrderMapping.updated_at.desc()).offset((page-1)*page_size).limit(page_size).all()
    pages = max(1, math.ceil(total/page_size))
    return templates.TemplateResponse("orders.html", {"request": request, "rows": rows, "q": q, "page": page, "pages": pages, "total": total, "page_size": page_size})

@app.post("/admin/orders/batch_delete_all")
def orders_batch_delete_all(request: Request, q: str = Form(""), db=Depends(get_db)):
    require_admin(request, db)
    if q: db.query(OrderMapping).filter(OrderMapping.order_id.like(f"%{q}%")).delete()
    else: db.query(OrderMapping).delete()
    db.commit(); set_mapping_version(db); write_mapping_json(db)
    return RedirectResponse(f"/admin/orders?q={q}", status_code=302)

@app.get("/admin/clients", response_class=HTMLResponse)
def clients_page(request: Request, db=Depends(get_db)):
    require_admin(request, db)
    rows = db.query(ClientAuth).order_by(ClientAuth.created_at.desc()).all()
    return templates.TemplateResponse("clients.html", {"request": request, "rows": rows})

@app.post("/admin/clients/add")
def clients_add(request: Request, code6: str = Form(...), description: str = Form(""), db=Depends(get_db)):
    require_admin(request, db)
    if not code6.isdigit() or len(code6)!=6:
        return RedirectResponse("/admin/clients", status_code=302)
    db.add(ClientAuth(code_plain=code6, description=description, is_active=True)); db.commit()
    return RedirectResponse("/admin/clients", status_code=302)

@app.post("/admin/clients/toggle")
def clients_toggle(request: Request, client_id: int = Form(...), db=Depends(get_db)):
    require_admin(request, db)
    c = db.get(ClientAuth, client_id)
    if c: c.is_active = not c.is_active; db.commit()
    return RedirectResponse("/admin/clients", status_code=302)

@app.post("/admin/clients/delete")
def clients_delete(request: Request, client_id: int = Form(...), db=Depends(get_db)):
    require_admin(request, db)
    c = db.get(ClientAuth, client_id)
    if c: db.delete(c); db.commit()
    return RedirectResponse("/admin/clients", status_code=302)

@app.get("/admin/settings", response_class=HTMLResponse)
def settings_page(request: Request, db=Depends(get_db)):
    require_admin(request, db)
    return templates.TemplateResponse("settings.html", {
        "request": request,
        "o_days": get_kv(db,'retention_orders_days','30'),
        "f_days": get_kv(db,'retention_files_days','30'),
        "server_version": get_kv(db,"server_version","server-20250916b"),
        "client_recommend": get_kv(db,"client_recommend","client-20250916b")
    })

@app.post("/admin/settings")
def settings_save(request: Request,
                  retention_orders_days: str = Form(...),
                  retention_files_days: str = Form(...),
                  server_version: str = Form(...),
                  client_recommend: str = Form(...),
                  db=Depends(get_db)):
    require_admin(request, db)
    set_kv(db,"retention_orders_days", retention_orders_days or "30")
    set_kv(db,"retention_files_days", retention_files_days or "30")
    set_kv(db,"server_version", server_version or "server-20250916b")
    set_kv(db,"client_recommend", client_recommend or "client-20250916b")
    cleanup_expired(db)
    return RedirectResponse("/admin", status_code=302)

def cleanup_expired(db):
    o_days = int(get_kv(db, 'retention_orders_days', '0') or '0')
    f_days = int(get_kv(db, 'retention_files_days', '0') or '0')
    if o_days > 0:
        dt = datetime.utcnow() - timedelta(days=o_days)
        db.query(OrderMapping).filter(OrderMapping.updated_at < dt).delete()
    if f_days > 0:
        dt = datetime.utcnow() - timedelta(days=f_days)
        olds = db.query(TrackingFile).filter(TrackingFile.uploaded_at < dt).all()
        for r in olds:
            try:
                if r.file_path and os.path.exists(r.file_path): os.remove(r.file_path)
            except Exception:
                pass
            db.delete(r)
    db.commit()

# ---------------- 客户端 API 版本/映射/文件/运行时 ----------------
@app.get("/api/v1/version")
def api_version(code: str = Query(""), db=Depends(get_db)):
    c = verify_code(db, code)
    if not c: raise HTTPException(status_code=403, detail="invalid code")
    return JSONResponse({
        "version": get_mapping_version(db),
        "list_version": get_mapping_version(db),
        "server_version": get_kv(db,"server_version","server-20250916b"),
        "client_recommend": get_kv(db,"client_recommend","client-20250916b"),
    })

@app.get("/api/v1/mapping")
def api_mapping(code: str = Query(""), db=Depends(get_db)):
    c = verify_code(db, code)
    if not c: raise HTTPException(status_code=403, detail="invalid code")
    return _build_mapping_payload(db)

@app.get("/api/v1/file/{tracking_no}")
def api_file(tracking_no: str, code: str = Query(""), db=Depends(get_db)):
    c = verify_code(db, code)
    if not c: raise HTTPException(status_code=403, detail="invalid code")
    def _find(tr):
        cand = [tr, canon_tracking(tr)]
        for t in cand:
            fp = os.path.join(PDF_DIR, f"{t}.pdf")
            if os.path.exists(fp): return fp
        tn = f"{tr}.pdf".lower()
        for name in os.listdir(PDF_DIR):
            if name.lower()==tn: return os.path.join(PDF_DIR,name)
        return None
    fp = _find(tracking_no)
    if not fp: raise HTTPException(status_code=404, detail="file not found")
    return FileResponse(fp, media_type="application/pdf", filename=os.path.basename(fp))

@app.get("/api/v1/runtime/sumatra")
def api_runtime_sumatra(arch: str = "win64", code: str = Query(""), db=Depends(get_db)):
    c = verify_code(db, code)
    if not c: raise HTTPException(status_code=403, detail="invalid code")
    fname = "SumatraPDF-3.5.2-64.exe" if arch=="win64" else "SumatraPDF-3.5.2-32.exe"
    fp = os.path.join(BASE_DIR, "runtime", fname)
    if not os.path.exists(fp): raise HTTPException(status_code=404, detail="runtime not found on server")
    return FileResponse(fp, media_type="application/octet-stream", filename=fname)

# ---------------- 认证/清理/路由自检 ----------------
def is_locked(c: ClientAuth) -> bool:
    return bool(c.locked_until and datetime.utcnow() < c.locked_until)

def verify_code(db, code: str):
    if not code or not code.isdigit() or len(code)!=6: return None
    rows = db.execute(select(ClientAuth).where(ClientAuth.is_active==True)).scalars().all()
    for c in rows:
        if is_locked(c): continue
        if (c.code_plain == code) or (c.code_hash and bcrypt.verify(code, c.code_hash)):
            c.last_used = datetime.utcnow(); c.fail_count = 0; c.locked_until=None; db.commit(); return c
    for c in rows:
        c.fail_count = (c.fail_count or 0) + 1
        if c.fail_count >= 5: c.locked_until = datetime.utcnow() + timedelta(minutes=5)
    db.commit(); return None

@app.get("/__routes__")
def __routes__():
    return [{"path": r.path, "methods": list(getattr(r, "methods", []))} for r in app.routes]
