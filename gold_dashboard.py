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

import pandas as pd
import streamlit as st
import ta  # Make sure 'ta' is in your requirements.txt

st.markdown("## 🇰🇭 Cambodian Gold Market Analysis")

# Load data from Google Sheets
@st.cache_data(ttl=3600)
def load_cambodia_gold():
    url = "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/export?format=csv"
    df = pd.read_csv(url)
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")
    df = df.rename(columns={"Gold Price": "Price"})
    return df

try:
    gold_kh_df = load_cambodia_gold()

    # 📊 Display the latest price table
    st.dataframe(gold_kh_df.tail(10), use_container_width=True)

    # 📈 Add Moving Average
    gold_kh_df["MA7"] = gold_kh_df["Price"].rolling(window=7).mean()
    st.line_chart(gold_kh_df.set_index("Date")[["Price", "MA7"]])

    # 🧠 Optional: RSI
    gold_kh_df["RSI"] = ta.momentum.RSIIndicator(close=gold_kh_df["Price"], window=14).rsi()
    st.line_chart(gold_kh_df.set_index("Date")[["RSI"]])

except Exception as e:
    st.error("⚠️ Could not load or process Cambodian gold data.")
    st.code(str(e))

url = "https://docs.google.com/spreadsheets/d/e/your_sheet_id/pub?output=csv"
df = pd.read_csv(url)

url = "https://docs.google.com/spreadsheets/d/e/your_sheet_id/pub?output=csv"
df = pd.read_csv(url)

import pandas as pd
from io import StringIO

data = """
Date,Price_KHR
2025-04-20,9500000
2025-04-21,9520000
2025-04-22,9480000
2025-04-23,9530000
"""

df = pd.read_csv(StringIO(data), parse_dates=["Date"])

import pandas as pd
from io import StringIO

mock_data = """
Date,Price_KHR
2025-04-20,9500000
2025-04-21,9520000
2025-04-22,9480000
2025-04-23,9530000
"""

df = pd.read_csv(StringIO(mock_data), parse_dates=["Date"])
