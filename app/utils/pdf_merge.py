from io import BytesIO
from typing import List
from pypdf import PdfReader, PdfWriter
def merge_pdfs(paths: List[str]) -> BytesIO:
    writer = PdfWriter()
    for p in paths:
        try:
            r = PdfReader(p)
            for page in r.pages:
                writer.add_page(page)
        except Exception as e:
            print(f"[WARN] 合并失败: {p} -> {e}")
            continue
    buf = BytesIO()
    writer.write(buf)
    buf.seek(0)
    return buf

