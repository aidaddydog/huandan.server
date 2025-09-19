from fastapi import APIRouter, Query
from typing import Dict, Any
from app.repositories.mapping_repo import get_mappings

router = APIRouter()

@router.get("/orders")
def list_orders(page:int=1, size:int=50, q:str="") -> Dict[str, Any]:
    data = get_mappings()
    if q:
        ql = q.strip().lower()
        data = [r for r in data if ql in str(r).lower()]
    total = len(data)
    start = max(0, (page-1)*size); end = start+size
    return {"code":0, "message":"ok", "data":{"total": total, "rows": data[start:end]}}

