# StockScope



StockScope is a lightweight stock analytics web application built with Python and Streamlit.



## Features

- Search stocks using Yahoo Finance
- Add and remove stocks from a personal watchlist
- Persistent watchlist using JSON
- View stock prices across multiple timeframes:
  - 1D
  - 1W
  - 1M
  - 3M
  - 1Y
  - 5Y
  - ALL
- View latest close, period high, and period low
- Color-coded price changes
- Toggle MA20 and MA50 moving averages
- Toggle volume chart
- Compare 2–6 stocks using normalized percentage returns
- Optional live auto-refresh mode
- Transformer-based stock forecasting
- Forecast horizon from 5 to 30 trading days
- Adjustable lookback window and training epochs
- Predicted future price path with forecast bands
- Model quality metrics including training loss and validation MAE
- Cached forecast results to avoid unnecessary retraining

## Technologies

- Python
- Streamlit
- yfinance
- pandas
- Plotly
- PyTorch
- streamlit-autorefresh

## Installation

Clone or download the project, then install the required packages:

```bash
pip install -r requirements.txt
```
## Usage

1. Enter or select a stock ticker.
2. Choose a timeframe.
3. View price data and summary statistics.
4. Enable MA20, MA50, or Volume if needed.
5. Use Compare Mode to compare multiple stocks.
6. Use the sidebar to manage the watchlist.
7. Open Prediction Lab in the sidebar.
8. Enable Transformer Forecast.
9. Choose the forecast days, lookback window, and training epochs.
10. View the forecast line, forecast band, and model metrics on the page.

## Forecasting Note

The Transformer forecasting feature is designed for learning and product exploration. It is not financial advice, and the predicted prices should not be treated as reliable investment signals.

