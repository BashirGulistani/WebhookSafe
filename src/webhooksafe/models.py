from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Optional



@dataclass(frozen=True)
class Receipt:
    provider: str
    event_id: str
    first_seen_at: datetime
    last_seen_at: datetime
    seen_count: int
    status: str  
    last_error: Optional[str]
    ttl_seconds: int
