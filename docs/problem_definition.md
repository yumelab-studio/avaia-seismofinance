# Problem Definition

This project investigates whether earthquake events in Japan can help predict short-term reactions in Japanese insurance stock prices.

Earthquakes may affect insurance companies because they can increase expected claims, uncertainty, and perceived financial risk. The project combines earthquake data with stock market time-series data to build a model that predicts possible stock reaction.

## Input

The model uses earthquake-related and financial features, including:

- Magnitude
- Depth
- Location
- Earthquake count
- Stock return
- Stock volatility
- Market return

## Output

The output is a prototype Buy/Hold/Sell signal:

- SELL: expected negative market reaction
- HOLD: expected neutral market reaction
- BUY: expected positive market reaction

This is an academic decision-support prototype and not real financial advice.
