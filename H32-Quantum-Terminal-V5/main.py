import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Trading Dashboard", layout="wide")
st.title("📈 CM Ultimate + Liquidity Pro System")

st.write(f"**Current Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

asset = st.selectbox("Select Asset", ["BTCUSDT", "GOLD", "ETHUSDT"])

st.subheader("Current Price")
st.metric(label="BTCUSDT", value="₹ 58,930", delta="-1.72%")

col1, col2 = st.columns(2)

with col1:
    st.success("**1H Trend:** BULLISH")
    st.write("EMA 9 > EMA 21 (CM Ultimate)")

with col2:
    st.success("**Liquidity Status:** Above Green Zone")

st.divider()

st.subheader("🎯 SIGNAL")
st.success("**🟢 STRONG BUY**")
st.write("• CM Ultimate Crossover: UP")
st.write("• Liquidity Pro: Buy Side Active")
st.write("• Volume: High")

st.write("**Stop Loss:** Not Set")
st.write("**Target:** 1:2")
st.write("**Time Limit:** 6 Hours")

st.caption("Simple & Lightweight Dashboard")
