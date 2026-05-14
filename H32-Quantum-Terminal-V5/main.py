import streamlit as st
import requests
import time

# --- 🛰️ SATELLITE CONFIG ---
st.set_page_config(page_title="ENCEPHALON V24 ELITE", layout="wide")

# API KEYS FROM ENV.TXT
GROQ_KEY = "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"
MISTRAL_KEY = "sTGr5fQ001Db2YqwXZqZDA6abPuU1awU"
GEMINI_KEY = "AIzaSyDI9PdXoYCwl6C21Q5KLBmN1LwseiQZKkI"
TELEGRAM_ID = "8376377797" #

# --- 📋 MASTER COIN LIST ---
COINS = ["ASTER", "UNI", "LTC", "ZEC", "BNB", "SOL", "AVAX", "ONDO", "BGB", "HYPE", "ADA", "SUI", "DOT", "LINK", "DOGE", "XPL", "BTC", "ETH", "XRP"]

# --- 🎨 WHALE UI ---
st.markdown("""
    <style>
    .stApp { background-color: #050a10; }
    .coin-card {
        background: #0d1621;
        border: 1px solid #00f2ff;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
    }
    .alarm-flash {
        background: #ff4444;
        color: white;
        padding: 10px;
        text-align: center;
        border-radius: 5px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 🚨 1-HOUR PRESSURE ALARM ENGINE ---
if 'last_alarm' not in st.session_state:
    st.session_state.last_alarm = time.time()

st.markdown("<h1 style='color:white; text-align:center;'>🛰️ ENCEPHALON V24: WHALE COMMANDER</h1>", unsafe_allow_html=True)

# Automatic Alarm logic for Big Pressure
if time.time() - st.session_state.last_alarm > 3600:
    st.markdown('<div class="alarm-flash">🚨 BIG PRESSURE ALERT: 1-HOUR CYCLE COMPLETE 🚨</div>', unsafe_allow_html=True)
    # Telegram alert code yahan trigger hoga
    st.session_state.last_alarm = time.time()

# --- 📊 LIVE GLOBAL DATA ---
try:
    url = f"https://min-api.cryptocompare.com/data/pricemultifull?fsyms={','.join(COINS)}&tsyms=USD"
    res = requests.get(url).json()['RAW']
    
    cols = st.columns(4)
    for i, sym in enumerate(COINS):
        if sym in res:
            p = res[sym]['USD']['PRICE']
            c = res[sym]['USD']['CHANGEPCT24HOUR']
            with cols[i % 4]:
                st.markdown(f"""
                    <div class="coin-card">
                        <p style="color:#8b949e; margin:0;">{sym}/USDT</p>
                        <h2 style="color:white; margin:0;">${p:,.2f}</h2>
                        <p style="color:{'#3fb950' if c >= 0 else '#ff4444'}; margin:0;">{c:+.2f}%</p>
                        <p style="color:#00f2ff; font-size:10px; margin-top:5px;">🚀 PURI ENTRY LENI HAI</p>
                    </div>
                """, unsafe_allow_html=True)
except:
    st.warning("📡 Re-establishing Satellite Link...")
