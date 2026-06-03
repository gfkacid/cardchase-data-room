# Reproduce

`build_dataset.py` reads `validation_snapshot.json` and writes
`../pricing_comparison_sample.csv` and `../pricing_comparison_summary.csv`.

    python3 build_dataset.py

## Important: Pikachu ex 276 manual override

The Pikachu ex 276 (`me2pt5-276`) row in `pricing_comparison_summary.csv` was
updated manually with figures from the NM-only deep-dive (May 2–27 2026, three
combined sources). The snapshot still holds the original 3-day-bucket data for
that card. Re-running `build_dataset.py` will overwrite row 2 with the stale
snapshot values.

After any re-run, restore the Pikachu ex 276 row to:

```
Pikachu ex,me2pt5-276,26,1299.5,1108.22,8.6,1.173
```

The full daily breakdown behind these numbers is in `../pikachu276_nm_daily.csv`.
