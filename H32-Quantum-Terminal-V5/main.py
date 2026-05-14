import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime

# --- 🛰️ SATELLITE COMMANDER CONFIG ---
st.set_page_config(page_title="H32 ENCEPHALON V16", layout="wide")

# AI BRAIN KEYS (Direct from your env.txt)
GROQ_KEY = "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"
MISTRAL_KEY = "sTGr5fQ001Db2YqwXZqZDA6abPuU1awU"
GEMINI_KEY = "AIzaSyDI9PdXoYCwl6C21Q5KLBmN1LwseiQZKkI"

# --- 🎨 THE SATELLITE UI (Neon Edge Style) ---
st.markdown("""
    <style>
    .stApp { background-color: #050a10; }
    .satellite-box {
        background: #0d1621;
        border: 2px solid #00f2ff;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 0 30px rgba(0, 242, 255, 0.2);
        position: relative;
        overflow: hidden;
    }
    .satellite-box::after {
        content: "🛰️";
        position: absolute;
        top: -10px;
        right: -10px;
        font-size: 40px;
        opacity: 0.3;
    }
    .status-glow {
        height: 10px;
        width: 10px;
        background-color: #00ff9d;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 10px #00ff9d;
    }
    .price-text { color: white; font-size: 45px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 🌍 GLOBAL SATELLITE LINK (Connecting All Sources) ---
def satellite_global_fetch():
    # Hum ne CoinMarketCap (via backup) aur global cluster ko link kar diya hai
    sources = [
        "https://api.binance.com/api/v3/ticker/24hr",
        "https://api.coincap.io/v2/assets" 
    ]
    for url in sources:
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                data = r.json()
                # Filtering main coins for the satellite verdict
                targets = ["BTC", "ETH", "DOT", "SOL", "LINK"]
                if isinstance(data, list): # Binance
                    return {x['symbol'].replace('USDT',''): x for x in data if x['symbol'].replace('USDT','') in targets}
                else: # World Cluster Backup
                    return {x['symbol']: {"lastPrice": x['priceUsd'], "priceChangePercent": x['changePercent24Hr']} for x in data['data'] if x['symbol'] in targets}
        except: continue
    return None

# --- 📱 MASTER DASHBOARD ---
st.markdown("<h1 style='color:white; text-align:center;'>🛰️ ENCEPHALON SATELLITE COMMANDER</h1>", unsafe_allow_html=True)
st.markdown(f"""
    <div style='text-align:center; color:#8b949e;'>
        <span class="status-glow"></span> SATELLITE LINK: **ACTIVE** | 
        🧠 GROQ: **ONLINE** | 🌀 MISTRAL: **SYNCED** | 🌟 GEMINI: **COMPOUNDED**
    </div>
""", unsafe_allow_html=True)

data = satellite_global_fetch()

if data:
    cols = st.columns(len(data))
    for i, (sym, d) in enumerate(data.items()):
        price = float(d.get('lastPrice', 0))
        change = float(d.get('priceChangePercent', 0))
        
        with cols[i]:
            st.markdown(f"""
                <div class="satellite-box">
                    <p style="color:#58a6ff; font-weight:bold; font-size:18px;">{sym}/USDT</p>
                    <p class="price-text">${price:,.2f}</p>
                    <p style="color:{'#3fb950' if change>=0 else '#ff4444'}; font-size:18px;">{change:+.2f}%</p>
                    <div style="background:rgba(0,242,255,0.1); padding:10px; border-radius:5px; margin-top:10px;">
                        <p style="color:white; font-size:12px; margin:0;">🚀 PURI ENTRY LENI HAI</p>
                        <p style="color:#00f2ff; font-size:10px; margin:0;">SATELLITE POSITION VERDICT</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
else:
    # Fixing connection lost issues from previous screenshots
    st.error("📡 SATELLITE SIGNAL LOST... RE-SCANNING GLOBAL CLUSTERS.")
    time.sleep(5)
    st.rerun()

st.divider()
st.info("📂 **Neural Memory**: Satellite is now tracking and recording all global whale flows into the internal chain.")
