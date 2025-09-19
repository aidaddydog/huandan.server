import json, time, uuid
from app.core.config import JOBS_DIR

def _path(job_id: str):
    return JOBS_DIR / f"{job_id}.json"

def create_job(job_type: str, total: int = 0) -> str:
    job_id = uuid.uuid4().hex[:16]
    data = {"id":job_id,"type":job_type,"status":"running","total":total,"done":0,"message":"开始","started_at":time.time(),"updated_at":time.time()}
    _path(job_id).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return job_id

def update_job(job_id: str, done: int = None, message: str = None):
    p = _path(job_id)
    if not p.exists(): return
    data = json.loads(p.read_text(encoding="utf-8"))
    if done is not None: data["done"] = done
    if message is not None: data["message"] = message
    data["updated_at"] = time.time()
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def finish_job(job_id: str, message: str = "完成"):
    p = _path(job_id)
    if not p.exists(): return
    data = json.loads(p.read_text(encoding="utf-8"))
    data["status"] = "done"
    data["message"] = message
    data["updated_at"] = time.time()
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def error_job(job_id: str, message: str):
    data = {"id":job_id,"status":"error","message":message,"updated_at":time.time()}
    _path(job_id).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def get_job(job_id: str):
    p = _path(job_id)
    if not p.exists(): return {"error":"not found"}
    return json.loads(p.read_text(encoding="utf-8"))

