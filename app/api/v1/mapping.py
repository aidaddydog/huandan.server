from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.repositories.mapping_repo import get_mappings, get_mapping_version, find_by_order_or_customer
from app.repositories.file_repo import get_pdf_paths_by_tracking_nos
from app.core.config import RUNTIME_DIR
router = APIRouter()
@router.get("/version")
def get_version(code: str):
    return {"version": get_mapping_version()}
@router.get("/mapping")
def get_mapping(code: str):
    return {"version": get_mapping_version(), "mappings": get_mappings()}
@router.get("/file/{tracking_no}")
def get_file(tracking_no: str, code: str):
    paths = get_pdf_paths_by_tracking_nos([tracking_no])
    if not paths: raise HTTPException(status_code=404, detail="file not found")
    return FileResponse(paths[0], media_type="application/pdf")
@router.get("/runtime/sumatra")
def get_sumatra(arch: str="win64", code: str=""):
    f = RUNTIME_DIR / "SumatraPDF.exe"
    if not f.exists(): raise HTTPException(status_code=404, detail="runtime not found")
    return FileResponse(f, media_type="application/octet-stream", filename="SumatraPDF.exe")
@router.get("/lookup")
def lookup_one(code: str, order_id: str):
    rec = find_by_order_or_customer(order_id)
    if not rec: raise HTTPException(status_code=404, detail="not found")
    tracking = rec.get("tracking_no") or ""
    return {"order_id": rec.get("order_id"), "tracking_no": tracking, "pdf_url": f"/api/v1/file/{tracking}?code={code}" if tracking else ""}

