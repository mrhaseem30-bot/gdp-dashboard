import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Page Setup
st.set_page_config(page_title="My Trading Dashboard", layout="wide", page_icon="📊")
st.title("🚀 My Simple Trading Dashboard")
st.markdown("**CM Ultimate + Liquidity Pro System**")

# Current Time
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.write(f"**Current Time:** {current_time}")

# Asset Selector
asset = st.selectbox("Select Asset", ["BTCUSDT", "GOLD (XAUUSD)", "ETHUSDT", "NASDAQ"])

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Current Price", "₹ 58,930", "-1.72%")

with col2:
    st.metric("1H Trend", "🟢 BULLISH", "EMA 9 > EMA 21")

with col3:
    st.metric("Signal", "🟢 **BUY**", "Strong")

st.divider()

# Main Dashboard
st.subheader("📊 Trading Signals")

colA, colB = st.columns(2)

with colA:
    st.success("**BUY SIGNAL**")
    st.write("• CM Ultimate: Blue Line crossed up")
    st.write("• Liquidity: Price above Green Zone")
    st.write("• Volume: High")
    st.write("**Entry:** Now")
    st.write("**Stop Loss:** Not Set (as per your rule)")
    st.write("**Target:** 1:2  |  **Time Limit:** 6 Hours")

with colB:
    st.error("**SELL SIGNAL** (Last)")
    st.write("• CM Ultimate: Blue Line crossed down")
    st.write("• Liquidity: Below Red Zone")

st.divider()

# Recent Signals
st.subheader("📋 Recent Signals")
data = {
    "Time": ["10:30", "09:15", "08:00"],
    "Signal": ["BUY", "HOLD", "SELL"],
    "Price": ["58,930", "58,650", "59,200"],
    "Status": ["Active", "Closed", "Closed"]
}
df = pd.DataFrame(data)
st.table(df)

st.caption("Made for mobile + desktop | Lag-free")
