# gold_dashboard.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

st.title("📈 Gold Price Tracker (Mini Dashboard)")

# Simulated data (you can later connect API or Google Sheets)
data = {
    'Date': pd.date_range(end=datetime.today(), periods=10).tolist(),
    'Gold Price': [2320, 2330, 2310, 2340, 2355, 2370, 2365, 2380, 2375, 2390]
}
df = pd.DataFrame(data)

# Show table
st.subheader("📊 Price Table")
st.dataframe(df)

# Moving average
df['MA_3'] = df['Gold Price'].rolling(3).mean()

# Show chart
st.subheader("📉 Price Chart with Moving Average")
fig, ax = plt.subplots()
ax.plot(df['Date'], df['Gold Price'], label='Gold Price')
ax.plot(df['Date'], df['MA_3'], label='3-Day MA', linestyle='--')
ax.legend()
st.pyplot(fig)
