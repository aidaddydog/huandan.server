from typing import Dict, List
from fastapi import UploadFile
from app.utils.excel_csv import parse_csv, parse_xlsx
from app.repositories.mapping_repo import upsert_mappings
from app.utils.fs_utils import unzip_to_dir
from app.core.config import PDF_DIR

def _normalize_rows(rows: List[dict]) -> List[dict]:
    def pick(obj: dict, keys: List[str]) -> str:
        for k in keys:
            if k in obj and obj[k]: return str(obj[k]).strip()
        return ""
    normalized = []
    for r in rows:
        normalized.append({
            "order_id": pick(r, ["order_id", "订单号", "order", "订单"]),
            "customer_order": pick(r, ["customer_order", "客户单号"]),
            "tracking_no": pick(r, ["tracking_no", "tracking", "运单号"]),
            "transfer_no": pick(r, ["transfer_no", "转单号"]),
            "channel_code": pick(r, ["channel_code", "channel", "渠道"]),
            "platform": pick(r, ["platform", "平台"]),
            "shop_name": pick(r, ["shop_name", "店铺"]),
            "buyer_id": pick(r, ["buyer_id", "客户ID"]),
            "country": pick(r, ["country", "国家"]),
            "postal_code": pick(r, ["postal_code", "邮编"]),
            "sku_summary": pick(r, ["sku_summary", "sku", "商品摘要"]),
        })
    return normalized

async def import_orders_file(file: UploadFile) -> Dict:
    content = await file.read()
    name = (file.filename or "").lower()
    if name.endswith(".csv"):
        rows = parse_csv(content)
    elif name.endswith((".xlsx",".xlsm",".xls")):
        rows = parse_xlsx(content)
    else:
        return {"error": "仅支持 CSV/XLSX"}
    normalized = _normalize_rows(rows)
    stat = upsert_mappings(normalized)
    return {"inserted": stat["inserted"], "updated": stat["updated"], "total": stat["total"]}

async def import_pdfs_zip(file: UploadFile) -> Dict:
    ok, fail = unzip_to_dir(file.file, PDF_DIR)
    return {"imported": ok, "skipped": fail}

