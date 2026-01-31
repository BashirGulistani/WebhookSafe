import os
import tempfile
import unittest

from webhooksieve.store import SQLiteReceiptStore
from webhooksieve.sieve import WebhookSieve


def extract_id_from_json_body(raw: bytes, headers: dict) -> str:
    import json
    obj = json.loads(raw.decode("utf-8"))
    return str(obj.get("id", ""))







