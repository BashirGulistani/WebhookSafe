from __future__ import annotations
import sqlite3
from datetime import datetime, timedelta, timezone
from typing import Optional, Iterable

from .models import Receipt


def utcnow() -> datetime:
    return datetime.now(timezone.utc)



class SQLiteReceiptStore:

    def __init__(self, db_path: str = "webhooksieve.db") -> None:
        self.db_path = db_path
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        return conn





