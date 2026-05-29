Data Sources

Overview

This project uses three datasets: earthquake data, Japanese insurance stock data,
and a Japanese market index. All datasets are aligned by date to enable analysis
of earthquake impact on stock market returns.

---

1. Earthquake Data

Source: USGS Earthquake Hazards Program — Earthquake Catalog  
URL: https://earthquake.usgs.gov/earthquakes/search/  
File: `data/raw/earthquake.csv`  
Clean file: `data/clean/earthquake_clean_v2.csv`

Collection method:
Downloaded via the USGS web interface with the following filters:
- Region: Japan (latitude 24–46, longitude 122–146)
- Minimum magnitude: 5.0
- Date range: 2011-04-06 to 2026-04-04

Columns used:

| Raw column | Renamed to | Description |
|---|---|---|
| time | datetime_utc | Earthquake timestamp in UTC |
| — | datetime_jst | Timestamp converted to Japan time (UTC+9) |
| — | date_jst | Date in Japan time (for stock matching) |
| latitude | latitude | Latitude of epicenter |
| longitude | longitude | Longitude of epicenter |
| depth | depth_km | Depth of earthquake in kilometers |
| mag | magnitude | Earthquake magnitude |
| place | place | Description of location |
| type | type | Event type (earthquake, etc.) |
| status | status | Review status (reviewed / automatic) |

Why these columns: 
Magnitude alone is insufficient for modeling. Depth affects surface impact.
Location (latitude/longitude) enables distance-based feature engineering.
Timezone conversion to JST is required to correctly align earthquake events
with Japanese stock trading days.

---

2. Stock Data — Tokio Marine Holdings (8766.T)

Source: Yahoo Finance via `yfinance` Python library  
Ticker: 8766.T (Tokio Marine Holdings — major Japanese insurance company)  
File: `data/raw/stocks.csv`  
Clean file:** `data/clean/stocks_clean_v2.csv`

Collection method: 
Downloaded programmatically using `yfinance.download()` with `start="2010-01-01"`.

Columns in clean file:

| Column | Description |
|---|---|
| date | Trading date |
| ticker | Stock symbol (8766.T) |
| close | Adjusted closing price (JPY) |
| volume | Daily trading volume |
| return | Daily percentage return: (close_t - close_t-1) / close_t-1 |

Why 8766.T: 
Tokio Marine Holdings is one of Japan's largest insurance companies. Insurance
stocks are directly exposed to earthquake risk through claims liability, making
them a relevant subject for this analysis.

---

3. Market Index — Nikkei 225 (^N225)

Source: Yahoo Finance via `yfinance` Python library  
Ticker: ^N225 (Nikkei 225 — main Japanese stock market index)  
File: `data/raw/market_index.csv`  
Clean file: `data/clean/market_index_clean.csv`

Collection method:  
Downloaded programmatically using `yfinance.download()` with `start="2010-01-01"`.

Columns in clean file:

| Column | Description |
|---|---|
| date | Trading date |
| market_close | Nikkei 225 closing value |
| market_return | Daily percentage return of the index |

Date Coverage

| Dataset | Start date | End date |
|---|---|---|
| Earthquake | 2011-04-06 | 2026-04-04 |
| Stock (8766.T) | 2010-01-04 | 2026-04-02 |
| Market (^N225) | 2010-01-04 | 2026-04-02 |
