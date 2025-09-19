from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import StreamingResponse
from typing import List, Dict, Any
from app.services.print_service import build_merged_pdf_stream
from app.repositories.mapping_repo import mark_printed
router = APIRouter()
@router.post("/print/merge")
def merge_print(payload: Dict[str, Any] = Body(...)):
    tracking_nos: List[str] = payload.get("tracking_nos") or []
    if not tracking_nos:
        raise HTTPException(status_code=400, detail="tracking_nos 不能为空")
    stream, filename = build_merged_pdf_stream(tracking_nos)
    headers = {"Content-Disposition": f'inline; filename="{filename}"'}
    return StreamingResponse(stream, media_type="application/pdf", headers=headers)
@router.post("/print/report")
def report_print(payload: Dict[str, Any] = Body(...)):
    t = (payload.get("tracking_no") or "").strip()
    ok = bool(payload.get("success", False))
    if not t:
        raise HTTPException(status_code=400, detail="tracking_no 不能为空")
    if ok: mark_printed(t)
    return {"code": 0, "message": "ok", "data": {"tracking_no": t, "printed": ok}}

