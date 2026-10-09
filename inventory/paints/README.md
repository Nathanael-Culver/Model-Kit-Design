# Paint & Finish Inventory

**Last updated:** 2026-10-09

This directory contains the on-hand paint/finish inventory, kept separate from model kits, tools, and consumable supplies. The structured CSV files are the canonical records; each row includes brand, SKU, name, product line, size, quantity, status, source, and functional category.

## Totals

- **429 unique on-hand paint/finish entries**
- **480 total containers**

## Files

- [`vallejo-model-air.csv`](vallejo-model-air.csv) — Vallejo Model Air
- [`vallejo-other-lines.csv`](vallejo-other-lines.csv) — all other Vallejo paint/finish lines
- [`kaleido.csv`](kaleido.csv) — Kaleido ColorWorks / Gaahleri
- [`tamiya.csv`](tamiya.csv) — Tamiya
- [`alclad-ii.csv`](alclad-ii.csv) — Alclad II
- [`polytranspar.csv`](polytranspar.csv) — Polytranspar iridescents

## Brand / line breakdown

### Vallejo — 241 entries / 281 containers

Model Air; Model Color; Mecha Color; Metal Color; Surface Primer; Model Wash; Premium Airbrush Color; The Shifters; Game Color; Game Air; Fantasy-Pro; Xpress Color; and a small group of varnishes not identified by PaintRack as a specific line.

The Vallejo 71.155 US Navy & USMC Colors 70s–Present set has been reconciled into the quantities. Its 70.615 Light Ghost Gray primer was added as a new entry and the seven overlapping Model Air colors had their quantities increased by one.

### Kaleido ColorWorks / Gaahleri — 135 entries / 135 containers

- Auto Colors A — 24
- Auto Colors B — 24
- Mecha Colors A — 24
- **Mecha Colors B — 24 (K125–K148; added 2026-10-09)**
- Metal Colors — 12
- Primary Colors — 8
- Translucent Colors — 12
- Primers — 4
- Varnishes — 3

The Mecha Colors B box shown on 2026-10-09 is recorded as individual paints K125 through K148 rather than only as a boxed set.

### Tamiya — 38 entries / 46 containers

Acrylic Flat; Acrylic Gloss; Fine Surface Primer L; Lacquer Paint; PS Spray; and TS Spray.

### Alclad II — 11 entries / 14 containers

Metallic/specialty finishes plus primer and clear.

### Polytranspar — 4 entries / 4 containers

WA440 Shimmering Blue, WA441 Shimmering Green, WA442 Shimmering Gold, and WA443 Shimmering Red.

## Ordered / inbound

**Vallejo VJP77271 True Metallic Metal Complete Brush Collection** is tracked as ordered/inbound and is intentionally **not** included in the on-hand totals yet. It should be expanded into individual colors after physical receipt.

## Scope rule

Thinners, reducers, cleaners, putties, liquid mask, flow improvers, cement, and similar non-paint products are excluded here. They belong in `../supplies/` when that inventory is populated.
