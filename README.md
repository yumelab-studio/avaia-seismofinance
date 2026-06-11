# SeismoFinance: Predicting Market Reactions to Major Earthquakes

![Project Poster](poster/final_poster_AVAIA.png)

## Overview

**SeismoFinance** is an AI project that investigates whether earthquake-related events in Japan can help predict short-term reactions in Japanese insurance stock prices.

The project combines earthquake data, stock market data, and market index data to build machine learning and deep learning models that predict the next-day abnormal return direction of **Tokio Marine Holdings (`8766.T`)**, a major Japanese insurance company.

The final system converts model predictions into a readable prototype trading signal:

```text
SELL / HOLD / BUY
```

> This project is an academic decision-support prototype and should not be interpreted as financial advice.

---

## Problem Definition

Earthquakes are sudden external events that may affect financial markets through uncertainty, expected insurance claims, perceived risk, and investor reaction.

Japan is highly exposed to seismic activity, making earthquake-related events especially relevant for companies in the insurance sector.

This project asks:

```text
Can earthquake-related data, combined with financial time-series indicators,
be used to predict the next-day market reaction of a Japanese insurance stock?
```

The final prediction task is formulated as a three-class classification problem:

| Class | Signal | Meaning |
|---:|---|---|
| 0 | SELL | Expected negative next-day abnormal return |
| 1 | HOLD | Expected near-neutral next-day abnormal return |
| 2 | BUY | Expected positive next-day abnormal return |

---

## Project Objectives

The main objectives of this project were to:

1. Collect earthquake, stock, and market index data.
2. Clean and align the datasets by Japanese trading dates.
3. Engineer earthquake-based and financial time-series features.
4. Create Buy/Hold/Sell labels using next-day abnormal return.
5. Train and compare baseline machine learning models.
6. Train and evaluate an LSTM time-series model.
7. Convert model output into a readable Buy/Hold/Sell prototype signal.
8. Document the full pipeline through notebooks, source code, results, and a final poster.

---

## Data Sources

The project uses three main data sources:

| Dataset | Source | Purpose |
|---|---|---|
| Earthquake data | USGS Earthquake Catalog | Provides seismic event data such as magnitude, depth, location, and time |
| Stock data | Yahoo Finance | Provides Tokio Marine Holdings (`8766.T`) stock prices and volume |
| Market index data | Yahoo Finance | Provides Nikkei 225 (`^N225`) market movement for abnormal return calculation |

The data is organized into three stages:

```text
data/raw/        Original downloaded datasets
data/clean/      Cleaned intermediate datasets
data/processed/  Final model-ready dataset
```

The final model dataset is stored in:

```text
data/processed/model_dataset.csv
```

More details are available in:

- [`docs/data_sources.md`](docs/data_sources.md)
- [`docs/data_quality_report.md`](docs/data_quality_report.md)

---

## Data Cleaning and Preparation

The raw datasets came from different sources and required separate cleaning steps.

### Earthquake Data

Earthquake data was cleaned by:

- selecting relevant columns
- converting timestamps from UTC to Japan Standard Time
- extracting Japanese trading dates
- filtering earthquake events by magnitude
- removing missing critical values
- removing duplicate records
- sorting events chronologically

Timezone conversion was important because earthquakes can occur at any time, while Japanese stock data is recorded by trading day.

### Stock and Market Data

Financial data was cleaned by:

- flattening Yahoo Finance multi-level headers
- keeping relevant columns such as date, close price, and volume
- calculating daily stock returns
- calculating market returns
- removing rows with missing return values
- sorting records chronologically

---

## Feature Engineering

The final dataset combines seismic and financial indicators.

### Earthquake Features

Earthquake-based features include:

- earthquake count
- maximum daily magnitude
- average daily magnitude
- average earthquake depth
- minimum earthquake depth
- earthquake energy estimates
- rolling earthquake activity features
- distance-based features for major Japanese cities
- days since last earthquake

### Financial Features

Financial features include:

- stock return
- market return
- abnormal return
- lagged returns
- rolling returns
- volatility features
- volume change

These features were designed to capture both seismic shock intensity and recent financial market behavior.

---

## Methodology

The full machine learning workflow follows this pipeline:

```text
Data collection
-> Data cleaning
-> Time alignment
-> Feature engineering
-> Target creation
-> Baseline modeling
-> LSTM modeling
-> Buy/Hold/Sell signal conversion
```

The final target is based on next-day abnormal return.

```text
0 = SELL
1 = HOLD
2 = BUY
```

The complete methodology is documented in:

- [`docs/methodology.md`](docs/methodology.md)

---

## Models

The project compares traditional machine learning baselines with a deep learning time-series model.

### Baseline Models

The following baseline models were trained:

- Majority Class Baseline
- Logistic Regression
- Support Vector Machine with RBF kernel
- K-Nearest Neighbors
- Random Forest
- Gradient Boosting

The purpose of the baseline models was to evaluate whether the LSTM model improves over simpler approaches.

### Final LSTM Model

The final deep learning model is a Long Short-Term Memory network trained on sequential windows of historical trading days.

The best sequence length was:

```text
10 trading days
```

The final LSTM architecture:

```text
Input sequence
-> LSTM layer with 64 units
-> Dropout
-> LSTM layer with 32 units
-> Dropout
-> Dense layer with 32 units and ReLU activation
-> Batch Normalization
-> Dropout
-> Dense output layer with 3 units and Softmax activation
```

The LSTM was trained using:

- time-based train/test split
- `StandardScaler` fitted only on training data
- class weights
- early stopping
- learning rate reduction
- macro F1-score as the main evaluation metric

More details are available in:

- [`docs/model_architecture.md`](docs/model_architecture.md)

---

## Results

The final LSTM model achieved the best macro F1-score among all tested models.

| Model | Accuracy | Macro Precision | Macro Recall | Macro F1 |
|---|---:|---:|---:|---:|
| LSTM | 0.3653 | 0.3641 | 0.3653 | 0.3622 |
| Gradient Boosting | 0.3560 | 0.3572 | 0.3516 | 0.3408 |
| Random Forest | 0.3383 | 0.3316 | 0.3347 | 0.3314 |
| KNN | 0.3279 | 0.3244 | 0.3258 | 0.3200 |
| SVM (RBF) | 0.3117 | 0.3094 | 0.3099 | 0.3095 |
| Logistic Regression | 0.3028 | 0.2959 | 0.3007 | 0.2942 |
| Majority Baseline | 0.3353 | 0.1118 | 0.3333 | 0.1674 |

### Interpretation

The LSTM achieved the strongest overall macro F1-score, outperforming the traditional baseline models.

However, the overall scores remain modest. This is expected because short-term stock prediction is highly noisy and affected by many factors beyond earthquake activity, including investor sentiment, global market conditions, macroeconomic events, and company-specific news.

The model should therefore be viewed as a prototype for seismic-financial decision support, not as a real trading system.

Detailed results are documented in:

- [`docs/results_summary.md`](docs/results_summary.md)

---

## Visual Results

### Model Comparison

![Model Comparison](results/figures/model_comparison.png)

The LSTM achieved the highest macro F1-score compared to all tested models.

### LSTM Confusion Matrix

![Confusion Matrix](results/figures/confusion_matrix.png)

The confusion matrix shows that BUY was the easiest class to identify, while SELL and HOLD were harder to separate.

### Training and Validation Loss

![Training and Validation Loss](results/figures/train_val_loss.png)

The training curve was used to monitor LSTM learning behavior and validation performance.

### Label Distribution

![Label Distribution](results/figures/label_distribution.png)

The target classes were reasonably balanced across SELL, HOLD, and BUY.

### Magnitude vs Stock Return

![Magnitude vs Return](results/figures/magnitude_vs_return.png)

Earthquake magnitude alone showed only a weak direct relationship with stock returns, supporting the need for richer engineered features.

---

## Final Demo

The final demo notebook loads the trained LSTM model and scaler, prepares the most recent input sequence, and converts class probabilities into a readable Buy/Hold/Sell signal.

Example output:

```text
Predicted signal after 2023-12-27: BUY
SELL probability: 30.68%
HOLD probability: 27.86%
BUY probability: 41.45%
Final prototype signal: BUY
```

The final demo is available in:

```text
notebooks/07_final_demo.ipynb
```

The signal conversion logic is implemented in:

```text
src/signals.py
```

---

## Repository Structure

```text
avaia-seismofinance/
├── data/
│   ├── raw/
│   ├── clean/
│   └── processed/
├── docs/
│   ├── data_quality_report.md
│   ├── data_sources.md
│   ├── final_submission_checklist.md
│   ├── future_work.md
│   ├── methodology.md
│   ├── model_architecture.md
│   ├── problem_definition.md
│   ├── results_summary.md
│   └── team_contributions.md
├── models/
│   ├── lstm_model.keras
│   └── scaler.pkl
├── notebooks/
│   ├── archive/
│   ├── 01_data_collection_v2.ipynb
│   ├── 02_preprocessing_v2.ipynb
│   ├── 03_baseline_model.ipynb
│   ├── 04_feature_engineering.py
│   ├── 05_model_comparison.ipynb
│   ├── 06_lstm_model.ipynb
│   ├── 07_final_demo.ipynb
│   └── EDA_visuals.py
├── poster/
│   └── final_poster_AVAIA.png
├── results/
│   ├── figures/
│   └── metrics/
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── data_loader.py
│   ├── features.py
│   ├── labels.py
│   └── signals.py
├── README.md
├── requirements.txt
└── LICENSE
```

---

## Reproducible Workflow

To reproduce the project, run the notebooks and scripts in this order:

```text
1. notebooks/01_data_collection_v2.ipynb
2. notebooks/02_preprocessing_v2.ipynb
3. notebooks/04_feature_engineering.py
4. notebooks/05_model_comparison.ipynb
5. notebooks/06_lstm_model.ipynb
6. notebooks/07_final_demo.ipynb
```

Older development notebooks are stored in:

```text
notebooks/archive/
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/yumelab-studio/avaia-seismofinance.git
cd avaia-seismofinance
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Main Dependencies

The project uses:

- Python
- pandas
- NumPy
- matplotlib
- seaborn
- scikit-learn
- TensorFlow / Keras
- yfinance
- joblib
- plotly
- Jupyter

---

## Source Code Modules

The reusable source code is stored in `src/`.

| File | Purpose |
|---|---|
| `config.py` | Stores project paths, model paths, signal threshold, and class names |
| `data_loader.py` | Provides helper functions for loading CSV files and model datasets |
| `features.py` | Contains feature engineering functions for earthquake and financial data |
| `labels.py` | Creates next-day target labels and decodes Buy/Hold/Sell classes |
| `signals.py` | Converts model outputs and probabilities into readable signals |

---

## Final Poster

The final project poster is available in:

```text
poster/final_poster_AVAIA.png
```

---

## Team Contributions

### Tyra

- organized the GitHub repository structure
- coordinated the final project workflow
- integrated documentation across the repository
- reviewed project files for consistency
- prepared the final README structure
- prepared the final poster content and layout
- worked on final project presentation materials
- helped connect model outputs to the Buy/Hold/Sell decision-support interpretation

### Adi

- implemented baseline machine learning models
- compared Logistic Regression, SVM, KNN, Random Forest, Gradient Boosting, and Majority Baseline
- developed the final LSTM model
- tested sequence lengths for the LSTM model
- saved the trained LSTM model
- generated final model metrics
- generated model comparison results
- created training and validation loss outputs

### Vanesa

- cleaned earthquake data
- cleaned stock market data
- cleaned market index data
- handled missing values and duplicate records
- worked on timezone conversion from UTC to Japan Standard Time
- helped prepare cleaned datasets in `data/clean/`
- documented data quality issues and cleaning decisions

### Erol

- engineered earthquake-based features
- engineered financial return and volatility features
- created abnormal return features
- helped create Buy/Hold/Sell target labels
- generated exploratory visualizations
- supported analysis of earthquake and market relationships
- contributed to the final processed dataset in `data/processed/model_dataset.csv`

More details are available in:

- [`docs/team_contributions.md`](docs/team_contributions.md)

---

## Limitations

The project has several limitations:

- only one insurance stock was used
- the dataset is relatively small for deep learning
- stock market reactions are influenced by many non-earthquake factors
- news sentiment and macroeconomic indicators were not included
- next-day stock movement is naturally noisy and difficult to predict

These limitations explain why the model performance is modest even though the LSTM outperformed the baselines.

---

## Future Work

Future improvements could include:

- adding more Japanese insurance stocks
- using additional earthquake impact indicators
- adding tsunami warnings and disaster severity data
- testing same-day, next-day, three-day, and weekly return horizons
- including market indicators such as TOPIX, interest rates, and exchange rates
- adding news and sentiment data
- testing more advanced deep learning architectures
- building a real-time dashboard connected to earthquake and financial APIs

More details are available in:

- [`docs/future_work.md`](docs/future_work.md)

---

## Conclusion

This project successfully built a complete seismic-financial prediction pipeline.

The final LSTM model achieved the best macro F1-score among all tested models and produced a readable Buy/Hold/Sell prototype signal. Although predictive performance remained modest, the project demonstrates how earthquake-derived features and financial indicators can be combined for academic decision-support modeling.

SeismoFinance shows that external shock data can be integrated into financial forecasting workflows, while also highlighting the difficulty of short-term market prediction.

---

## License

This project is licensed under the MIT License.
