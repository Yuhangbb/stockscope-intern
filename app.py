"""
Step 1: Get stock data from Yahoo Finance.

Goal: run this file and see Apple's recent stock prices in your terminal.

How to run:
    pip install -r requirements.txt
    python app.py
"""

import yfinance as yf


ticker = "MSFT"

# Create a Ticker object — this is how yfinance talks to Yahoo
stock = yf.Ticker(ticker)

# Fetch the last 5 days of daily prices.
# history() returns a pandas DataFrame (think: a table).
data = stock.history(period="5d", interval="1d")

# Print the whole table
print(f"--- {ticker} last 5 days ---")
print(data)

print("\n--- Close prices only ---")
print(data["Close"])

latest_close = data["Close"].iloc[-1]
print(f"\nLatest close: ${latest_close:.2f}")

print("\n--- Different period and interval tests ---")

tests = [
    ("1mo", "1d"),
    ("1y", "1wk"),
    ("1d", "5m"),
    ("1y", "1m"),
]

for period, interval in tests:
    test_data = stock.history(period=period, interval=interval)

    print(f"\nPeriod: {period}, Interval: {interval}")
    print(test_data)

#   Hint: data["Close"]

#   Hint: data["Close"].iloc[-1]

#   period options:   1d, 5d, 1mo, 3mo, 1y, 5y, max
#   interval options: 5m, 30m, 1h, 1d, 1wk, 1mo
#   (some combinations don't work — find out which!)
