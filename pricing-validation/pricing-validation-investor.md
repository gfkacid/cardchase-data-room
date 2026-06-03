# Are the card prices accurate? A market check against TCGplayer

This note answers the core question an investor would ask about the Near Mint card
prices we derive from eBay sold listings. How close are they to the broader market?

The benchmark is TCGplayer's published Near Mint market price. TCGplayer is the
largest US trading-card marketplace, and its market price is the reference number
most collectors and dealers quote. It is an estimate, not absolute truth, but it
is the best independent yardstick available.

The accompanying `pricing_comparison_sample.csv` and `pricing_comparison_summary.csv`
hold the underlying numbers, so the comparison can be opened and checked directly
in a spreadsheet.

---

## What was compared

We took every Near Mint card whose TCGplayer market value is $25 or more, and for
each one we lined up two price series over the same period:

- **Our price.** The median eBay sold price of Near Mint copies, in rolling 3-day
  windows.
- **The market.** TCGplayer's Near Mint market price for the same 3-day windows.

That gives a like-for-like comparison per card, window by window.

- **75 cards**, market value $25 to about $1,075.
- **942 three-day comparison windows.**
- About **12 weeks**, early March to end of May 2026.

The $25 cutoff matters. Below it the gap to the market widens sharply, driven by
fixed per-sale costs like shipping and fees that weigh more on a cheap card, and by
thinner, noisier markets at low value. At $25 and up those effects fade and the two
series line up. The cutoff is set on this observed pattern.

---

## Are the prices accurate? Yes.

For cards worth $25 or more, our eBay-derived Near Mint price tracks the TCGplayer
market closely, with no systematic markup.

- The typical card sits within **11%** of the market price (median gap 11.1%).
- **57 of 75 cards** (76%) are within 15%. **64 of 75** (85%) are within 20%.
- There is **no upward bias.** Our price runs slightly *below* the market on the
  typical card (median ratio 0.97x), and is above the market in only 39% of windows.
  Any worry that realised eBay sales would systematically overstate value does not
  hold at this price level.

In plain terms, for a $25+ card, our number lands within roughly a tenth of what the
largest marketplace says it is worth, and it does not lean high.

---

## Files in this folder

- `pricing-validation-investor.md` — this note.
- `pricing_comparison_sample.csv` — the full 3-day time series for 10 representative
  cards spanning $28 to $1,075. One row per card per window. Open this to see the two
  series side by side.
- `pricing_comparison_summary.csv` — one row per card for all 75, with each card's
  median eBay price, median market price, typical gap, and price ratio.
- `build_investor_dataset.py` — the script that produced the two CSVs from the
  validation snapshot. No scraping or network access.

Columns in `pricing_comparison_sample.csv`:

| Column | Meaning |
|--------|---------|
| `card` | card name |
| `card_id` | stable card identifier |
| `date` | start of the 3-day comparison window |
| `ebay_sold_nm_usd` | median eBay sold price of Near Mint copies in that window |
| `tcgplayer_nm_usd` | TCGplayer Near Mint market price for that window |
| `diff_pct` | percent difference, our price vs the market |
| `ebay_sales_count` | number of eBay sales behind our price that window |
