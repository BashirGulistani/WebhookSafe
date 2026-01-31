from __future__ import annotations
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from .sieve import WebhookSieve





class WebhookSieveMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, sieve: WebhookSieve, *, duplicate_status_code: int = 200):
        super().__init__(app)
        self.sieve = sieve
        self.duplicate_status_code = duplicate_status_code



    async def dispatch(self, request: Request, call_next):
        raw = await request.body()
        headers = dict(request.headers)

        verdict = self.sieve.precheck(raw, headers)
        if not verdict.accept:
            return JSONResponse(
                status_code=self.duplicate_status_code,
                content={
                    "ok": True,
                    "skipped": True,
                    "reason": verdict.reason,
                    "provider": verdict.receipt.provider,
                    "event_id": verdict.receipt.event_id,
                    "seen_count": verdict.receipt.seen_count,
                    "status": verdict.receipt.status,
                },
            )

        async def receive():
            return {"type": "http.request", "body": raw, "more_body": False}

        request._receive = receive 
        response = await call_next(request)
        return response
