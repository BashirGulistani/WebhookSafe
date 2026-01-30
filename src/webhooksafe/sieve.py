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





class WebhookSieve:
    """
    Core engine:
    - verify signature (optional)
    - extract event_id
    - write/lookup receipt
    - decide accept/duplicate
    """

    def __init__(
        self,
        *,
        store: SQLiteReceiptStore,
        provider: str,
        event_id_extractor: EventIdExtractor,
        signature_verifier: Optional[SignatureVerifier] = None,
        ttl_seconds: int = 7 * 24 * 3600,
        accept_retries_after_failure: bool = True,


