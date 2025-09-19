import os, zipfile, hashlib, time
from pathlib import Path
from typing import Tuple
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
                content = z.read(m.filename)
                out = target_dir / name
                with open(out, 'wb') as f: f.write(content)
                ok += 1
            except Exception:
                fail += 1
    return ok, fail
def timestamp() -> str:
    return time.strftime('%Y%m%d-%H%M%S')

