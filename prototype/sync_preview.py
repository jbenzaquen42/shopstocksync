#!/usr/bin/env python3
"""Simple stock reconciliation preview for ShopStockSync."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Preview inventory reconciliation from a local CSV file."
    )
    parser.add_argument(
        "--csv",
        required=True,
        dest="csv_path",
        help="Path to inventory CSV with sku,title,quantity,status columns.",
    )
    parser.add_argument(
        "--low-stock-threshold",
        type=int,
        default=5,
        help="Threshold for flagging low-stock items (default: 5).",
    )
    return parser.parse_args()


def load_rows(csv_path: Path) -> list[dict[str, str]]:
    with csv_path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def normalize_quantity(row: dict[str, str]) -> int:
    raw = (row.get("quantity") or "0").strip()
    try:
        return int(raw)
    except ValueError:
        return 0


def main() -> int:
    args = parse_args()
    csv_path = Path(args.csv_path)

    if not csv_path.exists():
        raise SystemExit(f"CSV not found: {csv_path}")

    rows = load_rows(csv_path)
    low_stock = []
    active = 0
    inactive = 0

    for row in rows:
        quantity = normalize_quantity(row)
        status = (row.get("status") or "active").strip().lower()
        if status == "active":
            active += 1
        else:
            inactive += 1

        if status == "active" and quantity <= args.low_stock_threshold:
            low_stock.append(
                {
                    "sku": row.get("sku", "").strip(),
                    "title": row.get("title", "").strip(),
                    "quantity": quantity,
                }
            )

    print("ShopStockSync Preview")
    print("=" * 21)
    print(f"CSV rows loaded: {len(rows)}")
    print(f"Active listings: {active}")
    print(f"Inactive listings: {inactive}")
    print(f"Low-stock threshold: {args.low_stock_threshold}")
    print(f"Low-stock items: {len(low_stock)}")

    if low_stock:
        print("\nLow-stock candidates:")
        for item in low_stock:
            print(
                f"- {item['sku']}: {item['title']} (quantity={item['quantity']})"
            )
    else:
        print("\nNo low-stock candidates found.")

    print("\nNext step: map these rows to listing IDs and generate a dry-run sync plan.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
