# StockScope — Intern Starter

## 🎯 Step 1: Get data from Yahoo Finance

**The only goal right now:** run `app.py` and see stock data printed in your terminal.
No UI, no charts. Just prove you can fetch data.

---

## Setup (do this once)

1. **Install Python 3.9+** if you don't have it: `python3 --version`
2. **Install the libraries:**
   ```bash
   cd intern_starter
   pip install -r requirements.txt
   ```
3. **Run the script:**
   ```bash
   python app.py
   ```
   You should see a table of Apple's last 5 days of prices. 🎉

---

## If it works — try these mini-tasks

Open `app.py` and complete the `TODO` comments. Each one is 1–3 lines.

### TODO 1.1 — Change the ticker
Change `"AAPL"` to another stock (try `"MSFT"`, `"TSLA"`, `"GOOGL"`). Run it again.

**Done when:** You see a different company's prices.

### TODO 1.2 — Print only the Close prices
A DataFrame has columns. Print just the closing prices.
```python
print(data["Close"])
```
**Done when:** You see one column of numbers instead of the full table.

### TODO 1.3 — Print just the latest close
How do you get the last row of a column?
```python
latest = data["Close"].iloc[-1]
print(f"Latest close: ${latest:.2f}")
```
**Done when:** You see something like `Latest close: $227.52`.

### TODO 1.4 — Try different time ranges
Change `period` and `interval` in the `history()` call.

Try:
- `period="1mo", interval="1d"` — last month, daily
- `period="1y", interval="1wk"` — last year, weekly
- `period="1d", interval="5m"` — today, every 5 minutes

**Done when:** You've tried 3 different combos and know what happens when an invalid combo is used (spoiler: it returns an empty table).

---

## 🛟 When you get stuck (read this before asking!)

1. **Copy the error message.** The first line usually tells you exactly what's wrong.
2. **Google it.** "ModuleNotFoundError: yfinance" → probably means you didn't run `pip install`.
3. **Try 30 minutes.** Then ping your mentor with:
   - What you were trying to do
   - What you tried
   - The exact error message

---

## ✅ When all 4 TODOs are done

Come back and we'll talk about **Step 2: turning this into a web page**.

Don't peek ahead — finish this step first. 😊
