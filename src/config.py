from pathlib import Path

# Root directory of the project
ROOT_DIR = Path(__file__).resolve().parents[1]

# Data directories
DATA_DIR = ROOT_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
CLEAN_DATA_DIR = DATA_DIR / "clean"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Results directories
RESULTS_DIR = ROOT_DIR / "results"
FIGURES_DIR = RESULTS_DIR / "figures"
METRICS_DIR = RESULTS_DIR / "metrics"

# Models directory
MODELS_DIR = ROOT_DIR / "models"

# Raw data paths
EARTHQUAKE_RAW_PATH = RAW_DATA_DIR / "earthquake.csv"
STOCKS_RAW_PATH = RAW_DATA_DIR / "stocks.csv"
MARKET_RAW_PATH = RAW_DATA_DIR / "market_index.csv"

# Clean data paths
EARTHQUAKE_CLEAN_PATH = CLEAN_DATA_DIR / "earthquake_clean_v2.csv"
STOCKS_CLEAN_PATH = CLEAN_DATA_DIR / "stocks_clean_v2.csv"
MARKET_CLEAN_PATH = CLEAN_DATA_DIR / "market_index_clean.csv"

# Processed data path
MODEL_DATASET_PATH = PROCESSED_DATA_DIR / "model_dataset.csv"

# Model paths
LSTM_MODEL_PATH = MODELS_DIR / "lstm_model.keras"
SCALER_PATH = MODELS_DIR / "scaler.pkl"

# Signal configuration
SIGNAL_THRESHOLD = 0.005

CLASS_NAMES = {
    0: "SELL",
    1: "HOLD",
    2: "BUY"
}
