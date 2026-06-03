# eBay seller TAM — Pokémon TCG sold comps (filtered)

This note sizes the **seller side** of **Pokémon TCG** sold listings in our eBay comps
lake. Figures include only rows we treat as correctly matched Pokémon catalog cards.

**Headline (last 90 days, Mar–May 2026).** **~$32M** comps GMV, **~214k** transactions,
**~58k** unique sellers, **~2,900** distinct `pokemontcg_id`s (145 sets). At the
90-day pace, roughly **~$129M/yr** in **Pokémon TCG comps GMV** for cards we scrape —
not total eBay Pokémon, not other TCGs.

---

## Filter — what “Pokémon TCG focus” means

All figures below apply **all** of:

| Rule | Rationale |
|------|-----------|
| `match_confidence` ∈ **`agree`**, **`ambiguous_resolved`** | Same oracle gate as gold comps: title supports the catalog `pokemontcg_id`. Drops `disagree_*`, `ambiguous_unresolved`, and `junk` (~$22M / 96k rows excluded in 90d). |
| `pokemontcg_id` present | Row tied to the internal Pokémon TCG catalog. |
| `price_usd` > 0 | Priced sold comp. |
| `seller_name` present; exclude grader-token names (`psa`, `cgc`, …) | Real seller handles only; drops parse artifacts. |

**Scrape intent:** eBay category **183454** (Pokémon CCG individual cards) and
per-card keyword searches from the pokemontcg catalog. This is **Pokémon TCG only** by
design; the filter above removes mis-attributed listings that still landed in silver.

**Out of scope:** buyers (not on public sold pages), Magic/Yu-Gi-Oh/sports as primary
categories, cards never searched, and comps we cannot verify as the claimed Pokémon card.

**Data:** `s3://cardchase-scraper-dev/ebay_scraper/silver/silver_sales.parquet`
(`eu-north-1`). **As of:** 2026-06-03.

---

## Headline TAM (90 days)

Window: **2026-03-02 → 2026-05-31**.

| Metric | Value |
|--------|------:|
| **GMV (USD)** | **$31.9M** |
| **Transactions** | 213,760 |
| **Unique sellers** | 58,373 |
| **Average order value** | $149 |
| **Unique Pokémon cards (`pokemontcg_id`)** | 2,924 |
| **Unique sets** | 145 |

**Run-rate (90-day annualized):** ~**$129M/yr** (`× 365.25 / 90`).

**May 2026** (heaviest scrape month, same filter): **$24.3M** GMV, 175,746 txns,
50,665 sellers. May × 12 ≈ **$291M/yr** — upper bound while volume is still ramping.

**In-lake total (same filter, all sale dates):** $32.6M GMV — almost identical to 90d
because the scrape ramped in 2026; do not treat “all-time” as years of history.

---

## Addressable seller base (90-day GMV thresholds)

| Min 90d GMV per seller | Sellers | Share of 90d GMV |
|------------------------|--------:|------------------:|
| ≥ $500 | 9,540 | 84.2% |
| ≥ $1,000 | 4,829 | 73.8% |
| ≥ $5,000 | 601 | 47.6% |
| ≥ $10,000 | 204 | 39.1% |

**Read:** ~**4.8k** sellers with ≥$1k in verified Pokémon comps (90d); ~**204** with ≥
$10k.

---

## Market structure (90 days)

**Concentration**

| Top N sellers | % of GMV |
|---------------|----------:|
| 10 | 22.6% |
| 50 | 31.3% |
| 100 | 34.9% |
| 500 | 45.9% |

Seller HHI ≈ **380** (10k scale) — fragmented long tail.

**By eBay lifetime feedback (proxy tier)**

| Tier | Sellers | % of 90d GMV |
|------|--------:|-------------:|
| Small (100–1K) | 24,797 | 31.8% |
| Micro (<100) | 25,817 | 23.2% |
| Large (10K–100K) | 701 | 16.4% |
| Mid (1K–10K) | 7,007 | 16.4% |
| Power (100K+) | 51 | 12.2% |

**Grade mix (90d GMV):** PSA 10 dominates; graded slabs are the majority of dollar volume.

**Trust:** sellers with 100% positive feedback → **~48%** of 90d GMV.

---

## Top sellers (90d, Pokémon TCG filter)

| Seller | 90d GMV | Txns |
|--------|--------:|-----:|
| zandgemporium | $2.7M | 2,377 |
| probstein123 | $2.0M | 2,664 |
| dcsports87 | $828k | 3,894 |
| slapauction | $395k | 1,029 |
| ryans_cardhouse | $388k | 307 |

---

## TAM framing for CardChase

| Lens | Estimate | Meaning |
|------|----------|---------|
| **90d Pokémon comps GMV** | ~$32M | Verified Pokémon catalog matches only |
| **Run-rate** | ~$129M/yr | 90d pace annualized |
| **Addressable sellers (≥$1k / 90d)** | ~4,800 | Active in verified Pokémon comps |
| **Whale sellers (≥$10k / 90d)** | ~204 | High-volume segment |

This sizes **seller activity on Pokémon TCG sold comps we trust**, for ~3k catalog cards
we search — useful for data product and seller tooling TAM, not as total eBay Pokémon
GMV.

---

## Caveats

1. **Card coverage** — ~2,900 `pokemontcg_id`s searched to date, not every Pokémon card
   on eBay (current grade watchlist is 150 cards; historical searches widen coverage).
2. **Scrape ramp** — May 2026 dominates; use 90-day window for run-rate.
3. **Stricter alternative** — `agree` only (~$25M / 90d) if you want the tightest
   title↔card match; this note uses oracle (`agree` + `ambiguous_resolved`) to align with gold.
4. **Seller parse** — usernames from SRP `listing_attrs`; grader names excluded.
5. **Silver only** — gold drops seller columns.

---

## Reproduction

```bash
aws s3 cp s3://cardchase-scraper-dev/ebay_scraper/silver/silver_sales.parquet /tmp/silver_sales.parquet \
  --profile cardchase --region eu-north-1

uv run python - <<'PY'
from datetime import timedelta
import polars as pl

SUSPECT = {"psa", "cgc", "bgs", "ace", "tag", "gem", "mint", "nm", "lp"}
ORACLE = ["agree", "ambiguous_resolved"]

df = pl.read_parquet("/tmp/silver_sales.parquet")
poke = df.filter(
    pl.col("match_confidence").is_in(ORACLE)
    & pl.col("pokemontcg_id").is_not_null()
    & pl.col("seller_name").is_not_null()
    & (pl.col("price_usd") > 0)
    & ~pl.col("seller_name").is_in(list(SUSPECT))
)
cut = poke["sale_date"].max() - timedelta(days=90)
recent = poke.filter(pl.col("sale_date") >= cut)
print("Pokémon TCG 90d GMV", recent["price_usd"].sum())
print("sellers", recent["seller_name"].n_unique())
print("txns", recent.height)
PY
```

Pipeline context: `cardchase-lake-of-rage` → `docs/lakehouse-schema.md`.
