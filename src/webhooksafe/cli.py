from __future__ import annotations
import argparse
from datetime import datetime

from .store import SQLiteReceiptStore


def main() -> None:
    ap = argparse.ArgumentParser(
        prog="webhooksieve",
        description="Inspect and maintain webhook idempotency receipts stored in SQLite.",
    )
    ap.add_argument("--db", default="webhooksieve.db", help="Path to SQLite db (default: webhooksieve.db)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_list = sub.add_parser("list", help="List recent receipts")
    p_list.add_argument("--limit", type=int, default=50)



    p_get = sub.add_parser("get", help="Get one receipt")
    p_get.add_argument("provider")
    p_get.add_argument("event_id")

    p_prune = sub.add_parser("prune", help="Prune expired receipts")

    args = ap.parse_args()
    store = SQLiteReceiptStore(args.db)

    if args.cmd == "list":
        items = store.list_recent(limit=args.limit)
        for r in items:
            print(
                f"{r.last_seen_at.isoformat()}  {r.provider}:{r.event_id}  "
                f"seen={r.seen_count}  status={r.status}"
            )



