# Future Work

## Overview

This project demonstrates a complete seismic-financial prediction pipeline, but several improvements could make the model more realistic, more accurate, and more useful in future research.

---

## 1. Include More Insurance Companies

The current project focuses on Tokio Marine Holdings (`8766.T`).

Future versions could include more Japanese insurance companies, such as:

- MS&AD Insurance Group Holdings
- Sompo Holdings
- other listed financial or insurance firms exposed to natural disaster risk

Using multiple companies would allow the model to compare whether earthquake events affect insurance firms differently.

---

## 2. Add More Market Indicators

The current model uses stock return, market return, abnormal return, volatility, and volume-based features.

Future work could include additional financial indicators, such as:

- TOPIX index movement
- interest rates
- exchange rates
- sector index data
- global market indicators
- bond market indicators

These features could help separate earthquake-specific effects from broader market movement.

---

## 3. Add News and Sentiment Data

Stock reactions are strongly affected by public information and investor sentiment.

Future versions could include:

- earthquake news headlines
- financial news articles
- social media sentiment
- insurance claim reports
- government disaster announcements

Natural language processing could be used to convert text data into sentiment features.

---

## 4. Improve Earthquake Impact Features

The current project uses earthquake magnitude, depth, location, energy estimates, and distance-based features.

Future work could improve seismic impact representation by adding:

- tsunami warnings
- earthquake intensity data
- affected population estimates
- distance to insured regions
- building damage estimates
- economic loss estimates
- aftershock sequences

These features may better represent the actual financial risk faced by insurance companies.

---

## 5. Test Different Prediction Horizons

The current project focuses on next-day reaction.

Future versions could test different time horizons:

- same-day reaction
- next-day reaction
- three-day reaction
- one-week reaction
- cumulative abnormal return after major events

This would help determine whether earthquake-related market effects appear immediately or over several trading days.

---

## 6. Improve Deep Learning Models

The LSTM achieved the best performance in this project, but the prediction task remains difficult.

Future work could test more advanced models, such as:

- GRU networks
- Bidirectional LSTM models
- Temporal Convolutional Networks
- Transformer-based time-series models
- hybrid models combining tree-based methods and neural networks

These models may capture more complex temporal relationships.

---

## 7. Expand the Dataset

Deep learning models usually require larger datasets.

Future improvements could include:

- longer historical periods
- multiple earthquake-prone countries
- multiple stock markets
- more companies
- additional macroeconomic variables

A larger dataset could improve generalization and reduce overfitting.

---

## 8. Build a Real-Time Prototype

A future version could connect directly to live APIs.

Possible real-time inputs:

- USGS earthquake feed
- Yahoo Finance or other market APIs
- live news feeds
- disaster warning feeds

This could produce a real-time academic dashboard showing predicted Buy/Hold/Sell signals after new earthquake events.

---

## 9. Improve Interpretability

Future work could include interpretability methods to better understand model behavior.

Possible methods:

- feature importance analysis
- SHAP values
- permutation importance
- attention mechanisms
- event-level case studies

This would help explain which earthquake or financial features contribute most to each prediction.

---

## Final Note

The current project should be viewed as a first academic prototype. It shows that seismic and financial data can be combined into a structured machine learning pipeline, but stronger performance would require richer data, broader market coverage, and more advanced modeling.
