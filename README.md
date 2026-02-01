# WebhookSieve

WebhookSieve is a tiny “seatbelt” for webhook consumers.

If you’ve run webhooks in production, you’ve seen this:
- providers retry (sometimes aggressively)
- your handler isn’t perfectly idempotent
- duplicates slip through and you create double orders / double DB rows / double emails

WebhookSieve gives you idempotency without needing Redis or a full event bus.
It stores “receipts” in SQLite and makes a simple decision for each incoming webhook:
**new** → process it  
**duplicate** → skip it (and return 2xx so the sender stops retrying)

It also tracks status (processed / failed), counts duplicates, and exposes a small CLI to inspect what happened.

---

## Install

```bash
pip install -e .




from fastapi import FastAPI, Request
from webhooksieve import WebhookSieve, SQLiteReceiptStore
from webhooksieve.middleware_fastapi import WebhookSieveMiddleware

def extract_event_id(raw: bytes, headers: dict) -> str:
    import json
    obj = json.loads(raw.decode("utf-8"))
    return str(obj.get("id", ""))

store = SQLiteReceiptStore("webhooksieve.db")
sieve = WebhookSieve(
    store=store,
    provider="stripe",
    event_id_extractor=extract_event_id,
    signature_verifier=None,   # plug yours in
    ttl_seconds=7*24*3600,
)

app = FastAPI()
app.add_middleware(WebhookSieveMiddleware, sieve=sieve, duplicate_status_code=200)

@app.post("/webhooks/stripe")
async def stripe_webhook(request: Request):
    payload = await request.json()

    # do your work...
    # if success:
    sieve.mark_processed(payload["id"])
    return {"ok": True}
