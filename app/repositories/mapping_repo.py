import json, time
from pathlib import Path
from typing import List, Dict, Optional
from app.repositories.base import with_conn
from app.core.config import DATA_DIR

def _mapping_file() -> Path:
    return DATA_DIR / "mapping.json"

@with_conn
def get_mappings(conn) -> List[Dict]:
    if conn:
        try:
            rows = conn.execute("""
                SELECT om.order_id, om.tracking_no, om.updated_at,
                       om.customer_order, om.platform, om.shop_name,
                       om.buyer_id, om.country, om.postal_code, om.channel_name,
                       om.printed_at, om.shipped_at, om.transfer_no, om.sku_summary
                  FROM OrderMapping om
                ORDER BY om.updated_at DESC
            """).fetchall()
            return [dict(r) for r in rows]
        except Exception:
            pass
    p = _mapping_file()
    if not p.exists(): return []
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        if isinstance(data, dict): return data.get("mappings", []) or []
        return data if isinstance(data, list) else []
    except Exception:
        return []

@with_conn
def get_mapping_version(conn) -> str:
    if conn:
        try:
            r = conn.execute("SELECT value FROM MetaKV WHERE key='mapping_version' LIMIT 1").fetchone()
            if r and r[0]: return str(r[0])
        except Exception:
            pass
    p = _mapping_file()
    if not p.exists(): return "v0"
    ts = int(p.stat().st_mtime)
    return f"file-{ts}"

def write_mapping_json(mappings: List[Dict]):
    p = _mapping_file()
    p.write_text(json.dumps(mappings, ensure_ascii=False, indent=2), encoding="utf-8")

def upsert_mappings(new_rows: List[Dict]) -> Dict:
    base = get_mappings(None)
    index_by_order = {str(x.get("order_id","")): i for i,x in enumerate(base) if x.get("order_id")}
    index_by_track = {str(x.get("tracking_no","")): i for i,x in enumerate(base) if x.get("tracking_no")}
    inserted = updated = 0
    for r in new_rows:
        r = {k:v for k,v in r.items() if v not in (None,"")}
        r.setdefault("updated_at", time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
        key_o = str(r.get("order_id","")); key_t = str(r.get("tracking_no",""))
        idx = None
        if key_o and key_o in index_by_order: idx = index_by_order[key_o]
        elif key_t and key_t in index_by_track: idx = index_by_track[key_t]
        if idx is None:
            base.append(r); inserted += 1
            if key_o: index_by_order[key_o] = len(base)-1
            if key_t: index_by_track[key_t] = len(base)-1
        else:
            base[idx].update(r); updated += 1
    write_mapping_json(base)
    return {"inserted": inserted, "updated": updated, "total": len(base)}

@with_conn
def find_by_order_or_customer(conn, code: str) -> Optional[Dict]:
    if conn:
        try:
            row = conn.execute("""
                SELECT om.order_id, om.tracking_no, om.customer_order, om.updated_at
                  FROM OrderMapping om
                 WHERE om.order_id = ? OR om.customer_order = ?
                 LIMIT 1
            """, (code, code)).fetchone()
            if row: return dict(row)
        except Exception:
            pass
    for r in get_mappings(None):
        if code in (str(r.get("order_id","")), str(r.get("customer_order",""))):
            return r
    return None

@with_conn
def mark_printed(conn, tracking_no: str) -> bool:
    if not tracking_no: return False
    if conn:
        try:
            conn.execute("UPDATE OrderMapping SET printed_at = CURRENT_TIMESTAMP WHERE tracking_no = ?", (tracking_no,))
            conn.commit(); return True
        except Exception:
            pass
    arr = get_mappings(None); changed=False
    for x in arr:
        if str(x.get("tracking_no","")) == str(tracking_no):
            x["printed_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()); changed=True
            break
    if changed: write_mapping_json(arr)
    return True

