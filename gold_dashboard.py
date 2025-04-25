import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# Fetch data
@st.cache_data
def get_data():
    try:
        df = yf.download("GC=F", period="1mo", interval="1d")
        df = df[['Close']].rename(columns={'Close': 'Gold Price'})
        return df
    except:
        st.warning("⚠️ Could not fetch live data. Using sample data.")
        return pd.read_csv('sample_gold_data.csv')

df = get_data()

# Calculate simple moving average
def moving_average(data, period=5):
    return data.rolling(window=period).mean()

# RSI Calculation
def rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

# UI Layout
st.title("📈 Gold Price Tracker Dashboard")

st.subheader("🌍 Live Gold Price")
st.write(df.tail())

st.subheader("📊 Price Table")
st.dataframe(df.tail(10))

st.subheader("📉 Price Chart with Moving Average")
df['MA5'] = moving_average(df['Gold Price'], period=5)

fig, ax = plt.subplots()
df['Gold Price'].plot(ax=ax, label='Gold Price')
df['MA5'].plot(ax=ax, label='5-day MA')
ax.legend()
st.pyplot(fig)

st.subheader("🧠 RSI Indicator (14-period)")
df['RSI'] = rsi(df['Gold Price'], period=14)
st.line_chart(df['RSI'])

st.caption("Built by dolkar11 ✨")

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

import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Gold, Forex & Stock Tracker", layout="wide")  # ✅ MUST be first

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
        st.warning("⚠️ No data returned. Try another symbol, or check your internet.")
    else:
        # ✅ Continue with plotting and metrics
        latest_price = data["Close"].iloc[-1]
        st.metric(label="Current Price", value=f"${latest_price:.2f}")
        ...
except Exception as e:
    st.error(f"❌ Error loading data: {e}")


    if not data.empty:
        # --- Live Price ---
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
        st.warning("No data available. Try again later or select a different symbol.")

except Exception as e:


