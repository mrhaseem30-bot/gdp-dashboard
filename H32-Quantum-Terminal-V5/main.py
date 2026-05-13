import streamlit as st
import pandas as pd
import ccxt
import requests
import time

st.set_page_config(page_title="H32 Quantum Terminal V5.1", layout="wide", page_icon="⚡")

st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #0a0e17, #11151f); color: #e0e0e0; }
    .big-signal { padding: 25px; border-radius: 20px; text-align: center; font-size: 1.8rem; font-weight: bold; margin: 10px 0; }
</style>
""", unsafe_allow_html=True)

st.title("⚡ H32 QUANTUM TERMINAL V5.1")
st.caption("Multi-Source Data • SMC + Time Intelligence")

with st.sidebar:
    st.header("📍 Watchlist")
    coins = ["BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT", "XRP/USDT", 
             "DOGE/USDT", "ADA/USDT", "AVAX/USDT", "SUI/USDT"]
    symbol = st.selectbox("Select Coin", coins)
    tf = st.selectbox("Timeframe", ["15m", "1h", "4h", "1d"])

@st.cache_data(ttl=30)
def get_data(symbol, timeframe, limit=250):
    sources = ["binance", "kraken", "bybit", "coingecko"]
    
    for source in sources:
        try:
            if source == "coingecko":
                coin = symbol.lower().replace("/usdt", "")
