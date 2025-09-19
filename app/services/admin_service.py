import os, shutil
from app.core.config import DATA_DIR, STORAGE_DIR, UPDATES_DIR
from app.utils.fs_utils import timestamp

def dangerous_clear(mode: str = "all"):
    backup_dir = UPDATES_DIR / f"backup-{timestamp()}"
    backup_dir.mkdir(parents=True, exist_ok=True)
    if DATA_DIR.exists(): shutil.copytree(DATA_DIR, backup_dir / "data")
    if (STORAGE_DIR / "pdfs").exists(): shutil.copytree(STORAGE_DIR / "pdfs", backup_dir / "pdfs")
    if mode in ("mapping","all"):
        (DATA_DIR / "mapping.json").write_text("[]", encoding="utf-8")
    if mode in ("pdfs","all"):
        pdf_dir = STORAGE_DIR / "pdfs"
        if pdf_dir.exists():
            for fn in os.listdir(pdf_dir):
                fp = pdf_dir / fn
                if os.path.isfile(fp): os.unlink(fp)
    return {"backup": str(backup_dir), "cleared": mode}

