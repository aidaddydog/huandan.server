from io import BytesIO
from typing import List, Tuple
from app.repositories.file_repo import get_pdf_paths_by_tracking_nos
from app.utils.pdf_merge import merge_pdfs
def build_merged_pdf_stream(tracking_nos: List[str]) -> Tuple[BytesIO, str]:
    uniq = list(dict.fromkeys([x.strip() for x in tracking_nos if x and x.strip()]))
    pdf_paths = get_pdf_paths_by_tracking_nos(uniq)
    if not pdf_paths:
        raise ValueError("未找到对应面单文件")
    buf = merge_pdfs(pdf_paths)
    filename = f"labels_{len(pdf_paths)}.pdf"
    return buf, filename

