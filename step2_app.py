import streamlit as st
import yfinance as yf


st.title("📈 My First Stock Page")
st.write("Hello! This page shows stock prices.")


# TODO 2.1
ticker = st.text_input("Ticker", value="MSFT").upper()

period = st.selectbox("Range", ["5d", "1mo", "3mo", "1y"])

stock = yf.Ticker(ticker)
data = stock.history(period=period, interval="1d")

st.subheader(f"Stock: {ticker}")
st.dataframe(data)

latest = data["Close"].iloc[-1]
st.metric("Latest Close", f"${latest:.2f}")

st.line_chart(data["Close"])

# TODO 2.2
# latest = data["Close"].iloc[-1]
# st.metric("Latest Close", f"${latest:.2f}")


# TODO 2.3
# ticker = st.text_input("Ticker", value="AAPL").upper()


# TODO 2.4
# st.line_chart(data["Close"])


# TODO 2.5 (bonus)
# period = st.selectbox("Range", ["5d", "1mo", "3mo", "1y"])