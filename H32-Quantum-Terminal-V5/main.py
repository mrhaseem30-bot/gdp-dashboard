import streamlit as st
import pandas as pd
import ccxt
import time

st.set_page_config(page_title="H32 Quantum V5.1", layout="wide", page_icon="⚡")

st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #0a0e17, #11151f); color: #e0e0e0; }
    .big-signal { padding: 25px; border-radius: 20px; text-align: center; font-size: 1.8rem; font-weight: bold; margin: 10px 0; }
</style>
""", unsafe_allow_html=True)

st.title("⚡ H32 QUANTUM TERMINAL V5.1")
st.caption("Smart Money + ICT + Time Intelligence")

with st.sidebar:
    st.header("📍 Watchlist")
    coins = ["BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT", "XRP/USDT", 
             "DOGE/USDT", "ADA/USDT", "AVAX/USDT", "SUI/USDT"]
    symbol = st.selectbox("Select Coin", coins)
    tf = st.selectbox("Timeframe", ["15m
