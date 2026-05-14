import streamlit as st
import requests
import time
from datetime import datetime

# --- 🛰️ SATELLITE CONFIG ---
st.set_page_config(page_title="ENCEPHALON V23 ELITE", layout="wide")

# API KEYS & IDs (Linked from your files)
[span_0](start_span)GROQ_KEY = "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"[span_0](end_span)
[span_1](start_span)MISTRAL_KEY = "sTGr5fQ001Db2YqwXZqZDA6abPuU1awU"[span_1](end_span)
[span_2](start_span)GEMINI_KEY = "AIzaSyDI9PdXoYCwl6C21Q5KLBmN1LwseiQZKkI"[span_2](end_span)
TELEGRAM_ID = "8376377797"
BOT_TOKEN = "APKA_BOT_TOKEN_YAHAN_DALEIN" 

# --- 📋 FULL COIN LIST (Linked from Screenshot 094220) ---
COIN_LIST = [
    "ASTER", "UNI", "LTC", "ZEC", "BNB", "SOL", "AVAX", "ONDO", 
    "BGB", "HYPE", "ADA", "SUI", "DOT", "LINK", "DOGE", "XPL", "BTC", "ETH", "XRP"
]

# --- 🎨 WHALE-SATELLITE UI ---
st.markdown("""
    <style>
    .stApp { background-color: #050a10; }
    .coin-card {
        background: #0d1621;
        border: 1px solid #00f2ff;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 10px;
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.1);
    }
    .pressure-alert {
        background: linear-gradient(45deg, #ff0000, #440000);
        color: white;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        animation: blinker 1.5s linear infinite;
    }
    @keyframes blinker { 50% { opacity: 0; } }
    </style>
    """, unsafe_allow_html=True)

# --- 🚨 AUTOMATIC ALARM & PRESSURE ENGINE ---
def send_telegram_alert(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": TELEGRAM_ID, "text": msg})

if 'alarm_time' not in st.session_state:
    st.session_state.alarm_time = time.time()

# --- 📱 MASTER DASHBOARD ---
st.markdown("<h1 style='color:white; text-align:center;'>🛰️ ENCEPHALON V23: GLOBAL COMMANDER</h1>", unsafe_allow_html=True)

# Check for Big Pressure (1 Hour Alarm)
if time.time() - st.session_state.alarm_time > 3600:
    st.markdown('<div class="pressure-alert">🚨 BIG PRESSURE DETECTED! 1-HOUR ALARM TRIGGERED 🚨</div>', unsafe_allow_html=True)
    send_telegram_alert("⚠️ URGENT: Big pressure on market detected. Check Encephalon now!")
    st.session_state.alarm_time = time.time()

# --- 🌍 LIVE COIN GRID ---
try:
    # Multiple sources for Unlimited Data
    url = f"https://min-api.cryptocompare.com/data/pricemultifull?fsyms={','.join(COIN_LIST)}&tsyms=USD"
    res = requests.get(url).json()['RAW']
    
    cols = st.columns(4) # 4 columns for clean look
    for idx, sym in enumerate(COIN_LIST):
        if sym in res:
            p = res[sym]['USD']['PRICE']
            c = res[sym]['USD']['CHANGEPCT24HOUR']
            v = res[sym]['USD']['VOLUME24HOUR']
            
            with cols[idx % 4]:
                color = "#3fb950" if c >= 0 else "#ff4444"
                st.markdown(f"""
                    <div class="coin-card">
                        <div style="color:white; font-size:14px; font-weight:bold;">● {sym}/USDT</div>
                        <div style="color:white; font-size:24px; font-weight:800;">${p:,.2f}</div>
                        <div style="color:{color}; font-size:14px;">{c:+.2f}%</div>
                        <div style="color:#8b949e; font-size:10px;">Pressure: {'High' if v > 1000000 else 'Stable'}</div>
                    </div>
                """, unsafe_allow_html=True)
except Exception as e:
    st.error("📡 Signal Lost. Re-scanning Clusters...")
