import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.title("📈 Gold, Forex & Stock Tracker Dashboard")
st.caption("Built by dolkar11 ✨")

# --- Select Market Type ---
market_type = st.selectbox("Select Market", ["Gold", "Forex", "Stocks"])

# --- Symbol Selection ---
if market_type == "Gold":
    symbol = "XAUUSD=X"
elif market_type == "Forex":
    forex_symbols = {
        "EUR/USD": "EURUSD=X",
        "GBP/USD": "GBPUSD=X",
        "USD/JPY": "JPY=X",
        "AUD/USD": "AUDUSD=X"
    }
    selected_forex = st.selectbox("Select Forex Pair", list(forex_symbols.keys()))
    symbol = forex_symbols[selected_forex]
elif market_type == "Stocks":
    stock_symbols = {
        "Apple (AAPL)": "AAPL",
        "Tesla (TSLA)": "TSLA",
        "Microsoft (MSFT)": "MSFT",
        "Nvidia (NVDA)": "NVDA"
    }
    selected_stock = st.selectbox("Select Stock", list(stock_symbols.keys()))
    symbol = stock_symbols[selected_stock]

# --- SMA & EMA sliders ---
st.subheader("📉 Price Chart with Moving Averages")
sma_window = st.slider("SMA Window", min_value=5, max_value=50, value=20)
ema_window = st.slider("EMA Window", min_value=5, max_value=50, value=20)

# --- Fetch Data ---
ticker = yf.Ticker(symbol)
data = ticker.history(period="1d", interval="1m")

# --- Show Live Price ---
if not data.empty:
    latest_price = data["Close"].iloc[-1]
    st.subheader(f"🔴 Live Price for {symbol}")
    st.metric(label="Current Price", value=f"${latest_price:.2f}")

    # --- Calculate MAs ---
    data[f"SMA_{sma_window}"] = data["Close"].rolling(window=sma_window).mean()
    data[f"EMA_{ema_window}"] = data["Close"].ewm(span=ema_window, adjust=False).mean()

    # --- Plot Chart ---
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(data.index, data["Close"], label="Price", color="blue")
    ax.plot(data.index, data[f"SMA_{sma_window}"], label=f"SMA {sma_window}", color="orange", linestyle="--")
    ax.plot(data.index, data[f"EMA_{ema_window}"], label=f"EMA {ema_window}", color="green", linestyle="--")
    ax.set_title(f"{symbol} Price Chart with Moving Averages")
    ax.set_xlabel("Time")
    ax.set_ylabel("Price")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

else:
    st.warning("No data available to plot. Please check your internet or try a different symbol.")
