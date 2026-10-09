# Hobby Inventory

This directory is the source of truth for the physical model-kit and paint collection.

## Current inventory

- [`kits.csv`](kits.csv) — canonical structured model-kit list.
- [`kits.md`](kits.md) — readable, category-grouped model-kit list.
- [`paints.csv`](paints.csv) — canonical structured on-hand paint/finish list.
- [`paints.md`](paints.md) — readable paint list grouped by brand and product line.
- [`sources/`](sources/) — original source snapshots used for reconciliation.

As of **2026-10-09**:

- **38 model-kit catalog entries / 48 physical kits or boxed sets**
- **429 unique on-hand paint/finish entries / 480 total containers**
- **Kaleido Mecha Colors Set B (K125–K148)** is included.
- **Vallejo VJP77271 True Metallic Metal Complete Brush Collection** is tracked as ordered/inbound and is not included in on-hand paint totals yet.

## Designed to grow

The inventory is intentionally split by asset type so additional collections do not have to be mixed into the paint or kit files:

- [`tools/`](tools/) — reserved for airbrushes, cutters, sanding tools, clamps, electronics tools, etc.
- [`supplies/`](supplies/) — reserved for glue, putty, masking products, thinner, cleaner, tape, wire, LEDs, decals, and other consumables/accessories.

## Data rules

1. `*.csv` files are the canonical structured records.
2. `*.md` files are human-readable views and should be updated with the CSV.
3. Quantities represent physical containers or boxed kits. Multi-ship model sets remain one boxed kit with the contents described in notes.
4. Ordered items should be marked as inbound and not added to on-hand totals until received.
5. Unknown details stay blank or `TBD`; do not guess.
6. Preserve source snapshots when importing from another inventory system.

## Source reconciliation

The starting paint data came from PaintRack export `paintRack_export_2026-09-15_23-19-00.csv`. PaintRack under-reported the Kaleido collection and did not include the Polytranspar iridescents, so those were added manually. The later Vallejo 71.155 set and Kaleido Mecha Colors Set B were also reconciled into the canonical inventory.
