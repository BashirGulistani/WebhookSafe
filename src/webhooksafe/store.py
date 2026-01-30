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

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS receipts (
                  provider TEXT NOT NULL,
                  event_id TEXT NOT NULL,
                  first_seen_at TEXT NOT NULL,
                  last_seen_at TEXT NOT NULL,
                  seen_count INTEGER NOT NULL,
                  status TEXT NOT NULL,
                  last_error TEXT,
                  ttl_seconds INTEGER NOT NULL,
                  PRIMARY KEY (provider, event_id)
                )
                """
            )
            conn.execute("CREATE INDEX IF NOT EXISTS idx_receipts_last_seen ON receipts(last_seen_at)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_receipts_status ON receipts(status)")
            conn.commit()

    def _row_to_receipt(self, row) -> Receipt:
        return Receipt(
            provider=row[0],
            event_id=row[1],
            first_seen_at=datetime.fromisoformat(row[2]),
            last_seen_at=datetime.fromisoformat(row[3]),
            seen_count=int(row[4]),
            status=row[5],
            last_error=row[6],
            ttl_seconds=int(row[7]),
        )





