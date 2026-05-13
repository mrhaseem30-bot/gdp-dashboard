import streamlit as st
import pandas as pd
import ccxt
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="H32 Quantum V5.1", layout="wide", page_icon="⚡")

st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #0a0e17, #11151f); color: #e0e0e0; }
    .big-signal { padding: 25px; border-radius: 20px; text-align: center; font-size: 1.8rem; font-weight: bold; margin: 10px 0; }
</style>
""", unsafe_allow_html=True)

st.title("⚡ H32 QUANTUM TERMINAL V5.1")
st.caption("SMC + ICT + AI + Macro + Time Intelligence + Urdu Voice")

# Sidebar
with st.sidebar:
    st.header("📍 Watchlist")
    coins = ["BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT", "XRP/USDT", "DOGE/USDT", 
             "ADA/USDT", "AVAX/USDT", "SUI/USDT", "LINK/USDT"]
    symbol = st.selectbox("Select Coin", coins)
    tf = st.selectbox("Timeframe", ["15m", "1h", "4h", "1d"])

@st.cache_data(ttl=60)
def get_data(symbol, timeframe, limit=400):
    exchange = ccxt.binance({'enableRateLimit': True})
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

if st.button("🚀 FULL QUANTUM ANALYSIS", type="primary"):
    with st.spinner("AI + Satellite + SMC chal rahe hain..."):
        df = get_data(symbol, tf)
        price = df['close'].iloc[-1]
        
        # Technical Analysis
        ma20 = df['close'].rolling(20).mean().iloc[-1]
        ma50 = df['close'].rolling(50).mean().iloc[-1]
        score = 65
        reasons = []
        
        if price > ma20 > ma50:
            structure = "Bullish"
            score += 25
            reasons.append("Strong EMA Alignment")
        else:
            structure = "Bearish / Neutral"
