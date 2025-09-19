import sqlite3
from pathlib import Path
from typing import Callable, Any
from app.core.config import DB_PATH
def with_conn(func: Callable[..., Any]):
    def wrapper(*args, **kwargs):
        if not Path(DB_PATH).exists():
            return func(None, *args, **kwargs)
        conn = sqlite3.connect(DB_PATH)
        try:
            conn.row_factory = sqlite3.Row
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

