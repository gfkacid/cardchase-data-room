# eBay seller TAM — Pokémon TCG sold comps

Matched to our card catalog.

**Headline (last 90 days, Mar–May 2026).** **~$32M** comps GMV, **~214k** transactions,
**~58k** unique sellers, **~2,900** catalog cards across **145** sets. At the 90-day
pace, roughly **~$129M/yr** in Pokémon TCG comps GMV for the cards we actively scrape.

**Data:** `s3://cardchase-scraper-dev/ebay_scraper/silver/silver_sales.parquet`
(`eu-north-1`). **As of:** 2026-06-03. **Window:** 2026-03-02 → 2026-05-31.

**Population:** Rows with `match_confidence` in `agree` or `ambiguous_resolved`, a
catalog `pokemontcg_id`, `price_usd` > 0, and a parsed eBay `seller_name`. Scrapes use
eBay category **183454** (Pokémon CCG individual cards) and per-card catalog search
queries.

---

## Headline metrics (90 days)

| Metric | Value |
|--------|------:|
| **GMV (USD)** | **$31.9M** |
| **Transactions** | 213,760 |
| **Unique sellers** | 58,373 |
| **Average order value** | $149 |
| **Unique cards (`pokemontcg_id`)** | 2,924 |
| **Unique sets** | 145 |

**Run-rate (90-day annualized):** ~**$129M/yr** (`× 365.25 / 90`).

**May 2026** (peak scrape month): **$24.3M** GMV, 175,746 txns, 50,665 sellers.

---

## Addressable seller base (90-day GMV thresholds)

| Min 90d GMV per seller | Sellers | Share of GMV |
|------------------------|--------:|-------------:|
| ≥ $500 | 9,540 | 84.2% |
| ≥ $1,000 | 4,829 | 73.8% |
| ≥ $5,000 | 601 | 47.6% |
| ≥ $10,000 | 204 | 39.1% |

~**4.8k** sellers with ≥$1k GMV in the period; ~**204** with ≥$10k.

---

## Market structure (90 days)

**Concentration**

| Top N sellers | % of GMV |
|---------------|----------:|
| 10 | 22.6% |
| 50 | 31.3% |
| 100 | 34.9% |
| 500 | 45.9% |

Seller HHI ≈ **380** (10,000 scale) — fragmented long tail.

**By eBay lifetime feedback**

| Tier | Sellers | % of GMV |
|------|--------:|---------:|
| Small (100–1K) | 24,797 | 31.8% |
| Micro (<100) | 25,817 | 23.2% |
| Large (10K–100K) | 701 | 16.4% |
| Mid (1K–10K) | 7,007 | 16.4% |
| Power (100K+) | 51 | 12.2% |

**Grade mix (90d GMV):** PSA 10 ~$10.4M (32%); PSA 9 ~$4.0M (13%); raw NM ~$2.3M (7%);
PSA 8 ~$2.0M (6%).

**Trust:** sellers with 100% positive feedback account for **~48%** of GMV.

---

## Top sellers (90 days)

| Seller | GMV | Txns |
|--------|----:|-----:|
| zandgemporium | $2.7M | 2,377 |
| probstein123 | $2.0M | 2,664 |
| dcsports87 | $828k | 3,894 |
| slapauction | $395k | 1,029 |
| ryans_cardhouse | $388k | 307 |

---

## TAM framing for CardChase

| Lens | Estimate |
|------|----------|
| **90d Pokémon comps GMV** | ~$32M |
| **Run-rate** | ~$129M/yr |
| **Addressable sellers (≥$1k / 90d)** | ~4,800 |
| **Whale sellers (≥$10k / 90d)** | ~204 |

---

## Caveats

1. **Card coverage** — metrics cover ~2,900 catalog cards we search, not the full Pokémon
   print catalog.
2. **Scrape ramp** — May 2026 carries most volume; 90-day window is the right run-rate
   basis.
3. **Seller field** — public eBay username from listing attributes; no buyer identity.

---

## Reproduction

```bash
aws s3 cp s3://cardchase-scraper-dev/ebay_scraper/silver/silver_sales.parquet /tmp/silver_sales.parquet \
  --profile cardchase --region eu-north-1

uv run python - <<'PY'
from datetime import timedelta
import polars as pl

ORACLE = ["agree", "ambiguous_resolved"]
INVALID_SELLER = {"psa", "cgc", "bgs", "ace", "tag", "gem", "mint", "nm", "lp"}

df = pl.read_parquet("/tmp/silver_sales.parquet")
poke = df.filter(
    pl.col("match_confidence").is_in(ORACLE)
    & pl.col("pokemontcg_id").is_not_null()
    & pl.col("seller_name").is_not_null()
    & (pl.col("price_usd") > 0)
    & ~pl.col("seller_name").is_in(list(INVALID_SELLER))
)
cut = poke["sale_date"].max() - timedelta(days=90)
recent = poke.filter(pl.col("sale_date") >= cut)
print("90d GMV", recent["price_usd"].sum())
print("sellers", recent["seller_name"].n_unique())
print("txns", recent.height)
PY
```

Pipeline: `cardchase-lake-of-rage` → `docs/lakehouse-schema.md`.
