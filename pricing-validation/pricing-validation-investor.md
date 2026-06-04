# Pricing accuracy

We price Near Mint cards from eBay sold listings. The independent benchmark is TCGplayer's published Near Mint market price — the reference number most collectors and dealers quote.

---

## Example: Pikachu ex 276

Pikachu ex 276 is the highest-value card in our catalog at roughly $1,300 Near Mint. We tracked it over 26 days (May 2–27 2026) combining three sources: eBay sold data, CardChase production sales, and TCGPlayer's Near Mint price. All sources filtered to Near Mint only; eBay records deduplicated across sources.

**486 Near Mint sales over 26 days.** That is 18.7 per day on average. All but one day in the window exceeded 10 sales.

| Metric | Value |
|--------|-------|
| eBay median NM | $1,299.50 |
| TCGPlayer NM median | $1,108.22 |
| Median gap | 8.6% |
| eBay / TCGPlayer ratio | 1.17x |

The 8.6% gap reflects rapid price appreciation over the period — the card rose from roughly $530 in early March to $1,300 by late May. eBay realised prices lead TCGPlayer's published market price during sharp moves.

The full daily breakdown is in `pikachu276_nm_daily.csv`.

---

## Files

- `pikachu276_nm_daily.csv` — 26-day daily Near Mint breakdown for Pikachu ex 276. Columns: date, eBay NM sale count, eBay median and average price, TCGPlayer NM price and daily quantity, and CardChase fair market value (`cc_fmv_usd` — our production system's published price for the card that day).
