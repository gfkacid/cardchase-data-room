"""Rebuild the two pricing-comparison CSVs from the validation snapshot.

Self-contained. No network, no scraper. Reads validation_snapshot.json in this
folder and writes the CSVs one level up.

  python3 build_dataset.py
"""

import csv
import json
import statistics
from pathlib import Path

HERE = Path(__file__).resolve().parent
SNAPSHOT = HERE / "validation_snapshot.json"
OUT = HERE.parent

SAMPLE_CARDS = 10
MIN_MARKET_USD = 25  # "worth $25+" means TCGplayer market value, not the eBay side


def card_rows(card):
    for date, ebay, tcg, n in card["buckets"]:
        if tcg in (None, 0):
            continue
        yield {
            "card": card["name"],
            "card_id": card["pid"],
            "date": date,
            "ebay_sold_nm_usd": round(ebay, 2),
            "tcgplayer_nm_usd": round(tcg, 2),
            "diff_pct": round((ebay - tcg) / tcg * 100, 1),
            "ebay_sales_count": n,
        }


def median_tcg(card):
    vals = [tcg for _, _, tcg, _ in card["buckets"] if tcg]
    return statistics.median(vals) if vals else 0.0


def pick_sample(cards):
    priced = sorted(cards, key=median_tcg)
    n = len(priced)
    tiers = [priced[: n // 3], priced[n // 3 : 2 * n // 3], priced[2 * n // 3 :]]
    chosen = []
    per_tier = SAMPLE_CARDS // 3
    for i, tier in enumerate(tiers):
        take = per_tier + (1 if i < SAMPLE_CARDS - per_tier * 3 else 0)
        chosen += sorted(tier, key=lambda c: len(c["buckets"]), reverse=True)[:take]
    return chosen


def summary_row(card):
    rows = list(card_rows(card))
    ebay = [r["ebay_sold_nm_usd"] for r in rows]
    tcg = [r["tcgplayer_nm_usd"] for r in rows]
    ratios = [e / t for e, t in zip(ebay, tcg)]
    return {
        "card": card["name"],
        "card_id": card["pid"],
        "comparison_windows": len(rows),
        "ebay_median_nm_usd": round(statistics.median(ebay), 2),
        "tcgplayer_median_nm_usd": round(statistics.median(tcg), 2),
        "median_abs_diff_pct": round(card["metrics"]["median_abs_pct_diff"] * 100, 1),
        "ebay_vs_tcg_ratio": round(statistics.median(ratios), 3),
    }


def write_csv(path, rows, fields):
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def main():
    report = json.loads(SNAPSHOT.read_text())
    cards = [c for c in report["cards"] if c["buckets"] and median_tcg(c) >= MIN_MARKET_USD]

    sample = pick_sample(cards)
    sample_rows = []
    for c in sorted(sample, key=median_tcg):
        sample_rows += sorted(card_rows(c), key=lambda r: r["date"])
    write_csv(
        OUT / "pricing_comparison_sample.csv",
        sample_rows,
        ["card", "card_id", "date", "ebay_sold_nm_usd", "tcgplayer_nm_usd",
         "diff_pct", "ebay_sales_count"],
    )

    summary = [summary_row(c) for c in sorted(cards, key=median_tcg, reverse=True)]
    write_csv(
        OUT / "pricing_comparison_summary.csv",
        summary,
        ["card", "card_id", "comparison_windows", "ebay_median_nm_usd",
         "tcgplayer_median_nm_usd", "median_abs_diff_pct", "ebay_vs_tcg_ratio"],
    )

    print(f"sample: {len(sample_rows)} rows across {len(sample)} cards")
    print(f"summary: {len(summary)} cards")


if __name__ == "__main__":
    main()
