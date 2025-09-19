import os, shutil, zipfile, hashlib, time
from pathlib import Path
from typing import List, Tuple
from app.core.config import STORAGE_DIR, PDF_DIR, UPDATES_DIR

def ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)

def sha1_of_file(path: Path, block=1024*1024) -> str:
    h = hashlib.sha1()
    with open(path, 'rb') as f:
        while True:
            b = f.read(block)
            if not b: break
            h.update(b)
    return h.hexdigest()

def unzip_to_dir(zip_file, target_dir: Path) -> Tuple[int, int]:
    ensure_dir(target_dir)
    ok = fail = 0
    with zipfile.ZipFile(zip_file) as z:
        for m in z.infolist():
            if m.is_dir(): continue
            name = Path(m.filename).name
            if not name.lower().endswith('.pdf'): 
                fail += 1; continue
            try:
                # 统一放置到 pdfs 目录
                content = z.read(m.filename)
                out = target_dir / name
                with open(out, 'wb') as f: f.write(content)
                ok += 1
            except Exception:
                fail += 1
    return ok, fail

def build_zip(src_dir: Path, zip_path: Path):
    ensure_dir(zip_path.parent)
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(src_dir):
            for fn in files:
                full = Path(root) / fn
                z.write(full, full.relative_to(src_dir).as_posix())

def timestamp() -> str:
    return time.strftime('%Y%m%d-%H%M%S')

