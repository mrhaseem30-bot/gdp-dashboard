import streamlit as st
from market import get_price
from orderbook import get_orderbook
from whales import detect_whales
from psychology import session_bias
from ai_engine import generate_signal

st.set_page_config(page_title="H32 ULTRA GOLD AI", layout="wide")

st.title("🔥 H32 ULTRA GOLD AI SYSTEM")

symbol = st.selectbox("Select Asset", ["XAUUSD", "BTCUSDT", "ETHUSDT"])

# =========================
# REAL PRICE
# =========================
price = get_price(symbol)

st.metric("📊 Live Price", price)

# =========================
# DATA
# =========================
bids, asks = get_orderbook(symbol)

if bids is not None:

    signal = generate_signal(bids, asks)

    buy_whales = detect_whales(bids)
    sell_whales = detect_whales(asks)

    bias = session_bias()

    st.success(f"AI SIGNAL: {signal}")
    st.info(f"SESSION BIAS: {bias}")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🟢 BUY WHALES")
        st.dataframe(buy_whales.head(10))

    with col2:
        st.subheader("🔴 SELL WHALES")
        st.dataframe(sell_whales.head(10))

else:
    st.error("Market data unavailable")
