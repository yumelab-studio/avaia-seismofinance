# Results Summary

## Overview

This project evaluated whether earthquake-related features, combined with financial time-series indicators, can help predict short-term market reactions in Japanese insurance stock prices.

The final prediction task was formulated as a three-class classification problem:

```text
0 = SELL
1 = HOLD
2 = BUY
```

The target represents the expected next-day abnormal return direction for Tokio Marine Holdings (`8766.T`).

---

## Dataset Summary

The final processed dataset was created by combining:

- earthquake data from the USGS Earthquake Catalog
- Tokio Marine Holdings stock data from Yahoo Finance
- Nikkei 225 market index data from Yahoo Finance

The final model dataset contains engineered earthquake and financial features, including:

- earthquake count features
- maximum and average earthquake magnitude
- average and minimum earthquake depth
- earthquake energy features
- distance-based features
- stock return
- market return
- abnormal return
- lagged returns
- rolling returns
- volatility features
- volume change

After preprocessing and removing rows with missing values, the final modeling dataset contained approximately **3,382 usable rows**.

---

## Target Label Distribution

The target classes were reasonably balanced:

| Class | Meaning | Count | Percentage |
|---|---|---:|---:|
| 0 | SELL | 1,206 | 35.6% |
| 1 | HOLD | 1,046 | 30.9% |
| 2 | BUY | 1,137 | 33.5% |

This balance allowed the project to evaluate all three classes more fairly, instead of relying only on accuracy.

---

## Baseline Model Results

Several traditional machine learning models were trained before the LSTM model.

| Model | Accuracy | Macro Precision | Macro Recall | Macro F1 |
|---|---:|---:|---:|---:|
| Gradient Boosting | 0.3560 | 0.3572 | 0.3516 | 0.3408 |
| Random Forest | 0.3383 | 0.3316 | 0.3347 | 0.3314 |
| KNN | 0.3279 | 0.3244 | 0.3258 | 0.3200 |
| SVM (RBF) | 0.3117 | 0.3094 | 0.3099 | 0.3095 |
| Logistic Regression | 0.3028 | 0.2959 | 0.3007 | 0.2942 |
| Majority Baseline | 0.3353 | 0.1118 | 0.3333 | 0.1674 |

The strongest traditional baseline was **Gradient Boosting**, with a macro F1-score of **0.3408**.

---

## LSTM Model Results

The final LSTM model used a sequence length of **10 trading days**.

| Metric | Value |
|---|---:|
| Accuracy | 0.3653 |
| Macro Precision | 0.3641 |
| Macro Recall | 0.3653 |
| Macro F1 | 0.3622 |
| Sequence Length | 10 |

The LSTM achieved the best macro F1-score among all tested models.

---

## Final Model Comparison

| Model | Accuracy | Macro Precision | Macro Recall | Macro F1 |
|---|---:|---:|---:|---:|
| LSTM | 0.3653 | 0.3641 | 0.3653 | 0.3622 |
| Gradient Boosting | 0.3560 | 0.3572 | 0.3516 | 0.3408 |
| Random Forest | 0.3383 | 0.3316 | 0.3347 | 0.3314 |
| KNN | 0.3279 | 0.3244 | 0.3258 | 0.3200 |
| SVM (RBF) | 0.3117 | 0.3094 | 0.3099 | 0.3095 |
| Logistic Regression | 0.3028 | 0.2959 | 0.3007 | 0.2942 |
| Majority Baseline | 0.3353 | 0.1118 | 0.3333 | 0.1674 |

---

## Interpretation

The LSTM model produced the best overall result, outperforming the strongest traditional baseline by macro F1-score.

However, the improvement was modest. This reflects the difficulty of predicting short-term financial market reactions, especially using earthquake and market data alone. Stock prices are influenced by many additional factors, including investor sentiment, macroeconomic conditions, company-specific news, global market movement, and uncertainty after major events.

The results suggest that earthquake-related features may provide some useful information, but they are not sufficient on their own to produce highly accurate short-term trading predictions.

---

## Final Prototype Output

The final demo notebook converts LSTM class probabilities into a readable Buy/Hold/Sell signal.

Example output from the final demo:

```text
Predicted signal after 2023-12-27: BUY
SELL probability: 30.68%
HOLD probability: 27.86%
BUY probability: 41.45%
Final prototype signal: BUY
```

This output should be interpreted as an academic decision-support prototype, not as financial advice.

---

## Main Conclusion

The project successfully built a complete pipeline for seismic-financial prediction:

```text
Earthquake data
-> Financial market data
-> Data cleaning
-> Feature engineering
-> Baseline models
-> LSTM model
-> Buy/Hold/Sell decision-support signal
```

The final LSTM model achieved the best performance among the tested models, but the modest scores show that this is a challenging prediction problem. Future improvements would require richer data sources, more insurance companies, additional market indicators, and possibly news or sentiment data.
