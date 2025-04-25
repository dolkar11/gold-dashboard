import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# ✅ MUST be the very first Streamlit command
st.set_page_config(page_title="Gold, Forex & Stock Tracker", layout="wide")

# --- App Header ---
st.title("📈 Gold, Forex & Stock Tracker Dashboard")
st.caption("Built by dolkar11 ✨")

# --- Market Type Selection ---
market_type = st.selectbox("Select Market", ["Gold", "Forex", "Stocks"])

# --- Choose Symbol ---
if market_type == "Gold":
    symbol = "XAUUSD=X"
elif market_type == "Forex":
    forex_pairs = {
        "EUR/USD": "EURUSD=X",
        "GBP/USD": "GBPUSD=X",
        "USD/JPY": "JPY=X",
        "AUD/USD": "AUDUSD=X"
    }
    selected_forex = st.selectbox("Select Forex Pair", list(forex_pairs.keys()))
    symbol = forex_pairs[selected_forex]
else:  # Stocks
    stock_list = {
        "Apple (AAPL)": "AAPL",
        "Tesla (TSLA)": "TSLA",
        "Microsoft (MSFT)": "MSFT",
        "Nvidia (NVDA)": "NVDA"
    }
    selected_stock = st.selectbox("Select Stock", list(stock_list.keys()))
    symbol = stock_list[selected_stock]

# --- Moving Average Inputs ---
st.subheader("📉 Price Chart with Moving Averages")
col1, col2 = st.columns(2)
with col1:
    sma_window = st.slider("SMA Window", min_value=5, max_value=50, value=20)
with col2:
    ema_window = st.slider("EMA Window", min_value=5, max_value=50, value=20)

# --- Fetch Data ---
try:
    ticker = yf.Ticker(symbol)
    data = ticker.history(period="1d", interval="1m")

    if data.empty:
        st.warning("⚠️ No data available to plot. Please check your internet or try a different symbol.")
    else:
        # --- Current Price ---
        current_price = data["Close"].iloc[-1]
        st.subheader(f"🔴 Live Price for {symbol}")
        st.metric("Current Price", f"${current_price:.2f}")

        # --- Add Moving Averages ---
        data[f"SMA_{sma_window}"] = data["Close"].rolling(window=sma_window).mean()
        data[f"EMA_{ema_window}"] = data["Close"].ewm(span=ema_window, adjust=False).mean()

        # --- Plot ---
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(data.index, data["Close"], label="Price", color="blue")
        ax.plot(data.index, data[f"SMA_{sma_window}"], label=f"SMA {sma_window}", linestyle="--", color="orange")
        ax.plot(data.index, data[f"EMA_{ema_window}"], label=f"EMA {ema_window}", linestyle="--", color="green")
        ax.set_title(f"{symbol} - Intraday Price Chart")
        ax.set_xlabel("Time")
        ax.set_ylabel("Price")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

except Exception as e:
    st.error(f"❌ Error loading data: {e}")

