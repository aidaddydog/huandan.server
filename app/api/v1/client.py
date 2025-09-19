from fastapi import APIRouter, UploadFile, Form
from fastapi.responses import JSONResponse
from app.services.client_update_service import get_latest_meta, save_package_and_update_meta
router = APIRouter()
@router.get("/client/update/check")
def check_update(ver: str, arch: str="win64", code: str=""):
    meta = get_latest_meta()
    return JSONResponse(content={"code":0, "message":"ok", "data": meta})
@router.post("/client/update/upload")
async def upload_client_package(file: UploadFile, version: str = Form(...), notes: str = Form(""), force: bool = Form(False)):
    meta = await save_package_and_update_meta(file, version, notes, force)
    return {"code": 0, "message": "uploaded", "data": meta}

