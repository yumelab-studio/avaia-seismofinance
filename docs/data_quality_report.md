Data Quality Report

Overview

This report documents the cleaning steps, issues found, and rows removed
for each dataset. All cleaning is performed in `notebooks/02_preprocessing.ipynb`.

---

1. Earthquake Data

Raw file: `data/raw/earthquake.csv`  
Clean file: `data/clean/earthquake_clean_v2.csv`

### Row counts

| Stage | Rows |
|---|---|
| Raw file (all magnitudes) | 1330 |
| After filtering magnitude ≥ 5.0 | 1330 |
| After dropping missing values | 1330 |
| After dropping duplicates | 1330 |


Issues found and fixes applied

| Issue | Fix |
|---|---|
| Raw file contained all event types (explosions, quarry blasts, etc.) | Filtered to `type == earthquake` only |
| Timestamps stored in UTC | Converted to Japan time (JST, UTC+9) using `dt.tz_convert('Asia/Tokyo')` |
| Column `mag` was not clearly named | Renamed to `magnitude` |
| Column `depth` had no unit in the name | Renamed to `depth_km` |
| Some rows had missing latitude, longitude, depth, or magnitude | Removed with `dropna()` — these are required for feature engineering |
| Potential duplicate events | Removed with `drop_duplicates()` |

Missing values (after column selection, before cleaning)

| Column | Missing count |
|---|---|
| datetime_utc | 0 |
| latitude | 0 |
| longitude | 0 |
| depth_km | 0 |
| magnitude | 0 |
| place | 0 |
| type | 0 |
| status | 0 |

Key decisions

- Rows with missing magnitude were removed because magnitude is a core model feature.
- Rows with missing depth, latitude, or longitude were removed because these are
  needed for distance and depth-based feature engineering.
- Timezone conversion was performed before date extraction so that `date_jst`
  correctly reflects the Japanese trading day. An earthquake at 23:00 UTC on
  April 6 becomes April 7 in JST, which changes which stock trading day it maps to.

---

2. Stock Data — 8766.T

Raw file: `data/raw/stocks.csv`  
Clean file: `data/clean/stocks_clean_v2.csv`

Row counts

| Stage | Rows |
|---|---|
| Raw file (including broken header rows) | 4000 |
| After removing NaT/broken date rows | 4000 |
| After removing NaN return rows (first row) | 3999 |


Issues found and fixes applied

| Issue | Fix |
|---|---|
| Raw CSV had a multi-level header from yfinance (Price/Ticker rows) | Read with `header=[0,1]` and flattened column names |
| Row 2 contained `8766.T` as a date value (leaked ticker header) | Removed by parsing dates with `errors='coerce'` and dropping NaT |
| No ticker column in the original clean file | Added `ticker = '8766.T'` explicitly |
| Volume column was missing from previous clean version | Added `volume` to selected columns |
| First row of `return` is always NaN (no previous day) | Removed with `dropna(subset=['return'])` |
| Rows were not guaranteed to be sorted by date | Sorted with `sort_values('date')` |

Missing values (final clean file)

| Column | Missing count |
|---|---|
| date | 0 |
| ticker | 0 |
| close | 0 |
| volume | 0 |
| return | 0 |

---

3. Market Index — Nikkei 225

Raw file: `data/raw/market_index.csv`  
Clean file: `data/clean/market_index_clean.csv`

Row counts

| Stage | Rows |
|---|---|
| Downloaded from Yahoo Finance | 4009 |
| After dropping NaN return rows | 4008 |


Issues found and fixes applied

| Issue | Fix |
|---|---|
| Multi-level column header from yfinance | Worked directly with downloaded DataFrame before CSV export |
| First row of `market_return` is NaN | Removed with `dropna(subset=['market_return'])` |

Missing values (final clean file)

| Column | Missing count |
|---|---|
| date | 0 |
| market_close | 0 |
| market_return | 0 |

---

Summary

| Dataset | Main issues | Status |
|---|---|---|
| Earthquake | UTC timezone, missing columns, too few features kept | Fixed in v2 |
| Stock | Broken header rows, missing ticker/volume columns | Fixed in v2 |
| Market index | Not collected in Stage 1 | Added in Stage 2 |

All three clean files are ready for feature engineering and model training.
