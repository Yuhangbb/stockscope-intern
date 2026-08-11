import json
import os

import streamlit as st
import yfinance as yf

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
st.line_chart(data["Close"])