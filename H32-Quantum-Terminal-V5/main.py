import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="Trading System", layout="wide")
st.title("📈 CM Ultimate + Liquidity Pro Trading System")

# Fake Chart Data (Real mein API se la sakte hain)
df = pd.DataFrame({
    'Date': pd.date_range('2026-05-27', periods=100),
    'Open': [58000, 58500, 57900, 59000] * 25,
    'High': [59000, 59500, 58500, 60000] * 25,
    'Low': [57500, 58000, 57000, 58500] * 25,
    'Close': [58500, 58200, 58800, 59300] * 25
})

# Candlestick Chart
fig = go.Figure(data=[go.Candlestick(
    x=df['Date'],
    open=df['Open'],
    high=df['High'],
    low=df['Low'],
    close=df['Close'],
    name="BTCUSDT"
)])

fig.update_layout(title="BTCUSDT 1H Chart", xaxis_title="Time", yaxis_title="Price", height=600)
st.plotly_chart(fig, use_container_width=True)

# Indicators Status
col1, col2 = st.columns(2)

with col1:
    st.success("**CM Ultimate:** Blue Line crossed UP → Bullish")
    st.info("EMA 9 > EMA 21")

with col2:
    st.success("**Liquidity Pro:** Price above Green Zone")
    st.info("Buy-side Liquidity Active")

st.metric("Signal", "🟢 STRONG BUY", "High Volume Confirmed")
st.write("**Stop Loss:** Not Set | **Time Limit:** 6 Hours")
