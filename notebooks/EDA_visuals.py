import sys
import os
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import seaborn as sns

warnings.filterwarnings("ignore")

BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR    = os.path.join(BASE_DIR, "..")
DATA_CLEAN  = os.path.join(ROOT_DIR, "data", "processed")
FIGURES_DIR = os.path.join(ROOT_DIR, "results", "figures")
os.makedirs(FIGURES_DIR, exist_ok=True)

LABEL_MAP = {0: "SELL", 1: "HOLD", 2: "BUY"}

PALETTE = {
    "earthquake": "#e85d04",
    "stock":      "#1d3557",
    "sell":       "#e63946",
    "hold":       "#457b9d",
    "buy":        "#2a9d8f",
    "neutral":    "#8ecae6",
}

plt.style.use("seaborn-v0_8-whitegrid")

ds_path = os.path.join(DATA_CLEAN, "model_dataset.csv")
if not os.path.exists(ds_path):
    raise FileNotFoundError(f"model_dataset.csv not found at {ds_path}. Run 04_feature_engineering.py first.")

df = pd.read_csv(ds_path, parse_dates=["date"])
df = df.sort_values("date").reset_index(drop=True)

print("=" * 60)
print("EDA VISUALS")
print("=" * 60)
print(f"\n  Shape : {df.shape}")
print(f"  Dates : {df['date'].min().date()} -> {df['date'].max().date()}")


def save_fig(name):
    path = os.path.join(FIGURES_DIR, name)
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"  saved: {name}")


fig, axes = plt.subplots(2, 1, figsize=(14, 7), sharex=True, gridspec_kw={"height_ratios": [3, 1]})
ax1, ax2 = axes
ax1.scatter(df["date"], df["max_magnitude_1d"], alpha=0.45, s=7, color=PALETTE["earthquake"], rasterized=True)
ax1.set_title("Earthquake Activity Over Time", fontsize=14, fontweight="bold")
ax1.set_ylabel("Max Daily Magnitude")
ax1.axhline(7, color="darkred", linewidth=0.9, linestyle="--", label="M 7.0")
ax1.legend(fontsize=9)
ax2.bar(df["date"], df["quake_count_1d"], width=1, color=PALETTE["earthquake"], alpha=0.6)
ax2.set_ylabel("Quake Count")
ax2.set_xlabel("Date")
ax2.xaxis.set_major_locator(mdates.YearLocator())
ax2.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
save_fig("earthquake_timeline.png")

fig, ax = plt.subplots(figsize=(14, 5))
ax.plot(df["date"], df["close"], color=PALETTE["stock"], linewidth=1.3, alpha=0.9)
ax.fill_between(df["date"], df["close"], df["close"].min(), alpha=0.08, color=PALETTE["stock"])
ax.set_title("Insurance Stock Close Price Over Time", fontsize=14, fontweight="bold")
ax.set_xlabel("Date")
ax.set_ylabel("Close Price (JPY)")
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
save_fig("stock_price_timeline.png")

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
returns = df["return"].dropna()
axes[0].hist(returns, bins=80, color=PALETTE["stock"], alpha=0.75, edgecolor="white")
axes[0].axvline(0, color="black", linewidth=1.3, linestyle="--", label="Zero")
axes[0].axvline(returns.mean(), color="red", linewidth=1, linestyle=":", label=f"Mean={returns.mean():.4f}")
axes[0].set_title("Daily Stock Return Distribution", fontsize=13, fontweight="bold")
axes[0].set_xlabel("Daily Return")
axes[0].set_ylabel("Frequency")
axes[0].legend(fontsize=9)
ab = df["abnormal_return"].dropna()
axes[1].hist(ab, bins=80, color=PALETTE["neutral"], alpha=0.8, edgecolor="white")
axes[1].axvline(0, color="black", linewidth=1.3, linestyle="--")
axes[1].set_title("Abnormal Return Distribution\n(Return - Market Return)", fontsize=13, fontweight="bold")
axes[1].set_xlabel("Abnormal Return")
axes[1].set_ylabel("Frequency")
save_fig("stock_return_distribution.png")

counts = df["target_signal"].value_counts().sort_index()
labels_str  = [LABEL_MAP[i] for i in counts.index]
colors_bar  = [PALETTE["sell"], PALETTE["hold"], PALETTE["buy"]]
fig, axes = plt.subplots(1, 2, figsize=(11, 5))
bars = axes[0].bar(labels_str, counts.values, color=colors_bar, edgecolor="white", width=0.5)
for bar, val in zip(bars, counts.values):
    axes[0].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + counts.max() * 0.01,
                 f"{val:,}", ha="center", va="bottom", fontweight="bold", fontsize=10)
axes[0].set_title("Label Distribution (count)", fontsize=13, fontweight="bold")
axes[0].set_ylabel("Number of Trading Days")
axes[1].pie(counts.values, labels=labels_str, colors=colors_bar, autopct="%1.1f%%",
            startangle=90, wedgeprops={"edgecolor": "white", "linewidth": 1.5},
            textprops={"fontsize": 11})
axes[1].set_title("Label Distribution (%)", fontsize=13, fontweight="bold")
save_fig("label_distribution.png")

viz = df[df["max_magnitude_1d"] > 0].dropna(subset=["max_magnitude_1d", "return"])
signal_colors = viz["target_signal"].map({0: PALETTE["sell"], 1: PALETTE["hold"], 2: PALETTE["buy"]})
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
axes[0].scatter(viz["max_magnitude_1d"], viz["return"], c=signal_colors, alpha=0.4, s=12)
z = np.polyfit(viz["max_magnitude_1d"], viz["return"], 1)
xs = np.linspace(viz["max_magnitude_1d"].min(), viz["max_magnitude_1d"].max(), 100)
axes[0].plot(xs, np.poly1d(z)(xs), color="black", linewidth=1.5, linestyle="--",
             label=f"Trend (slope={z[0]:.5f})")
axes[0].axhline(0, color="gray", linewidth=0.8, linestyle=":")
axes[0].set_title("Max Magnitude vs Stock Return\n(coloured by signal)", fontsize=12, fontweight="bold")
axes[0].set_xlabel("Max Daily Earthquake Magnitude")
axes[0].set_ylabel("Stock Daily Return")
axes[0].legend(fontsize=9)
viz2 = viz.copy()
viz2["mag_bucket"] = pd.cut(viz2["max_magnitude_1d"], bins=[0, 4, 5, 6, 7, 10],
                             labels=["<4", "4-5", "5-6", "6-7", ">7"])
viz2.boxplot(column="return", by="mag_bucket", ax=axes[1],
             boxprops=dict(color=PALETTE["earthquake"]),
             medianprops=dict(color="black", linewidth=2), patch_artist=True)
axes[1].set_title("Return Distribution by Magnitude Bucket", fontsize=12, fontweight="bold")
axes[1].set_xlabel("Magnitude Range")
axes[1].set_ylabel("Stock Daily Return")
plt.suptitle("")
save_fig("magnitude_vs_return.png")

heatmap_cols = [
    "max_magnitude_1d", "quake_count_1d", "avg_depth_1d",
    "energy_sum_1d", "energy_max_1d",
    "min_distance_tokyo_km", "min_distance_osaka_km",
    "volatility_5", "volatility_20",
    "rolling_return_5", "rolling_return_10",
    "market_return", "abnormal_return", "return_lag_1",
    "target_abnormal_return_next_day",
]
heatmap_cols = [c for c in heatmap_cols if c in df.columns]
corr = df[heatmap_cols].corr()
fig, ax = plt.subplots(figsize=(13, 10))
mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="RdBu_r", center=0,
            linewidths=0.4, linecolor="white", square=True, ax=ax,
            annot_kws={"size": 7.5}, cbar_kws={"shrink": 0.7})
ax.set_title("Feature Correlation Heatmap", fontsize=14, fontweight="bold")
save_fig("correlation_heatmap.png")

top_eq = df.nlargest(10, "max_magnitude_1d")[
    ["date", "max_magnitude_1d", "return", "abnormal_return", "target_signal"]
].copy()
top_eq["signal_name"] = top_eq["target_signal"].map(LABEL_MAP)
top_eq = top_eq.sort_values("max_magnitude_1d", ascending=True)
colors_top = top_eq["return"].apply(lambda r: PALETTE["sell"] if r < 0 else PALETTE["buy"])
fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(
    top_eq["date"].dt.strftime("%Y-%m-%d") + "  M" + top_eq["max_magnitude_1d"].round(1).astype(str),
    top_eq["return"], color=colors_top, edgecolor="white",
)
ax.axvline(0, color="black", linewidth=0.9)
ax.set_title("Top 10 Earthquake Days - Stock Return", fontsize=13, fontweight="bold")
ax.set_xlabel("Stock Daily Return")
save_fig("top_earthquake_events.png")

print("\n" + "=" * 60)
print("EDA SUMMARY STATISTICS")
print("=" * 60)
print(f"\n  Trading days     : {len(df):,}")
print(f"  Days w/ quakes   : {(df['quake_count_1d'] > 0).sum():,}")
print(f"  Total quake evts : {int(df['quake_count_1d'].sum()):,}")
print(f"  Max magnitude    : {df['max_magnitude_1d'].max():.1f}")
print(f"  Mean return      : {df['return'].mean():.4f}")
print(f"  Std return       : {df['return'].std():.4f}")
print()
for k, name in LABEL_MAP.items():
    n   = (df["target_signal"] == k).sum()
    pct = n / len(df) * 100
    print(f"  {name:4s} ({k}) : {n:5,}  ({pct:.1f}%)")
print(f"\n  Done. Figures -> {FIGURES_DIR}\n")
