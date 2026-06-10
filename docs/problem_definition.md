# Problem Definition

## Project Title

**SeismoFinance: Predicting Market Reactions to Earthquakes**

---

## Problem Overview

Earthquakes are sudden external events that can create uncertainty in financial markets. In countries with high seismic activity, such as Japan, major earthquakes may influence investor expectations, insurance risk, and short-term stock price movement.

This project investigates whether earthquake-related features can help predict short-term reactions in Japanese insurance stock prices.

The project focuses on **Tokio Marine Holdings (`8766.T`)**, a major Japanese insurance company, because insurance firms may be financially exposed to natural disaster risk through claims, uncertainty, and perceived market risk.

---

## Research Question

Can earthquake-related data, combined with financial time-series indicators, be used to predict the next-day market reaction of a Japanese insurance stock?

More specifically, this project asks:

```text
Given recent earthquake activity and market behavior,
can a model predict whether the stock reaction will be SELL, HOLD, or BUY?
```

---

## Input Data

The model uses two main categories of input features:

### Earthquake Features

- earthquake magnitude
- earthquake depth
- earthquake location
- earthquake count
- earthquake energy estimates
- distance from major Japanese cities
- days since last earthquake
- rolling earthquake activity

### Financial Features

- stock return
- market return
- abnormal return
- lagged returns
- rolling returns
- volatility
- volume change

---

## Output

The final output is a three-class prediction:

```text
0 = SELL
1 = HOLD
2 = BUY
```

The prediction represents the expected next-day abnormal return direction.

The output is also converted into a readable prototype Buy/Hold/Sell signal.

---

## Why This Problem Matters

This problem is relevant because earthquake events may affect insurance companies through:

- expected future claims
- uncertainty about disaster losses
- investor risk perception
- short-term volatility in financial markets
- broader market reaction after major seismic events

A model that studies this relationship can be useful as an academic decision-support prototype for understanding how external shock events may interact with financial markets.

---

## Scope

This project is limited to:

- earthquake events in Japan
- one Japanese insurance stock: Tokio Marine Holdings (`8766.T`)
- one market index: Nikkei 225 (`^N225`)
- short-term next-day prediction
- three-class Buy/Hold/Sell classification

The project does not attempt to create a real trading system.

---

## Expected Outcome

The expected outcome is a complete machine learning pipeline that:

1. collects earthquake and financial market data
2. cleans and aligns the datasets by Japanese trading dates
3. creates earthquake and financial time-series features
4. trains baseline machine learning models
5. trains an LSTM time-series model
6. evaluates model performance
7. converts predictions into a readable Buy/Hold/Sell signal

---

## Important Note

This project is an academic decision-support prototype. It should not be interpreted as financial advice or used for real investment decisions.
