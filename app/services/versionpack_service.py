import os, shutil, json, zipfile
from pathlib import Path
from typing import Dict, List
from app.core.config import UPDATES_DIR, PDF_DIR, DATA_DIR
from app.repositories.mapping_repo import get_mappings
from app.utils.fs_utils import timestamp
PACK_DIR = UPDATES_DIR / "packs"
def build_version_pack() -> Dict:
    PACK_DIR.mkdir(parents=True, exist_ok=True)
    ver_date = timestamp().split('-')[0]
    existing = [p for p in PACK_DIR.glob(f"{ver_date}-*.zip")]
    seq = len(existing) + 1
    ver = f"{ver_date}-{seq:02d}"
    tmp_dir = UPDATES_DIR / f"pack_{ver}"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    (tmp_dir / "mapping.json").write_text(json.dumps(get_mappings(None), ensure_ascii=False, indent=2), encoding="utf-8")
    out_pdfs = tmp_dir / "pdfs"; out_pdfs.mkdir(exist_ok=True)
    for root, _, files in os.walk(PDF_DIR):
        for fn in files:
            if fn.lower().endswith(".pdf"):
                src = Path(root) / fn
                shutil.copy2(src, out_pdfs / fn)
    zip_path = PACK_DIR / f"{ver}.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
        for r, _, fs in os.walk(tmp_dir):
            for fn in fs:
                full = Path(r)/fn
                z.write(full, full.relative_to(tmp_dir).as_posix())
    shutil.rmtree(tmp_dir, ignore_errors=True)
    return {"version": ver, "url": f"/updates/packs/{ver}.zip"}
def list_packs() -> List[Dict]:
    PACK_DIR.mkdir(parents=True, exist_ok=True)
    return [{"version": p.stem, "size": p.stat().st_size, "url": f"/updates/packs/{p.name}"} for p in sorted(PACK_DIR.glob("*.zip"))]
def rollback_pack(version: str) -> Dict:
    zip_path = PACK_DIR / f"{version}.zip"
    if not zip_path.exists():
        return {"error": "version not found"}
    with zipfile.ZipFile(zip_path) as z:
        try:
            content = z.read("mapping.json").decode("utf-8")
            (DATA_DIR / "mapping.json").write_text(content, encoding="utf-8")
        except Exception:
            return {"error": "mapping.json missing in pack"}
    return {"rolled_back": version}

