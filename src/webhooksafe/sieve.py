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

    ) -> None:
        self.store = store
        self.provider = provider
        self.event_id_extractor = event_id_extractor
        self.signature_verifier = signature_verifier
        self.ttl_seconds = int(ttl_seconds)
        self.accept_retries_after_failure = bool(accept_retries_after_failure)

    def precheck(self, raw_body: bytes, headers: dict) -> Verdict:
        """
        Call this early in your webhook route.
        If accept=False, you should short-circuit the handler (duplicate/invalid).
        """
        # Signature check
        if self.signature_verifier is not None:
            ok = False
            try:
                ok = bool(self.signature_verifier(raw_body, headers))
            except Exception:
                ok = False
            if not ok:
                # event_id might not be trustworthy; still try to extract for traceability
                eid = self._safe_extract_id(raw_body, headers) or "unknown"
                receipt = self.store.upsert_receive(self.provider, eid, self.ttl_seconds)
                self.store.mark_failed(self.provider, eid, "signature_verification_failed")
                return Verdict(False, "invalid_signature", receipt)

        event_id = self._safe_extract_id(raw_body, headers)
        if not event_id:
            receipt = self.store.upsert_receive(self.provider, "unknown", self.ttl_seconds)
            self.store.mark_failed(self.provider, "unknown", "missing_event_id")
            return Verdict(False, "missing_event_id", receipt)

        receipt = self.store.upsert_receive(self.provider, event_id, self.ttl_seconds)

        if receipt.seen_count > 1:
            if self.accept_retries_after_failure and receipt.status == "failed":
                return Verdict(True, "duplicate_retry_after_failure", receipt)
            return Verdict(False, "duplicate", receipt)

        return Verdict(True, "new", receipt)

    def mark_processed(self, event_id: str) -> None:
        self.store.mark_processed(self.provider, event_id)

    def mark_failed(self, event_id: str, error: str) -> None:
        self.store.mark_failed(self.provider, event_id, error)

    def _safe_extract_id(self, raw_body: bytes, headers: dict) -> str:
        try:
            eid = self.event_id_extractor(raw_body, headers)
            return (eid or "").strip()
        except Exception:
            return ""
