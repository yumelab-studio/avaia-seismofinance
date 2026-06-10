# Model Architecture and Optimization

## Overview

This project compares traditional machine learning models with a deep learning time-series model to predict short-term market reactions after earthquake-related events.

The final prediction task is formulated as a three-class classification problem:

- `0 = SELL`
- `1 = HOLD`
- `2 = BUY`

The target represents the expected next-day abnormal return direction for Tokio Marine Holdings (`8766.T`), a major Japanese insurance company.

---

## Baseline Models

Several baseline machine learning models were trained and compared before building the final LSTM model:

- Majority Class Baseline
- Logistic Regression
- Support Vector Machine with RBF kernel
- K-Nearest Neighbors
- Random Forest
- Gradient Boosting

The purpose of these baselines was to determine whether the deep learning model improves over simpler models and to avoid evaluating the LSTM in isolation.

The best traditional baseline was **Gradient Boosting**, with a macro F1-score of approximately **0.3408**.

---

## Final LSTM Model

The final model is a Long Short-Term Memory neural network designed to capture temporal patterns in the engineered earthquake and financial features.

The model uses sliding windows of historical trading days. The best sequence length selected during experimentation was:

```text
10 trading days
```

This means the model uses the previous 10 trading days of features to predict the next Buy/Hold/Sell signal.

---

## LSTM Architecture

The final LSTM architecture is:

```text
Input sequence
-> LSTM layer with 64 units
-> Dropout layer
-> LSTM layer with 32 units
-> Dropout layer
-> Dense layer with 32 units and ReLU activation
-> Batch Normalization
-> Dropout layer
-> Dense output layer with 3 units and Softmax activation
```

The output layer produces probabilities for the three possible classes:

```text
SELL, HOLD, BUY
```

---

## Optimization Strategy

Several optimization choices were used to improve model reliability:

### Time-Based Train/Test Split

The dataset was sorted chronologically and split using an 80/20 time-based split. This prevents future information from leaking into the training set.

### Feature Scaling

Features were scaled using `StandardScaler`. The scaler was fitted only on the training data and then applied to the test data.

### Sequence Length Tuning

The LSTM was tested with multiple sequence lengths. The best result was achieved with a sequence length of 10 trading days.

### Class Weights

Class weights were used to reduce the effect of class imbalance and help the model treat SELL, HOLD, and BUY more fairly.

### Early Stopping

Early stopping was used to stop training once validation performance stopped improving.

### Learning Rate Reduction

`ReduceLROnPlateau` was used to reduce the learning rate when validation loss stopped improving.

---

## Evaluation Metrics

The main evaluation metric was **macro F1-score**.

Macro F1 was selected because the task has three classes and the model should not be evaluated only by accuracy. Macro F1 gives equal importance to SELL, HOLD, and BUY performance.

The model was also evaluated using:

- Accuracy
- Macro Precision
- Macro Recall
- Confusion Matrix

---

## Final Results

The LSTM achieved the best overall performance among all tested models.

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

The LSTM achieved the highest macro F1-score, which suggests that temporal feature sequences helped improve prediction performance compared to traditional baseline models.

However, the overall scores remain modest. This is expected because short-term stock movement prediction is highly noisy and affected by many external factors beyond earthquake activity, such as investor sentiment, global market conditions, macroeconomic events, and company-specific news.

The final model should therefore be interpreted as an academic decision-support prototype, not as a real financial trading system.
