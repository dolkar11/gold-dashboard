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

# 🇰🇭 Cambodian Gold Market Analysis
st.markdown("## 🇰🇭 Cambodian Gold Market")

# Load Cambodian gold data from Google Sheets
@st.cache_data(ttl=3600)
def load_cambodia_gold_data():
    url = "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/export?format=csv"
    return pd.read_csv(url)

try:
    cambodia_gold_df = load_cambodia_gold_data()

    # Clean/format
    cambodia_gold_df["Date"] = pd.to_datetime(cambodia_gold_df["Date"])
    cambodia_gold_df = cambodia_gold_df.sort_values("Date")

    # Add moving average
    cambodia_gold_df["MA7"] = cambodia_gold_df["Price"].rolling(window=7).mean()

    # Display
    st.dataframe(cambodia_gold_df.tail(10), use_container_width=True)

    st.line_chart(cambodia_gold_df.set_index("Date")[["Price", "MA7"]])

except Exception as e:
    st.error("⚠️ Failed to load Cambodian gold data.")
    st.code(str(e))

import ta

# RSI Calculation
cambodia_gold_df["RSI"] = ta.momentum.RSIIndicator(cambodia_gold_df["Price"], window=14).rsi()

st.line_chart(cambodia_gold_df.set_index("Date")[["RSI"]])


