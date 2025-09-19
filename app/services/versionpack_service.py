import os, shutil, json
from pathlib import Path
from typing import Dict, List
from app.core.config import UPDATES_DIR, PDF_DIR, DATA_DIR
from app.repositories.mapping_repo import get_mappings
from app.utils.fs_utils import build_zip, timestamp

PACK_DIR = UPDATES_DIR / "packs"

def build_version_pack() -> Dict:
    PACK_DIR.mkdir(parents=True, exist_ok=True)
    ver_date = timestamp().split('-')[0]
    # 计算当日序号
    existing = [p for p in PACK_DIR.glob(f"{ver_date}-*.zip")]
    seq = len(existing) + 1
    ver = f"{ver_date}-{seq:02d}"
    tmp_dir = UPDATES_DIR / f"pack_{ver}"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    # 写 mapping.json（按当前 get_mappings）
    mappings = get_mappings(None)
    (tmp_dir / "mapping.json").write_text(json.dumps(mappings, ensure_ascii=False, indent=2), encoding="utf-8")
    # 拷贝 pdfs（全部）
    out_pdfs = tmp_dir / "pdfs"
    out_pdfs.mkdir(exist_ok=True)
    for root, _, files in os.walk(PDF_DIR):
        for fn in files:
            if fn.lower().endswith(".pdf"):
                src = Path(root) / fn
                shutil.copy2(src, out_pdfs / fn)
    # 打包
    zip_path = PACK_DIR / f"{ver}.zip"
    build_zip(tmp_dir, zip_path)
    shutil.rmtree(tmp_dir, ignore_errors=True)
    return {"version": ver, "url": f"/updates/packs/{ver}.zip"}

def list_packs() -> List[Dict]:
    PACK_DIR.mkdir(parents=True, exist_ok=True)
    res = []
    for p in sorted(PACK_DIR.glob("*.zip")):
        res.append({"version": p.stem, "size": p.stat().st_size, "url": f"/updates/packs/{p.name}"})
    return res

def rollback_pack(version: str) -> Dict:
    # 简化：仅回滚 mapping.json（pdfs 可按需手动解压覆盖）
    zip_path = PACK_DIR / f"{version}.zip"
    if not zip_path.exists():
        return {"error": "version not found"}
    import zipfile
    with zipfile.ZipFile(zip_path) as z:
        try:
            content = z.read("mapping.json").decode("utf-8")
            (DATA_DIR / "mapping.json").write_text(content, encoding="utf-8")
        except Exception:
            return {"error": "mapping.json missing in pack"}
    return {"rolled_back": version}

