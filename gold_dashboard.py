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
st.write(cambodia_df.head())
st.write(cambodia_df.columns)
# Load Global Gold Prices
@st.cache_data
def load_global_data():
    url = "https://docs.google.com/spreadsheets/d/1wnNRlSy2MwVYRApGPOCeCEdjXeVC-XmMjL7BhDiXmrw/export?format=csv&id=1wnNRlSy2MwVYRApGPOCeCEdjXeVC-XmMjL7BhDiXmrw&gid=0"
    return pd.read_csv(url)

# Load Cambodia Gold Prices
@st.cache_data
def load_cambodia_data():
    url = "https://docs.google.com/spreadsheets/d/1wnNRlSy2MwVYRApGPOCeCEdjXeVC-XmMjL7BhDiXmrw/export?format=csv&id=1wnNRlSy2MwVYRApGPOCeCEdjXeVC-XmMjL7BhDiXmrw&gid=414083665"
    return pd.read_csv(url)

# Load data
global_df = load_global_data()
cambodia_df = load_cambodia_data()

# Set titles
st.title("🌍📊 Gold Price Dashboard")
st.markdown("**Global vs Cambodian Market (USD)**")

# GLOBAL GOLD PRICE CHART
fig_global = go.Figure()
fig_global.add_trace(go.Scatter(x=global_df['Date'], y=global_df['Gold Price'], name='Global Gold Price', line=dict(color='gold')))
fig_global.add_trace(go.Scatter(x=global_df['Date'], y=global_df['MA20'], name='MA20', line=dict(color='blue', dash='dot')))
fig_global.add_trace(go.Scatter(x=global_df['Date'], y=global_df['MA50'], name='MA50', line=dict(color='green', dash='dash')))
fig_global.update_layout(title="Global Gold Prices & Moving Averages", xaxis_title="Date", yaxis_title="USD/oz")
st.plotly_chart(fig_global)

# CAMBODIA GOLD PRICE CHART
fig_cam = go.Figure()
fig_cam.add_trace(go.Scatter(x=cambodia_df['Date'], y=cambodia_df['Chi → USD'], name='Chi (USD)', line=dict(color='orange')))
fig_cam.add_trace(go.Scatter(x=cambodia_df['Date'], y=cambodia_df['Damlung → USD'], name='Damlung (USD)', line=dict(color='red')))
fig_cam.update_layout(title="Cambodian Gold Prices (Chi & Damlung)", xaxis_title="Date", yaxis_title="Price in USD")
st.plotly_chart(fig_cam)

# Show RSI Chart (Optional)
fig_rsi = go.Figure()
fig_rsi.add_trace(go.Scatter(x=global_df['Date'], y=global_df['RSI'], name='RSI', line=dict(color='purple')))
fig_rsi.update_layout(title="Global Gold Price RSI (14-Day)", xaxis_title="Date", yaxis_title="RSI")
st.plotly_chart(fig_rsi)

st.markdown("Data powered by Google Sheets | Analysis by You 🧠")
