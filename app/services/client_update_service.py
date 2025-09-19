import json, os
from pathlib import Path
from typing import Dict
from fastapi import UploadFile
from app.core.config import CLIENT_UPD_DIR
LATEST = CLIENT_UPD_DIR / "latest.json"
def get_latest_meta() -> Dict:
    if not LATEST.exists():
        return {"version":"v0.0.0","url":"","notes":"","force":False}
    try:
        return json.loads(LATEST.read_text(encoding="utf-8"))
    except Exception:
        return {"version":"v0.0.0","url":"","notes":"","force":False}
def save_latest_meta(meta: Dict):
    CLIENT_UPD_DIR.mkdir(parents=True, exist_ok=True)
    LATEST.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
async def save_package_and_update_meta(file: UploadFile, version: str, notes: str, force: bool=False) -> Dict:
    CLIENT_UPD_DIR.mkdir(parents=True, exist_ok=True)
    ext = os.path.splitext(file.filename or "")[1] or ".zip"
    pkg_name = f"huandan_client_{version}{ext}"
    pkg_path = CLIENT_UPD_DIR / pkg_name
    with open(pkg_path, "wb") as f:
        while True:
            chunk = await file.read(8192)
            if not chunk: break
            f.write(chunk)
    meta = {"version": version, "url": f"/updates/client/{pkg_name}", "notes": notes, "force": force}
    save_latest_meta(meta)
    return meta

