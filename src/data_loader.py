import pandas as pd


def load_csv(path, date_columns=None):
    """
    Load a CSV file and optionally convert selected columns to datetime.

    Parameters
    ----------
    path : str or pathlib.Path
        Path to the CSV file.

    date_columns : list, optional
        List of column names that should be converted to datetime.

    Returns
    -------
    pandas.DataFrame
        Loaded dataframe.
    """
    if date_columns is None:
        date_columns = []

    df = pd.read_csv(path)

    for column in date_columns:
        if column in df.columns:
            df[column] = pd.to_datetime(df[column], errors="coerce")

    return df


def load_model_dataset(path):
    """
    Load the final model dataset.

    If a date column exists, it is converted to datetime and the dataset is sorted by date.
    """
    df = pd.read_csv(path)

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.sort_values("date")

    return df
