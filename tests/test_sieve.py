import os
import tempfile
import unittest

from webhooksieve.store import SQLiteReceiptStore
from webhooksieve.sieve import WebhookSieve


def extract_id_from_json_body(raw: bytes, headers: dict) -> str:
    import json
    obj = json.loads(raw.decode("utf-8"))
    return str(obj.get("id", ""))





def always_ok_sig(raw: bytes, headers: dict) -> bool:
    return True


class TestSieve(unittest.TestCase):
    def test_dedup(self):
        with tempfile.TemporaryDirectory() as d:
            db = os.path.join(d, "t.db")
            store = SQLiteReceiptStore(db)

            sieve = WebhookSieve(
                store=store,
                provider="test",
                event_id_extractor=extract_id_from_json_body,
                signature_verifier=always_ok_sig,
                ttl_seconds=60,
            )

            body = b'{"id":"evt_123","x":1}'
            v1 = sieve.precheck(body, {})
            self.assertTrue(v1.accept)
            self.assertEqual(v1.reason, "new")

            v2 = sieve.precheck(body, {})
            self.assertFalse(v2.accept)
            self.assertEqual(v2.reason, "duplicate")
            sieve.mark_failed("evt_123", "boom")
            v3 = sieve.precheck(body, {})
            self.assertTrue(v3.accept)
            self.assertEqual(v3.reason, "duplicate_retry_after_failure")


if __name__ == "__main__":
    unittest.main()

