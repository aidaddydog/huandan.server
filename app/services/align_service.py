import os
from typing import Dict, List, Set
from app.repositories.mapping_repo import get_mappings, write_mapping_json
from app.repositories.file_repo import list_pdfs
from app.core.config import PDF_DIR

def scan_alignment() -> Dict:
    maps = get_mappings(None)
    map_set: Set[str] = set([str(x.get("tracking_no","")).strip() for x in maps if x.get("tracking_no")])
    pdfs = list_pdfs()
    file_set: Set[str] = set([os.path.splitext(os.path.basename(p))[0] for p in pdfs])
    missing_file = sorted(list(map_set - file_set))         # 有映射却没有文件
    orphan_file = sorted(list(file_set - map_set))          # 有文件却没有映射
    return {
        "mapping_total": len(maps),
        "pdf_total": len(pdfs),
        "missing_file": missing_file,
        "orphan_file": orphan_file
    }

def fix_alignment(add_mapping_from_orphan: bool = True) -> Dict:
    report = scan_alignment()
    if add_mapping_from_orphan and report["orphan_file"]:
        maps = get_mappings(None)
        exist_tracks = set([str(x.get("tracking_no","")) for x in maps])
        for t in report["orphan_file"]:
            if t and t not in exist_tracks:
                maps.append({"order_id":"", "tracking_no": t})
        write_mapping_json(maps)
        report["added_mappings"] = len(report["orphan_file"])
    return report

