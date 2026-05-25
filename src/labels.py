import pandas as pd


LABEL_MAP = {0: "SELL", 1: "HOLD", 2: "BUY"}


def create_next_day_targets(df):
    df = df.copy()
    df["target_return_next_day"]          = df["return"].shift(-1)
    df["target_abnormal_return_next_day"] = df["abnormal_return"].shift(-1)
    return df


def create_signal_label(x, threshold=0.005):
    if pd.isna(x):
        return pd.NA
    if x < -threshold:
        return 0
    elif x > threshold:
        return 2
    else:
        return 1


def add_signal_labels(df, threshold=0.005):
    df = df.copy()
    df["target_signal"] = df["target_abnormal_return_next_day"].apply(
        lambda x: create_signal_label(x, threshold)
    )
    return df


def add_signal_labels_quantile(df, q=3):
    df = df.copy()
    df["target_signal"] = pd.qcut(
        df["target_abnormal_return_next_day"],
        q=q,
        labels=list(range(q)),
        duplicates="drop",
    ).astype("Int64")
    return df


def build_labels(df, threshold=0.005, method="fixed"):
    df = create_next_day_targets(df)
    if method == "quantile":
        df = add_signal_labels_quantile(df)
    else:
        df = add_signal_labels(df, threshold=threshold)
    df = df.dropna(subset=["target_signal"])
    df["target_signal"] = df["target_signal"].astype(int)
    return df


def decode_signal(series):
    return series.map(LABEL_MAP)
