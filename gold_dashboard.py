import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
from datetime import datetime
import pandas_ta as ta

st.title("📈 Gold Price Tracker Dashboard")

# 🔐 Your Twelve Data API key here
API_KEY = "your_api_key_here"

# 👉 Function to get live gold price
def get_gold_price():
    url = f"https://api.twelvedata.com/price?symbol=XAU/USD&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    return float(data["price"])

# 📡 Display current gold price
st.subheader("🌍 Live Gold Price")
try:
    price = get_gold_price()
    st.metric("Current Price (XAU/USD)", f"${price:,.2f}")
except:
    st.warning("⚠️ Could not fetch live data. Using sample data.")
    price = 2380  # fallback

# 🧪 Historical simulated data (can be replaced later)
data = {
    'Date': pd.date_range(end=datetime.today(), periods=10).tolist(),
    'Gold Price': [2320, 2330, 2310, 2340, 2355, 2370, 2365, 2380, 2375, price]
}
df = pd.DataFrame(data)

# 📊 Show price table
st.subheader("📊 Price Table")
st.dataframe(df)

# 🧠 Moving Average
df['MA_3'] = df['Gold Price'].rolling(3).mean()

# 📉 Plot price + MA
st.subheader("📈 Price Chart with Moving Average")
fig, ax = plt.subplots()
ax.plot(df['Date'], df['Gold Price'], label='Gold Price')
ax.plot(df['Date'], df['MA_3'], label='3-Day MA', linestyle='--')
ax.legend()
st.pyplot(fig)

# 📉 RSI Indicator
st.subheader("🧠 RSI Indicator (5-period)")
df['RSI'] = ta.rsi(df['Gold Price'], length=5)
fig2, ax2 = plt.subplots()
ax2.plot(df['Date'], df['RSI'], label='RSI', color='purple')
ax2.axhline(70, color='red', linestyle='--', label='Overbought')
ax2.axhline(30, color='green', linestyle='--', label='Oversold')
ax2.legend()
st.pyplot(fig2)
