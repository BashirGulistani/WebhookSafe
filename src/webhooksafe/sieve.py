from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Optional, Any

from .store import SQLiteReceiptStore
from .models import Receipt


@dataclass(frozen=True)
class Verdict:
    accept: bool
    reason: str
    receipt: Receipt


SignatureVerifier = Callable[[bytes, dict], bool]
EventIdExtractor = Callable[[bytes, dict], str]







