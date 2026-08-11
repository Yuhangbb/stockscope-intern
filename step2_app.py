import json
import os
from datetime import datetime

import streamlit as st
import yfinance as yf
from streamlit_autorefresh import st_autorefresh

WATCHLIST_FILE = "watchlist.json"

def load_watchlist():
    if os.path.exists(WATCHLIST_FILE):
        with open(WATCHLIST_FILE, "r") as f:
            return json.load(f)
    return ["MSFT", "AAPL", "TSLA"]

def save_watchlist(watchlist):
    with open(WATCHLIST_FILE, "w") as f:
        json.dump(watchlist, f)

if "watchlist" not in st.session_state:
    st.session_state.watchlist = load_watchlist()

st.sidebar.title("Watchlist")

selected_watchlist = st.sidebar.selectbox(
    "Select Stock",
    st.session_state.watchlist
)

search_ticker = st.sidebar.text_input("Search Ticker")

if search_ticker:
    search_results = yf.Search(search_ticker, max_results=5).quotes

    search_options = []

    for result in search_results:
        symbol = result.get("symbol", "")
        name = result.get("shortname", result.get("longname", ""))

        if symbol:
            search_options.append(f"{symbol} — {name}")

    if search_options:
        selected_result = st.sidebar.selectbox(
            "Search Results",
            search_options
        )

        selected_symbol = selected_result.split(" — ")[0]

        if st.sidebar.button("Add Search Result"):
            if selected_symbol not in st.session_state.watchlist:
                st.session_state.watchlist.append(selected_symbol)
                save_watchlist(st.session_state.watchlist)
                st.rerun()
new_ticker = st.sidebar.text_input("Add Stock").upper()
if st.sidebar.button("Add"):
    if new_ticker and new_ticker not in st.session_state.watchlist:
        st.session_state.watchlist.append(new_ticker)
        save_watchlist(st.session_state.watchlist)
        st.rerun()

if st.sidebar.button("Remove"):
    if selected_watchlist in st.session_state.watchlist and len(st.session_state.watchlist) > 1:
        st.session_state.watchlist.remove(selected_watchlist)
        save_watchlist(st.session_state.watchlist)
        st.rerun()

st.title("📈 My First Stock Page")
st.write("Hello! This page shows stock prices.")

from datetime import datetime

live_mode = st.checkbox("Live Mode")

if live_mode:
    st_autorefresh(interval=30000, key="live_refresh")
    st.write("Last refresh:", datetime.now().strftime("%H:%M:%S"))


ticker = st.text_input("Ticker", value=selected_watchlist).upper()

timeframes = {
    "1D": ("1d", "5m"),
    "1W": ("5d", "30m"),
    "1M": ("1mo", "1d"),
    "3M": ("3mo", "1d"),
    "1Y": ("1y", "1d"),
    "5Y": ("5y", "1wk"),
    "ALL": ("max", "1mo"),
}

selected_range = st.selectbox("Range", list(timeframes.keys()))
period, interval = timeframes[selected_range]
stock = yf.Ticker(ticker)
data = stock.history(period=period, interval=interval)

data["MA20"] = data["Close"].rolling(window=20).mean()
data["MA50"] = data["Close"].rolling(window=50).mean()

show_ma20 = st.checkbox("Show MA20")
show_ma50 = st.checkbox("Show MA50")
show_volume = st.checkbox("Show Volume")
compare_mode = st.checkbox("Compare Mode")

compare_tickers = []

if compare_mode:
    compare_tickers = st.multiselect(
        "Compare Tickers",
        st.session_state.watchlist,
        default=st.session_state.watchlist[:2],
        max_selections=6
    )

st.subheader(f"Stock: {ticker}")
st.dataframe(data)

latest = data["Close"].iloc[-1]

first_close = data["Close"].iloc[0]
change = latest - first_close
change_pct = (change / first_close) * 100

period_high = data["High"].max()
period_low = data["Low"].min()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Latest Close",
        f"${latest:.2f}",
        f"{change:+.2f} ({change_pct:+.2f}%)"
    )

with col2:
    st.metric("Period High", f"${period_high:.2f}")

with col3:
    st.metric("Period Low", f"${period_low:.2f}")
chart_data = data[["Close"]].copy()

if show_ma20:
    chart_data["MA20"] = data["MA20"]

if show_ma50:
    chart_data["MA50"] = data["MA50"]

st.line_chart(chart_data)

if show_volume:
    st.subheader("Volume")
    st.bar_chart(data["Volume"])

if compare_mode and len(compare_tickers) >= 2:
    compare_data = {}

    for symbol in compare_tickers:
        compare_stock = yf.Ticker(symbol)
        compare_history = compare_stock.history(
            period=period,
            interval=interval
        )

        if not compare_history.empty:
            close = compare_history["Close"]
            normalized = (close / close.iloc[0] - 1) * 100
            compare_data[symbol] = normalized

    if compare_data:
        st.subheader("Normalized Return Comparison (%)")
        st.line_chart(compare_data)