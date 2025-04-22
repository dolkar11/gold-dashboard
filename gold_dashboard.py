import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import pandas_ta as ta
from datetime import datetime, timedelta

st.set_page_config(page_title="Gold Price Tracker", layout="wide")

st.title("📈 Gold Price Tracker Dashboard")

# Try to fetch gold price from Yahoo Finance
symbol = "GC=F"  # Gold Futures
end_date = datetime.today()
start_date = end_date - timedelta(days=60)

try:
    data = yf.download(symbol, start=start_date, end=end_date)
    df = pd.DataFrame(data)[['Close']].rename(columns={'Close': 'Gold Price'})
    st.success("✅ Live gold price data loaded.")
except Exception:
    st.warning("⚠️ Could not fetch live data. Using sample data.")
    df = pd.DataFrame({
        "Gold Price": [1920, 1930, 1915, 1945, 1955, 1935, 1925]
    })

# Moving average
df["MA_5"] = df["Gold Price"].rolling(window=5).mean()

# Clean the data for RSI calculation
gold_prices = pd.to_numeric(df["Gold Price"], errors='coerce').dropna()
rsi_series = ta.rsi(gold_prices, length=5)
df["RSI"] = rsi_series.reindex(df.index).fillna(0)

# Price Table
st.subheader("📊 Price Table")
st.dataframe(df.tail(10), use_container_width=True)

# Chart
st.subheader("📈 Price Chart with Moving Average")
fig, ax = plt.subplots()
df["Gold Price"].plot(ax=ax, label="Gold Price", color='gold')
df["MA_5"].plot(ax=ax, label="MA (5)", linestyle='--', color='orange')
ax.set_title("Gold Price vs MA (5)")
ax.set_ylabel("Price (USD)")
ax.legend()
st.pyplot(fig)

# RSI Chart
st.subheader("🧠 RSI Indicator (5-period)")
fig2, ax2 = plt.subplots()
df["RSI"].plot(ax=ax2, color='purple')
ax2.axhline(70, color='red', linestyle='--', label="Overbought")
ax2.axhline(30, color='green', linestyle='--', label="Oversold")
ax2.set_title("Relative Strength Index (RSI)")
ax2.set_ylabel("RSI")
ax2.set_ylim([0, 100])
ax2.legend()
st.pyplot(fig2)
