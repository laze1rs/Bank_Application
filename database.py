import sqlite3
import os
from pathlib import Path
from typing import Any, Optional, Tuple
import config

DB_PATH = config.DB_PATH

def init_db() -> None:
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT, balance REAL, transactions TEXT)"
        )
        conn.commit()
    # Попытаться установить права файла (только на unix-подобных)
    try:
        if os.name != "nt":
            os.chmod(DB_PATH, config.DB_FILE_MODE)
    except Exception:
        pass

def _normalize_params(params: Optional[Any]) -> Tuple:
    if params is None:
        return ()
    if isinstance(params, (list, tuple)):
        return tuple(params)
    return (params,)

def sql_command(command: str, params: Optional[Any] = None, fetch: bool = False, retries: int = 1):
    params = _normalize_params(params)
    last_exc = None
    for _ in range(retries + 1):
        try:
            with sqlite3.connect(DB_PATH, timeout=5) as conn:
                cur = conn.cursor()
                cur.execute(command, params)
                result = cur.fetchall() if fetch else None
                conn.commit()
                return result
        except (sqlite3.OperationalError, sqlite3.ProgrammingError) as e:
            last_exc = e
            continue
    raise last_exc

init_db()