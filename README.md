# CardChase Data Room

Diligence materials for CardChase. Each folder is one topic, with an investor-facing
note, the underlying data, and a self-contained script to reproduce the data from a raw
snapshot.

## Contents

### [pricing-validation/](pricing-validation/)

Do the Near Mint card prices CardChase derives from eBay sold listings reflect the real
market? Benchmarked against TCGplayer's published Near Mint market price.

- [`pricing-validation-investor.md`](pricing-validation/pricing-validation-investor.md)
  answers the two questions: are the prices accurate, and do they track movement.
- [`pricing_comparison_sample.csv`](pricing-validation/pricing_comparison_sample.csv) is
  the full 3-day time series for 10 representative cards ($28 to $1,075), our price next
  to the market price.
- [`pricing_comparison_summary.csv`](pricing-validation/pricing_comparison_summary.csv)
  is one row per card for all 75 cards in the cohort.
- [`reproduce/`](pricing-validation/reproduce/) holds the raw snapshot and the script
  that builds the CSVs, so the numbers can be re-derived independently.

**Headline.** For cards worth $25 or more, our price tracks the TCGplayer market within
about 11% on the typical card, with no upward bias. It is an accurate level estimate. It
is not a short-horizon trend signal over the flat 12-week test window.
