# ShopStockSync

ShopStockSync is a small prototype project for inventory-sync workflows built around Etsy listing coordination and spreadsheet-based stock tracking.

## Current repository contents

- `index.html` — public landing page for the project
- `prototype/sync_preview.py` — simple CLI preview script for stock reconciliation
- `prototype/sample_inventory.csv` — sample dataset for local testing

## Prototype usage

```bash
python3 prototype/sync_preview.py \
  --csv prototype/sample_inventory.csv \
  --low-stock-threshold 5
```

## What the prototype does

- loads a local inventory CSV
- counts low-stock items
- reports active/inactive rows
- prints a dry-run style sync summary

## Notes

This repository is intentionally lightweight for early iteration and presentation.
