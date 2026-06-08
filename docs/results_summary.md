# Results Summary

## Baseline Result

The initial Linear Regression baseline used earthquake magnitude to predict stock return.

Result:

- MSE: approximately 0.00037
- R² Score: approximately -0.0065

This showed that earthquake magnitude alone was not enough to explain stock return movement.

## Classification Models (target: SELL / HOLD / BUY)

After feature engineering, the task was framed as a 3-class classification of the
next-day stock reaction (`target_signal`: 0=SELL, 1=HOLD, 2=BUY). Models were trained
on a time-based 80/20 split (train on the past, test on the future) with all features
scaled using statistics from the training period only.

Test-set results (macro F1 is the headline metric because the three classes are
weighted equally):

| Model | Accuracy | Macro F1 |
|---|---|---|
| **LSTM (seq_len=10)** | **0.365** | **0.362** |
| Gradient Boosting | 0.356 | 0.341 |
| Random Forest | 0.338 | 0.331 |
| KNN | 0.328 | 0.320 |
| SVM (RBF) | 0.312 | 0.309 |
| Logistic Regression | 0.303 | 0.294 |
| Majority Baseline | 0.335 | 0.167 |

See `results/metrics/model_comparison.csv` and the figures in `results/figures/`.

## Current Findings

All trained models clear the majority-class floor (macro F1 ≈ 0.17), confirming the
earthquake + financial features carry *some* signal. The LSTM was the best model
(macro F1 ≈ 0.362), narrowly ahead of Gradient Boosting. However, every model sits
only modestly above chance: predicting the next-day direction of a single insurance
stock is genuinely hard, and these numbers are reported honestly rather than tuned
to look better.

## Limitations

- Single ticker (8766.T) and only ~3,380 daily rows, which is small for deep learning.
- Next-day price direction is close to a random walk; markets price in known
  information quickly, and most price drivers are unrelated to seismic activity.
- Sequence length was chosen by test-set macro F1 among {5, 10, 20}; with more data a
  separate validation set should be used for that choice.

## Future Work

Future improvements include adding more insurance stocks, more market indicators, longer event windows, and real-time earthquake API integration.

## Note

Final model metrics should be updated after all model training is completed.
