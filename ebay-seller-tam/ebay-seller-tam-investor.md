# eBay seller TAM — aggregate metrics from sold comps

This note sizes the **seller side** of the Pokémon graded-card comps we capture from
eBay sold listings. It answers how much transaction volume and how many distinct sellers
appear in our lake, and how concentrated that activity is.

**Headline.** In the last 90 days of our watchlist scrape (Mar–May 2026), we observe
**~$54M** in sold comps GMV across **~74k** unique sellers and **~310k** transactions,
with a fragmented long tail and a meaningful whale tier (~370 sellers above $10k GMV
each in that window). Annualized at the recent 90-day pace, that is roughly **~$217M/yr**
in comps GMV **within our card universe** — not total eBay Pokémon.

---

## What this measures (and what it does not)

**In scope**

- **GMV:** sum of `price_usd` on sold comps in `silver_sales.parquet`.
- **Sellers:** public eBay usernames parsed from search-result attribute text
  (`seller_name`, plus feedback % and count).
- **Universe:** cards on the CardChase eBay watchlist (~2,987 `pokemontcg_id`s,
  145 sets) — a deliberate sample, not all of eBay TCG.

**Out of scope**

- **Buyers:** eBay does not expose buyer identity on public sold search; we do not
  track them.
- **Full eBay TAM:** extrapolating to all Pokémon on eBay would require a wider scrape
  or external market estimates.
- **Gold layer:** consumer `gold_ebay_sales` drops seller columns; this analysis uses
  **silver** only.

**Data source:** `s3://cardchase-scraper-dev/ebay_scraper/silver/silver_sales.parquet`
(region `eu-north-1`). **As of:** 2026-06-03 (342,482 rows; sale dates 2020-02-21 →
2026-05-31).

**Cleaning:** ~18% of raw GMV had `seller_name` matching grader tokens (`psa`, `cgc`,
etc.) from parse noise on titles. Figures below **exclude** those names. Top artifact
before cleaning: `psa` at ~$12M (22k rows) — not a real seller.

---

## Headline TAM (cleaned sellers, last 90 days)

Window: **2026-03-02 → 2026-05-31** (90 days ending latest sale in lake).

| Metric | Value |
|--------|------:|
| **GMV (USD)** | **$53.6M** |
| **Transactions** | 310,053 |
| **Unique sellers** | 73,630 |
| **Average order value** | $173 |
| **GMV per seller (mean)** | $728 |
| **Unique cards (pokemontcg_id)** | 2,987 |
| **Unique sets** | 145 |

**Run-rate (90-day pace annualized):** ~**$217M/yr** GMV (`× 365.25 / 90`).

**May 2026 alone** (heaviest scrape month): $39.6M GMV, 246,947 txns, 63,445 sellers.
May × 12 ≈ **$476M/yr** — an upper bound while scrape volume is still ramping; prefer
the 90-day figure for a steadier read.

**All-time in lake (cleaned):** $55.1M GMV, 319,600 txns, 74,671 sellers. Most history
predates the 2026 scrape ramp; all-time annualization is misleading.

---

## Addressable seller base (90-day GMV thresholds)

Sellers active at each cumulative GMV level in the 90-day window:

| Min 90d GMV per seller | Sellers | Share of 90d GMV |
|------------------------|--------:|------------------:|
| ≥ $100 | 35,990 | 97.5% |
| ≥ $500 | 13,727 | 87.7% |
| ≥ $1,000 | 7,266 | 79.2% |
| ≥ $5,000 | 1,008 | 55.7% |
| ≥ $10,000 | 369 | 47.5% |
| ≥ $50,000 | 55 | 37.3% |
| ≥ $100,000 | 28 | 33.8% |

**Read:** ~**7.3k** sellers did ≥$1k in watchlist comps in 90 days; ~**370** did ≥
$10k (a practical “pro” tier for this slice).

---

## Market structure

**Concentration (90d GMV, cleaned)**

| Top N sellers | % of GMV |
|---------------|----------:|
| 10 | 28.2% |
| 50 | 36.8% |
| 100 | 40.2% |
| 500 | 49.7% |
| 1,000 | 55.6% |

Seller HHI ≈ **431** (on a 10,000 scale) — **fragmented** long tail; not winner-take-all
in this sample.

**By eBay lifetime feedback (proxy tier, 90d GMV)**

| Tier | Sellers | % of 90d GMV |
|------|--------:|-------------:|
| Small (100–1K feedback) | 30,871 | 29.8% |
| Large (10K–100K) | 858 | 21.7% |
| Micro (<100) | 33,106 | 19.8% |
| Mid (1K–10K) | 8,735 | 16.8% |
| Power (100K+) | 60 | 11.8% |

**Grade mix (all-time GMV):** PSA 10 ≈ 40%; PSA 9 ≈ 12%; raw NM ≈ 5%.

**Trust:** sellers with 100% positive feedback → **46%** of all-time GMV.

**Oracle-quality comps** (`match_confidence` in `agree`, `ambiguous_resolved`):
**60%** of all-time GMV; **60%** of 90d GMV (~$32M of ~$54M).

---

## Top sellers (90d, cleaned)

| Seller | 90d GMV | Txns |
|--------|--------:|-----:|
| zandgemporium | $4.4M | 3,878 |
| probstein123 | $3.6M | 4,083 |
| mirmex | $3.0M | 327 |
| dcsports87 | $1.1M | 4,823 |
| slapauction | $812k | 1,933 |
| ryans_cardhouse | $559k | 443 |

*(Full tables available on request; single-transaction outliers like nathacostanz_0
are high-AOV one-offs.)*

---

## TAM framing for CardChase

| Lens | Estimate | Meaning |
|------|----------|---------|
| **Observed comps TAM** | ~$55M | Cumulative GMV in silver for watchlist cards |
| **Current run-rate** | ~$217M/yr | 90-day GMV annualized |
| **Aggressive run-rate** | ~$476M/yr | May 2026 × 12 (scrape still scaling) |
| **Addressable sellers (≥$1k / 90d)** | ~7,300 | Meaningful volume in our comp set |
| **Whale sellers (≥$10k / 90d)** | ~370 | High-touch segment |

These numbers size **comps GMV and seller activity in our scraped card universe**, useful
for data-product TAM, seller tooling, and marketplace adjacency — not as total eBay
Pokémon GMV without widening the watchlist or adding third-party market totals.

---

## Caveats

1. **Watchlist sample** — not exhaustive eBay TCG; expanding cards changes GMV and
   seller counts.
2. **Scrape ramp** — May 2026 dominates recent volume; use 90-day or forward months for
   run-rate, not full 2020–2026 span.
3. **Seller parse** — username extracted from SRP `listing_attrs` regex; grader-token
   false positives removed for this note; pipeline improvement would tighten totals.
4. **No seller user id** — only public handles; profile URLs derivable as
   `https://www.ebay.com/usr/{seller_name}` but not stored in silver today.
5. **Silver vs gold** — investor-facing comps in gold omit seller; this analysis is
   silver-only.

---

## Reproduction

From a machine with AWS profile `cardchase` and repo `cardchase-lake-of-rage`:

```bash
aws s3 cp s3://cardchase-scraper-dev/ebay_scraper/silver/silver_sales.parquet /tmp/silver_sales.parquet \
  --profile cardchase --region eu-north-1

uv run python - <<'PY'
# Aggregate script — exclude grader-token seller names; 90d window from max(sale_date).
import re
from datetime import timedelta
import polars as pl

SUSPECT = {"psa", "cgc", "bgs", "ace", "tag", "gem", "mint", "nm", "lp"}
df = pl.read_parquet("/tmp/silver_sales.parquet")
base = df.filter(
    pl.col("seller_name").is_not_null()
    & (pl.col("price_usd") > 0)
    & ~pl.col("seller_name").is_in(list(SUSPECT))
)
cut = base["sale_date"].max() - timedelta(days=90)
recent = base.filter(pl.col("sale_date") >= cut)
print("90d GMV", recent["price_usd"].sum())
print("sellers", recent["seller_name"].n_unique())
print("txns", recent.height)
PY
```

Schema and pipeline context: `cardchase-lake-of-rage` → `docs/lakehouse-schema.md`.
