from __future__ import annotations
import sqlite3
from datetime import datetime, timedelta, timezone
from typing import Optional, Iterable

from .models import Receipt


def utcnow() -> datetime:
    return datetime.now(timezone.utc)



