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
