# Methodology

## Overview

This project follows a complete machine learning workflow for predicting short-term market reactions after earthquake events in Japan.

The pipeline combines earthquake data, stock market data, and market index data, then transforms them into a supervised learning dataset for Buy/Hold/Sell prediction.

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

---

## 1. Data Collection

Three datasets were used:

| Dataset | Source | Purpose |
|---|---|---|
| Earthquake data | USGS Earthquake Catalog | Provides seismic event features such as magnitude, depth, location, and event time |
| Stock data | Yahoo Finance | Provides daily price and volume data for Tokio Marine Holdings (`8766.T`) |
| Market index data | Yahoo Finance | Provides Nikkei 225 (`^N225`) market movement for calculating market-adjusted return |

The project focuses on Japan because it is a highly earthquake-prone country and because Japanese insurance companies may be directly affected by earthquake-related financial risk.

---

## 2. Data Cleaning

The raw datasets came from different sources and required separate cleaning steps.

### Earthquake Data

Earthquake data was cleaned by:

- selecting relevant columns
- converting timestamps from UTC to Japan Standard Time
- extracting the Japanese trading date
- filtering earthquake events by magnitude
- removing rows with missing critical values
- removing duplicate records
- sorting events chronologically

The timezone conversion was important because Japanese stock prices must be matched to the correct local trading day.

### Stock Data

Stock data was cleaned by:

- flattening Yahoo Finance multi-level headers
- keeping relevant columns such as date, close price, and volume
- adding the ticker symbol explicitly
- calculating daily percentage return
- removing the first row with missing return
- sorting records by date

### Market Index Data

Nikkei 225 market index data was cleaned by:

- keeping the closing price
- calculating daily market return
- removing missing return rows
- sorting records by date

---

## 3. Time Alignment

Earthquake and financial data operate on different time systems. Earthquakes can occur at any time, including weekends and non-trading hours, while stock prices are available only for trading days.

To solve this, earthquake timestamps were converted to Japan Standard Time and then aligned with Japanese trading dates.

This allowed earthquake-related features to be joined with stock and market data on a daily basis.

---

## 4. Feature Engineering

The final model dataset includes both earthquake-based and financial features.

### Earthquake Features

The earthquake feature set includes:

- earthquake count features
- maximum daily magnitude
- average daily magnitude
- average earthquake depth
- minimum earthquake depth
- estimated earthquake energy
- distance to major Japanese cities
- days since last earthquake
- rolling earthquake activity features

### Financial Features

The financial feature set includes:

- stock return
- market return
- abnormal return
- lagged stock returns
- rolling return features
- volatility features
- volume change

These features were designed to represent both seismic shock intensity and recent financial market behavior.

---

## 5. Target Creation

The prediction target is based on the next-day abnormal return.

The task was converted into a three-class classification problem:

```text
0 = SELL
1 = HOLD
2 = BUY
```

The classes represent expected market reaction:

- `SELL`: expected negative abnormal return
- `HOLD`: expected neutral abnormal return
- `BUY`: expected positive abnormal return

This makes the final output easier to interpret as a decision-support signal.

---

## 6. Baseline Modeling

Several traditional machine learning models were trained first:

- Majority Class Baseline
- Logistic Regression
- Support Vector Machine with RBF kernel
- K-Nearest Neighbors
- Random Forest
- Gradient Boosting

The purpose of this stage was to create a fair comparison and determine whether the final LSTM model improved over simpler approaches.

---

## 7. LSTM Modeling

A Long Short-Term Memory neural network was used as the final deep learning model.

The LSTM was selected because the project uses time-series data and the model can learn patterns across sequences of previous trading days.

The final LSTM used:

- 10-day input sequences
- two LSTM layers
- dropout regularization
- batch normalization
- softmax output for three-class prediction

The model was trained using a time-based train/test split to avoid future data leakage.

---

## 8. Evaluation

The models were evaluated using:

- Accuracy
- Macro Precision
- Macro Recall
- Macro F1-score
- Confusion Matrix

Macro F1-score was used as the main comparison metric because the project predicts three classes and each class should contribute equally to the evaluation.

---

## 9. Signal Conversion

The final model outputs class probabilities for SELL, HOLD, and BUY.

These probabilities are converted into a readable prototype signal:

```text
Model probabilities
-> Highest probability class
-> SELL / HOLD / BUY signal
```

The final signal is intended as an academic decision-support prototype and should not be interpreted as real financial advice.

---

## 10. Limitations

The project has several limitations:

- only one insurance stock was used
- the dataset is relatively small for deep learning
- market reactions are affected by many non-earthquake factors
- news sentiment and macroeconomic indicators were not included
- the model predicts short-term direction, which is naturally noisy

Despite these limitations, the project demonstrates a complete seismic-financial prediction pipeline.
