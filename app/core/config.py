import os
from pathlib import Path

APP_NAME = os.getenv("APP_NAME", "huandan")
APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT = int(os.getenv("APP_PORT", "8000"))

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = Path(os.getenv("DATA_DIR", str(BASE_DIR / "data")))
STORAGE_DIR = Path(os.getenv("STORAGE_DIR", str(BASE_DIR / "storage")))
PDF_DIR = STORAGE_DIR / "pdfs"
UPDATES_DIR = Path(os.getenv("UPDATES_DIR", str(BASE_DIR / "updates")))
CLIENT_UPD_DIR = UPDATES_DIR / "client"
JOBS_DIR = UPDATES_DIR / "jobs"
RUNTIME_DIR = BASE_DIR / "runtime"

DB_PATH = DATA_DIR / "app.db"  # 可选

for d in (DATA_DIR, PDF_DIR, CLIENT_UPD_DIR, JOBS_DIR):
    d.mkdir(parents=True, exist_ok=True)

