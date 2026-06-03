# CardChase Data Room

Diligence materials for CardChase. Each folder is one topic, with an investor-facing note
and, where relevant, the underlying data and a self-contained script to reproduce it from a
raw snapshot.

## Contents

### [pricing-validation/](pricing-validation/)

Do the Near Mint card prices CardChase derives from eBay sold listings reflect the real
market? Benchmarked against TCGplayer's published Near Mint market price.

- [`pricing-validation-investor.md`](pricing-validation/pricing-validation-investor.md) is
  the note. How close our price is to the market, for cards worth $25 or more.
- [`pricing_comparison_sample.csv`](pricing-validation/pricing_comparison_sample.csv) is
  the full 3-day time series for 10 representative cards ($28 to $1,075), our price next to
  the market price.
- [`pricing_comparison_summary.csv`](pricing-validation/pricing_comparison_summary.csv) is
  one row per card for all 75 cards in the cohort.
- [`reproduce/`](pricing-validation/reproduce/) holds the raw snapshot and the script that
  builds the CSVs, so the numbers can be re-derived independently.

**Headline.** For cards worth $25 or more, our price tracks the TCGplayer market within
about 11% on the typical card, with no upward bias.

### [data-quality/](data-quality/)

How raw eBay sold listings become trustworthy prices. The filtering funnel that decides
which sales count and which are thrown out.

- [`data-quality-investor.md`](data-quality/data-quality-investor.md) walks the five
  filters, from discarding bot-blocked pages to flagging a lone inflated sale.

**Headline.** Every raw sale passes five filters before it can move a price. Roughly a
third are dropped at the identity check alone, where a listing's title must independently
resolve to the exact card it claims to be.

### [ebay-seller-tam/](ebay-seller-tam/)

Seller-side TAM for **Pokémon TCG** sold comps (oracle-matched catalog cards).

- [`ebay-seller-tam-investor.md`](ebay-seller-tam/ebay-seller-tam-investor.md) — 90-day
  GMV, seller counts, concentration (as of 2026-06-03).

**Headline.** Mar–May 2026: **~$32M** Pokémon TCG comps GMV, **~58k** sellers,
**~214k** transactions (~2.9k catalog cards).
