import sys
import os
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

warnings.filterwarnings("ignore")

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from features import build_feature_dataset
from labels import build_labels, LABEL_MAP

BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR    = os.path.join(BASE_DIR, "..")
DATA_CLEAN  = os.path.join(ROOT_DIR, "data", "processed")
FIGURES_DIR = os.path.join(ROOT_DIR, "results", "figures")
DOCS_DIR    = os.path.join(ROOT_DIR, "docs")

os.makedirs(DATA_CLEAN,  exist_ok=True)
os.makedirs(FIGURES_DIR, exist_ok=True)
os.makedirs(DOCS_DIR,    exist_ok=True)

print("=" * 60)
print("FEATURE ENGINEERING PIPELINE")
print("=" * 60)

print("\n[1/8] Loading cleaned data ...")

eq_path = os.path.join(DATA_CLEAN, "earthquakes_clean.csv")
if not os.path.exists(eq_path):
    print(f"  WARNING: {eq_path} not found. Using synthetic data.")
    rng = np.random.default_rng(42)
    dates = pd.date_range("2011-01-01", "2023-12-31", freq="D")
    n_eq = 2000
    eq_df = pd.DataFrame({
        "date":      pd.to_datetime(rng.choice(dates, size=n_eq, replace=True)),
        "magnitude": rng.uniform(4.0, 8.0, n_eq),
        "depth":     rng.uniform(5.0, 600.0, n_eq),
        "latitude":  rng.uniform(30.0, 45.0, n_eq),
        "longitude": rng.uniform(130.0, 145.0, n_eq),
    })
else:
    eq_df = pd.read_csv(eq_path, parse_dates=["date"])

stock_path = os.path.join(DATA_CLEAN, "stock_clean.csv")
if not os.path.exists(stock_path):
    print(f"  WARNING: {stock_path} not found. Using synthetic data.")
    rng = np.random.default_rng(7)
    trading_days = pd.bdate_range("2011-01-01", "2023-12-31")
    n = len(trading_days)
    stock_df = pd.DataFrame({
        "date":   trading_days,
        "ticker": "8766.T",
        "close":  1000 * np.cumprod(1 + rng.normal(0, 0.01, n)),
        "volume": rng.integers(500_000, 5_000_000, n),
    })
else:
    stock_df = pd.read_csv(stock_path, parse_dates=["date"])

market_path = os.path.join(DATA_CLEAN, "market_clean.csv")
if not os.path.exists(market_path):
    print(f"  WARNING: {market_path} not found. Using synthetic data.")
    rng = np.random.default_rng(99)
    trading_days = pd.bdate_range("2011-01-01", "2023-12-31")
    n = len(trading_days)
    market_df = pd.DataFrame({
        "date":  trading_days,
        "close": 10_000 * np.cumprod(1 + rng.normal(0, 0.008, n)),
    })
else:
    market_df = pd.read_csv(market_path, parse_dates=["date"])

print(f"  Earthquake rows : {len(eq_df):,}")
print(f"  Stock rows      : {len(stock_df):,}")
print(f"  Market rows     : {len(market_df):,}")

print("\n[2/8] Building features ...")
model_df = build_feature_dataset(stock_df, market_df, eq_df)
print(f"  Merged rows : {len(model_df):,}  |  cols : {len(model_df.columns)}")

print("\n[3/8] Creating Buy / Hold / Sell labels ...")
model_df = build_labels(model_df, threshold=0.005, method="fixed")

label_counts = model_df["target_signal"].value_counts().sort_index()
label_pct    = model_df["target_signal"].value_counts(normalize=True).sort_index()
for k, name in LABEL_MAP.items():
    print(f"  {name:4s} ({k}) : {label_counts.get(k, 0):5,}  ({label_pct.get(k, 0)*100:.1f}%)")

print("\n[4/8] Validation ...")
model_df = model_df.sort_values("date").reset_index(drop=True)
important_cols = ["date", "return", "market_return", "abnormal_return", "target_signal"]
missing = model_df[important_cols].isna().sum()
if missing.sum() > 0:
    print("  Missing values:")
    print(missing[missing > 0])
else:
    print("  No missing values in important columns")
print(f"  Date range : {model_df['date'].min().date()} -> {model_df['date'].max().date()}")

print("\n[5/8] Saving model dataset ...")
ordered_cols = [
    "date", "ticker", "close", "return", "market_return", "abnormal_return",
    "quake_count_1d", "max_magnitude_1d", "avg_magnitude_1d", "avg_depth_1d", "min_depth_1d",
    "energy_sum_1d", "energy_max_1d", "quake_count_3d", "max_magnitude_3d", "energy_sum_3d",
    "min_distance_tokyo_km", "min_distance_osaka_km", "min_distance_sendai_km",
    "min_distance_fukushima_km", "min_distance_major_city_km", "days_since_last_quake",
    "return_lag_1", "return_lag_2", "return_lag_3", "return_lag_5",
    "rolling_return_5", "rolling_return_10",
    "volatility_5", "volatility_10", "volatility_20", "volume_change",
    "target_return_next_day", "target_abnormal_return_next_day", "target_signal",
]
ordered_cols = [c for c in ordered_cols if c in model_df.columns]
model_df = model_df[ordered_cols]

out_path = os.path.join(DATA_CLEAN, "model_dataset.csv")
model_df.to_csv(out_path, index=False)
print(f"  Saved -> {out_path}  |  shape: {model_df.shape}")

feature_columns = [
    "quake_count_1d", "max_magnitude_1d", "avg_magnitude_1d", "avg_depth_1d", "min_depth_1d",
    "energy_sum_1d", "energy_max_1d", "quake_count_3d", "max_magnitude_3d", "energy_sum_3d",
    "min_distance_tokyo_km", "min_distance_osaka_km", "min_distance_sendai_km",
    "min_distance_fukushima_km", "min_distance_major_city_km", "days_since_last_quake",
    "return_lag_1", "return_lag_2", "return_lag_3", "return_lag_5",
    "rolling_return_5", "rolling_return_10",
    "volatility_5", "volatility_10", "volatility_20",
    "volume_change", "market_return", "abnormal_return",
]
feature_columns = [c for c in feature_columns if c in model_df.columns]
print(f"\n  Feature columns ({len(feature_columns)}) -> target_signal")

plt.style.use("seaborn-v0_8-whitegrid")
COLOR_EQ    = "#e85d04"
COLOR_STOCK = "#1d3557"
COLOR_SELL  = "#e63946"
COLOR_HOLD  = "#457b9d"
COLOR_BUY   = "#2a9d8f"

print("\n[6/8] Saving EDA figures ...")

fig, ax = plt.subplots(figsize=(14, 4))
eq_plot = eq_df.sort_values("date")
ax.scatter(eq_plot["date"], eq_plot["magnitude"], alpha=0.35, s=8, color=COLOR_EQ, rasterized=True)
ax.set_title("Earthquake Magnitude Over Time", fontsize=14, fontweight="bold")
ax.set_xlabel("Date")
ax.set_ylabel("Magnitude")
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
plt.tight_layout()
fig.savefig(os.path.join(FIGURES_DIR, "earthquake_timeline.png"), dpi=150)
plt.close()

fig, ax = plt.subplots(figsize=(14, 4))
stock_plot = stock_df.sort_values("date")
ax.plot(stock_plot["date"], stock_plot["close"], color=COLOR_STOCK, linewidth=1.2)
ax.set_title("Insurance Stock Close Price Over Time", fontsize=14, fontweight="bold")
ax.set_xlabel("Date")
ax.set_ylabel("Close Price")
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
plt.tight_layout()
fig.savefig(os.path.join(FIGURES_DIR, "stock_price_timeline.png"), dpi=150)
plt.close()

fig, ax = plt.subplots(figsize=(10, 5))
ax.hist(model_df["return"].dropna(), bins=80, color=COLOR_STOCK, alpha=0.75, edgecolor="white")
ax.axvline(0, color="black", linewidth=1.2, linestyle="--")
ax.set_title("Daily Stock Return Distribution", fontsize=14, fontweight="bold")
ax.set_xlabel("Daily Return")
ax.set_ylabel("Frequency")
plt.tight_layout()
fig.savefig(os.path.join(FIGURES_DIR, "stock_return_distribution.png"), dpi=150)
plt.close()

fig, ax = plt.subplots(figsize=(7, 5))
counts = model_df["target_signal"].value_counts().sort_index()
bars = ax.bar(
    [LABEL_MAP[i] for i in counts.index],
    counts.values,
    color=[COLOR_SELL, COLOR_HOLD, COLOR_BUY],
    edgecolor="white", width=0.55,
)
for bar, val in zip(bars, counts.values):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 5,
            str(val), ha="center", va="bottom", fontweight="bold")
ax.set_title("Buy / Hold / Sell Label Distribution", fontsize=14, fontweight="bold")
ax.set_xlabel("Signal")
ax.set_ylabel("Count")
plt.tight_layout()
fig.savefig(os.path.join(FIGURES_DIR, "label_distribution.png"), dpi=150)
plt.close()

fig, ax = plt.subplots(figsize=(9, 6))
viz = model_df[model_df["max_magnitude_1d"] > 0].dropna(subset=["max_magnitude_1d", "return"])
ax.scatter(viz["max_magnitude_1d"], viz["return"], alpha=0.35, s=12, color=COLOR_EQ)
z = np.polyfit(viz["max_magnitude_1d"], viz["return"], 1)
xs = np.linspace(viz["max_magnitude_1d"].min(), viz["max_magnitude_1d"].max(), 100)
ax.plot(xs, np.poly1d(z)(xs), color="black", linewidth=1.5, linestyle="--", label="Linear trend")
ax.axhline(0, color="gray", linewidth=0.8, linestyle=":")
ax.set_title("Max Daily Magnitude vs Stock Return", fontsize=13, fontweight="bold")
ax.set_xlabel("Max Earthquake Magnitude")
ax.set_ylabel("Stock Daily Return")
ax.legend()
plt.tight_layout()
fig.savefig(os.path.join(FIGURES_DIR, "magnitude_vs_return.png"), dpi=150)
plt.close()

heatmap_cols = [
    "max_magnitude_1d", "avg_depth_1d", "energy_sum_1d",
    "min_distance_tokyo_km", "min_distance_osaka_km",
    "volatility_5", "volatility_20",
    "market_return", "abnormal_return", "return_lag_1",
    "target_abnormal_return_next_day",
]
heatmap_cols = [c for c in heatmap_cols if c in model_df.columns]
corr = model_df[heatmap_cols].corr()
fig, ax = plt.subplots(figsize=(12, 9))
mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="RdBu_r", center=0,
            linewidths=0.4, linecolor="white", square=True, ax=ax,
            annot_kws={"size": 8})
ax.set_title("Feature Correlation Heatmap", fontsize=14, fontweight="bold")
plt.tight_layout()
fig.savefig(os.path.join(FIGURES_DIR, "correlation_heatmap.png"), dpi=150)
plt.close()

print("  All figures saved.")
print("\n" + "=" * 60)
print("PIPELINE COMPLETE")
print("=" * 60)
print(f"\n  model_dataset.csv -> {out_path}")
print(f"  Shape             -> {model_df.shape}")
print(f"  Figures           -> {FIGURES_DIR}\n")
