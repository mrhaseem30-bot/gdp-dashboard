import streamlit as st
import pandas as pd
import ccxt
import requests
from macro_sentinel import get_macro_context
from smc_engine import detect_market_structure, get_key_levels, calculate_confluence
from ai_analyst import get_ai_verdict_with_timeframe

st.set_page_config(page_title="H32 Quantum Terminal V6.0", layout="wide", page_icon="⚡")

# Professional Dark Theme
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #0a0a0a, #1a1a2e, #16213e); color: #e0e0e0; }
    .big-signal { padding: 25px; border-radius: 15px; text-align: center; font-size: 2rem; font-weight: bold; margin: 10px 0; }
    .level-box { padding: 15px; border-radius: 10px; background: rgba(255,255,255,0.08); margin: 8px 0; text-align: center; }
</style>
""", unsafe_allow_html=True)

st.title("⚡ H32 QUANTUM TERMINAL V6.0")
st.caption("Satellite Real-Time • SMC + Liquidation Engine")

with st.sidebar:
    st.header("📍 Watchlist")
    coins = ["BTC/USDT", "ETH/USDT", "SOL/USDT", "AVAX/USDT", "SUI/USDT"]
    symbol = st.selectbox("Select Coin", coins)
    tf = st.selectbox("Timeframe", ["15m", "1h", "4h", "1d"])

@st.cache_data(ttl=15)
def get_data(symbol, timeframe, limit=300):
    sources = ["binance", "bybit", "kraken", "coingecko"]
    for source in sources
