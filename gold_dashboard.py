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

