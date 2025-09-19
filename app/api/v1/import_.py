from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.import_service import import_orders_file, import_pdfs_zip
from app.services.align_service import scan_alignment, fix_alignment
from app.services.versionpack_service import build_version_pack, list_packs, rollback_pack
from app.services.admin_service import dangerous_clear

router = APIRouter()

@router.post("/import/orders")
async def import_orders(file: UploadFile = File(...)):
    return await import_orders_file(file)

@router.post("/import/pdfs_zip")
async def import_pdfs(file: UploadFile = File(...)):
    return await import_pdfs_zip(file)

@router.get("/align/scan")
def align_scan():
    return scan_alignment()

@router.post("/align/fix")
def align_fix():
    return fix_alignment(add_mapping_from_orphan=True)

@router.post("/version/build")
def version_build():
    return build_version_pack()

@router.get("/version/list")
def version_list():
    return {"packs": list_packs()}

@router.post("/version/rollback")
def version_rollback(version: str):
    res = rollback_pack(version)
    if "error" in res: raise HTTPException(status_code=400, detail=res["error"])
    return res

@router.post("/admin/clear")
def admin_clear(mode: str = "all"):
    return dangerous_clear(mode)

