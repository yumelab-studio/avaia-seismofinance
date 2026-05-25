import numpy as np
import pandas as pd


MAJOR_CITIES = {
    "tokyo":     (35.6762, 139.6503),
    "osaka":     (34.6937, 135.5023),
    "sendai":    (38.2682, 140.8694),
    "fukushima": (37.7608, 140.4747),
}


def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371
    lat1 = np.radians(lat1)
    lon1 = np.radians(lon1)
    lat2 = np.radians(lat2)
    lon2 = np.radians(lon2)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arcsin(np.sqrt(a))
    return R * c


def add_distance_features(eq_df):
    df = eq_df.copy()
    for city, (city_lat, city_lon) in MAJOR_CITIES.items():
        df[f"dist_{city}_km"] = haversine_distance(
            df["latitude"].values, df["longitude"].values, city_lat, city_lon
        )
    return df


def add_energy_feature(eq_df):
    df = eq_df.copy()
    df["energy"] = 10 ** (1.5 * df["magnitude"])
    return df


def aggregate_earthquakes_by_day(eq_df):
    df = eq_df.copy()
    df["date"] = pd.to_datetime(df["date"]).dt.normalize()
    df = add_energy_feature(df)
    df = add_distance_features(df)

    agg = df.groupby("date").agg(
        quake_count_1d=("magnitude", "count"),
        max_magnitude_1d=("magnitude", "max"),
        avg_magnitude_1d=("magnitude", "mean"),
        avg_depth_1d=("depth", "mean"),
        min_depth_1d=("depth", "min"),
        energy_sum_1d=("energy", "sum"),
        energy_max_1d=("energy", "max"),
        min_distance_tokyo_km=("dist_tokyo_km", "min"),
        min_distance_osaka_km=("dist_osaka_km", "min"),
        min_distance_sendai_km=("dist_sendai_km", "min"),
        min_distance_fukushima_km=("dist_fukushima_km", "min"),
    ).reset_index()

    city_dist_cols = [
        "min_distance_tokyo_km", "min_distance_osaka_km",
        "min_distance_sendai_km", "min_distance_fukushima_km",
    ]
    agg["min_distance_major_city_km"] = agg[city_dist_cols].min(axis=1)
    return agg


def add_rolling_earthquake_features(daily_eq_df, stock_dates):
    all_dates = pd.date_range(
        start=daily_eq_df["date"].min(),
        end=daily_eq_df["date"].max(),
        freq="D",
    )
    df = daily_eq_df.set_index("date").reindex(all_dates).fillna(0)
    df.index.name = "date"

    df["quake_count_3d"]   = df["quake_count_1d"].rolling(3, min_periods=1).sum()
    df["max_magnitude_3d"] = df["max_magnitude_1d"].rolling(3, min_periods=1).max()
    df["energy_sum_3d"]    = df["energy_sum_1d"].rolling(3, min_periods=1).sum()

    df["had_quake"] = (df["quake_count_1d"] > 0).astype(int)
    days_since = []
    last = None
    for idx, row in df.iterrows():
        if row["had_quake"]:
            last = idx
        days_since.append((idx - last).days if last is not None else np.nan)
    df["days_since_last_quake"] = days_since

    df = df.reset_index().rename(columns={"index": "date"})
    df = df[df["date"].isin(stock_dates.values)]
    return df.drop(columns=["had_quake"], errors="ignore")


def add_financial_features(stock_df, market_df):
    stock = stock_df.copy()
    market = market_df.copy()

    stock["date"]  = pd.to_datetime(stock["date"])
    market["date"] = pd.to_datetime(market["date"])

    stock = stock.sort_values("date").reset_index(drop=True)
    stock["return"] = stock["close"].pct_change()

    market = market.sort_values("date").reset_index(drop=True)
    market["market_return"] = market["close"].pct_change()
    market = market.rename(columns={"close": "market_close"})[["date", "market_return"]]

    df = stock.merge(market, on="date", how="left")
    df["abnormal_return"] = df["return"] - df["market_return"]

    for lag in [1, 2, 3, 5]:
        df[f"return_lag_{lag}"] = df["return"].shift(lag)

    df["rolling_return_5"]  = df["return"].rolling(5,  min_periods=1).mean()
    df["rolling_return_10"] = df["return"].rolling(10, min_periods=1).mean()
    df["volatility_5"]      = df["return"].rolling(5,  min_periods=2).std()
    df["volatility_10"]     = df["return"].rolling(10, min_periods=2).std()
    df["volatility_20"]     = df["return"].rolling(20, min_periods=2).std()

    if "volume" in df.columns:
        df["volume_change"] = df["volume"].pct_change()
    else:
        df["volume_change"] = np.nan

    return df


def build_feature_dataset(stock_df, market_df, eq_df):
    fin = add_financial_features(stock_df, market_df)
    fin["date"] = pd.to_datetime(fin["date"])

    daily_eq = aggregate_earthquakes_by_day(eq_df)
    daily_eq["date"] = pd.to_datetime(daily_eq["date"])

    daily_eq_rolling = add_rolling_earthquake_features(daily_eq, fin["date"])
    daily_eq_rolling["date"] = pd.to_datetime(daily_eq_rolling["date"])

    df = fin.merge(daily_eq_rolling, on="date", how="left")

    eq_fill_zero = [
        "quake_count_1d", "quake_count_3d",
        "max_magnitude_1d", "avg_magnitude_1d", "max_magnitude_3d",
        "avg_depth_1d", "min_depth_1d",
        "energy_sum_1d", "energy_max_1d", "energy_sum_3d",
    ]
    for col in eq_fill_zero:
        if col in df.columns:
            df[col] = df[col].fillna(0)

    dist_cols = [c for c in df.columns if "distance" in c or "dist_" in c]
    for col in dist_cols:
        df[col] = df[col].fillna(df[col].max() if df[col].notna().any() else 9999)

    df = df.sort_values("date").reset_index(drop=True)
    return df
