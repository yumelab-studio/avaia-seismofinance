# SeismoFinance: Predicting Market Reactions to Earthquakes

SeismoFinance is an AI project that investigates whether earthquake events in Japan can help predict short-term reactions in Japanese insurance stock prices.

The project combines earthquake data, stock market data, and market index data to build machine learning and deep learning models that estimate possible short-term stock reactions after seismic events.

The final system demonstrates a prototype Buy/Hold/Sell signal based on predicted market reaction.

> This project is an academic decision-support prototype and should not be interpreted as financial advice.

---

## Problem Definition

Earthquakes can affect insurance companies because they may increase expected claims, uncertainty, and perceived financial risk.

This project studies whether earthquake-related features can be used together with financial time-series features to predict short-term stock reactions of Japanese insurance companies.

### Input

The model uses features such as:

- Earthquake magnitude
- Earthquake depth
- Earthquake location
- Earthquake count
- Stock returns
- Stock volatility
- Market index return

### Output

The output is:

- A predicted market reaction
- A prototype Buy/Hold/Sell signal

---

## Project Objectives

The main objectives of this project are:

1. Collect and clean earthquake and financial data.
2. Align earthquake events with stock market trading days.
3. Create earthquake-based and financial time-series features.
4. Train baseline machine learning models.
5. Train and evaluate an LSTM model.
6. Convert model output into a readable Buy/Hold/Sell prototype signal.
7. Present the final pipeline through documentation, a demo notebook, and a poster.

---

## Data Sources

The project uses three main datasets:

- Earthquake data
- Japanese insurance stock data
- Japanese market index data

The raw datasets are stored in:

```text
data/raw/
