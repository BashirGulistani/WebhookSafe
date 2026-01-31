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





