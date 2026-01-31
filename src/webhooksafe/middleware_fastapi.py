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




