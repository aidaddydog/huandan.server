import os
from typing import List
from app.repositories.base import with_conn
from app.core.config import PDF_DIR

@with_conn
def get_pdf_paths_by_tracking_nos(conn, tracking_nos: List[str]) -> List[str]:
    paths, uniq = [], []
    for n in tracking_nos:
        n = (n or "").strip()
        if n and n not in uniq: uniq.append(n)
    # DB 优先（若有 file_path 字段）
    if conn and uniq:
        try:
            q = ",".join("?" for _ in uniq)
            rows = conn.execute(f"SELECT file_path FROM TrackingFile WHERE tracking_no IN ({q})", uniq).fetchall()
            for r in rows:
                p = r[0]
                if p and os.path.exists(p): paths.append(p)
        except Exception:
            pass
    # 回退：storage/pdfs/{tracking}.pdf
    for n in uniq:
        p = os.path.join(PDF_DIR, f"{n}.pdf")
        if os.path.exists(p): paths.append(p)
    return paths

def list_pdfs() -> List[str]:
    if not os.path.isdir(PDF_DIR): return []
    files = []
    for name in os.listdir(PDF_DIR):
        if name.lower().endswith('.pdf'):
            files.append(os.path.join(PDF_DIR, name))
    return files

