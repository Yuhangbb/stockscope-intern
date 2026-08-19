import json
import os
from datetime import datetime

import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh
from transformer_forecast import forecast_prices

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

st.sidebar.divider()
st.sidebar.subheader("Prediction Lab")

forecast_enabled = st.sidebar.checkbox("Enable Transformer Forecast")

forecast_days = st.sidebar.slider(
    "Forecast Days",
    min_value=5,
    max_value=30,
    value=10
)

lookback_window = st.sidebar.slider(
    "Lookback Window",
    min_value=10,
    max_value=60,
    value=20
)

training_epochs = st.sidebar.slider(
    "Training Epochs",
    min_value=5,
    max_value=100,
    value=20
)

st.title("📈 My First Stock Page")
st.write("Hello! This page shows stock prices.")

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
@st.cache_data(ttl=30)
def fetch_stock_data(ticker, period, interval):
    stock = yf.Ticker(ticker)
    return stock.history(period=period, interval=interval)

data = fetch_stock_data(ticker, period, interval)

if data.empty:
    st.error(f"No data found for {ticker}. Please check the ticker symbol.")
    st.stop()

@st.cache_data
def get_forecast(close_prices, forecast_days, lookback_window, training_epochs):
    return forecast_prices(
        close_prices,
        forecast_days=forecast_days,
        lookback=lookback_window,
        epochs=training_epochs
    )


forecast_df = None
forecast_metrics = None

if forecast_enabled:
    try:
        forecast_df, forecast_metrics = get_forecast(
            data["Close"].values,
            forecast_days,
            lookback_window,
            training_epochs
        )
    except ValueError as e:
        st.warning(str(e))
data["MA20"] = data["Close"].rolling(window=20).mean()
data["MA50"] = data["Close"].rolling(window=50).mean()
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
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=data.index,
        y=data["Close"],
        mode="lines",
        name="Close"
    )
)

if forecast_enabled and forecast_df is not None:
    future_dates = pd.bdate_range(
        start=data.index[-1] + pd.Timedelta(days=1),
        periods=len(forecast_df)
    )

    fig.add_trace(
        go.Scatter(
            x=future_dates,
            y=forecast_df["Upper Band"],
            mode="lines",
            line=dict(width=0),
            showlegend=False
        )
    )

    fig.add_trace(
        go.Scatter(
            x=future_dates,
            y=forecast_df["Lower Band"],
            mode="lines",
            line=dict(width=0),
            fill="tonexty",
            name="Forecast Band"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=future_dates,
            y=forecast_df["Predicted Close"],
            mode="lines",
            name="Forecast",
            line=dict(dash="dash")
        )
    )

if show_ma20:
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["MA20"],
            mode="lines",
            name="MA20"
        )
    )

if show_ma50:
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["MA50"],
            mode="lines",
            name="MA50"
        )
    )

fig.update_layout(
    title=f"{ticker} Price Chart",
    xaxis_title="Time",
    yaxis_title="Price",
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

if forecast_enabled and forecast_metrics is not None:
    final_predicted_price = forecast_metrics["final_predicted_price"]
    implied_change = (
        (final_predicted_price / latest) - 1
    ) * 100

    metric1, metric2, metric3, metric4, metric5 = st.columns(5)

    with metric1:
        st.metric(
            "Final Predicted Price",
            f"${final_predicted_price:.2f}"
        )

    with metric2:
        st.metric(
            "Implied Change",
            f"{implied_change:+.2f}%"
        )

    with metric3:
        st.metric(
            "Training Samples",
            forecast_metrics["training_samples"]
        )

    with metric4:
        st.metric(
            "Training Loss",
            f"{forecast_metrics['training_loss']:.6f}"
        )

    with metric5:
        validation_mae = forecast_metrics["validation_mae"]

        if validation_mae is not None:
            st.metric(
                "Validation MAE",
                f"{validation_mae:.6f}"
            )
        else:
            st.metric(
                "Validation MAE",
                "N/A"
            )

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

        compare_fig = go.Figure()

        for symbol, series in compare_data.items():
            compare_fig.add_trace(
                go.Scatter(
                    x=series.index,
                    y=series,
                    mode="lines",
                    name=symbol
                )
            )

        compare_fig.update_layout(
            xaxis_title="Time",
            yaxis_title="Return (%)",
            hovermode="x unified"
        )

        st.plotly_chart(compare_fig, use_container_width=True)