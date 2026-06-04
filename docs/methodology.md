# Methodology
## 1. Data Collection

Earthquake data, insurance stock data, and market index data were collected from external sources.

## 2. Data Cleaning

Dates, missing values, duplicates, and unnecessary columns were handled. The cleaned datasets were saved in the `data/clean/` folder.

## 3. Feature Engineering

Earthquake events were converted into trading-day features. Financial indicators such as lagged returns, volatility, and market index return were added.

## 4. Target Creation

Stock market reaction was converted into Buy/Hold/Sell labels.

Possible label interpretation:

- SELL: negative return beyond threshold
- HOLD: return close to neutral
- BUY: positive return beyond threshold

## 5. Model Training

Baseline machine learning models and an LSTM model were trained and compared.

## 6. Evaluation

The models were evaluated using metrics such as:

- Accuracy
- Precision
- Recall
- Macro F1-score
- Confusion matrix
- MSE
- R² score

## 7. Signal Conversion

The final model output is converted into a readable prototype Buy/Hold/Sell signal using helper functions in:

```text
src/signals.py
