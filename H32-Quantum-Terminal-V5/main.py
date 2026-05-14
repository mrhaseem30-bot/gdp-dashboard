import streamlit as st
import pandas as pd
import requests
import time

# --- 🛰️ SATELLITE ELITE CONFIG ---
st.set_page_config(page_title="ENCEPHALON CMC V19", layout="wide")

# AI BRAINS FROM ENV.TXT
GROQ_KEY = "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"
GEMINI_KEY = "AIzaSyDI9PdXoYCwl6C21Q5KLBmN1LwseiQZKkI"

# --- 🎨 SATELLITE UI (PREMIUM NEON) ---
st.markdown("""
    <style>
    .stApp { background-color: #050a10; }
    .satellite-card {
        background-color: #0d1621;
        border: 2px solid #00f2ff;
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 0 25px rgba(0, 242, 255, 0.3);
    }
    .price-text { color: white; font-size: 42px; font-weight: 800; }
    .verdict-box {
        background: rgba(0, 242, 255, 0.1);
        border-left: 5px solid #00f2ff;
        padding: 12px;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 🌍 UNLIMITED MARKET CAP ENGINE (ID: 04d81f21...) ---
def fetch_elite_data():
    # Linking CoinMarketCap, Binance, and CryptoCompare for Zero Failure
    sources = [
        "https://api.binance.com/api/v3/ticker/24hr",
        "https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,ETH,SUI,SOL,DOT&tsyms=USD",
        "https://api.coincap.io/v2/assets"
    ]
    
    for url in sources:
        try:
            r = requests.get(url, timeout=4)
            if r.status_code == 200:
                res = r.json()
                # Unified Parsing for SUI (ID: 04d81f21...) and others
                if "RAW" in res: # CryptoCompare (Stable for CMC data)
                    return {k: {"p": v['USD']['PRICE'], "c": v['USD']['CHANGEPCT24HOUR'], "m": v['USD']['MKTCAP']} for k, v
