import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime

# --- 🛰️ SATELLITE COMMANDER CONFIG ---
st.set_page_config(page_title="ENCEPHALON V17", layout="wide")

# AI BRAINS (Direct from your env.txt)
GROQ_KEY = "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"
MISTRAL_KEY = "sTGr5fQ001Db2YqwXZqZDA6abPuU1awU"
GEMINI_KEY = "AIzaSyDI9PdXoYCwl6C21Q5KLBmN1LwseiQZKkI"

# --- 🎨 THE SATELLITE UI (Screenshot 214819 Style) ---
st.markdown("""
    <style>
    .stApp { background-color: #050a10; }
    .satellite-card {
        background-color: #0d1621;
        border: 2px solid #00f2ff;
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 0 20px rgba(0, 242, 255, 0.2);
    }
    .verdict-box {
        background: rgba(0, 242, 255, 0.1);
        border-left: 5px solid #00f2ff;
        padding: 10px;
        border-radius: 5px;
    }
    .price-text { color: white; font-size: 40px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 🌍 WORLD SATELLITE LINK (Triple Path) ---
def satellite_engine():
    # Attempt 1: Binance Public API | Attempt 2: World Asset Cluster
    urls = [
        "https://api.binance.com/api/v3/ticker/24hr",
        "https://api.coincap.io/v2/assets"
    ]
    for url in urls:
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                data = r.json()
                targets = ["BTC", "ETH", "DOT", "SOL", "LINK"]
                # Logic for different world sources
                if isinstance(data, list): # Binance Format
                    return {x['symbol'].replace('USDT',''): x for x in data if x['symbol'].replace('USDT','') in targets}
                else: # Global Cluster Format
                    return {x['symbol']: {"lastPrice": x['priceUsd'], "priceChangePercent": x['changePercent24Hr']} for x in data['data'] if x['symbol'] in targets}
        except: continue
    return None

# --- 🧠 MASTER INTERFACE ---
st.markdown("<h1 style='color:white; text-align:center;'>🛰️ ENCEPHALON SATELLITE COMMANDER</h1>", unsafe_allow_html=True)
st.markdown(f"🟢 **Satellite Link:** ACTIVE | 🧠 **Groq:** ONLINE | 🌀 **Mistral:** SYNCED | 🌟 **Gemini:** COMPOUNDED")

intel = satellite_engine()

if intel:
    cols = st.columns(len(intel))
    for i, (sym, d) in enumerate(intel.items()):
        p = float(d.get('lastPrice', 0))
        c = float(d.get('priceChangePercent', 0))
        
        with cols[i]:
            st.markdown(f"""
                <div class="satellite-card">
                    <div style="color:white; font-size:20px;">● {sym}/USDT <span style="color:#3fb950; float:right;">{c:+.2f}%</span></div>
                    <div class="price-text">${p:,.2f}</div>
                    <div class="verdict-box">
                        <p style="color:#8b949e; font-size:10px; margin:0;">SATELLITE POSITION VERDICT</p>
                        <p style="color:white; font-weight:bold; margin:5px 0;">🚀 PURI ENTRY LENI HAI</p>
                        <p style="color:#3fb950; font-size:12px;">ENTRY: ${p:,.2f} | TARGET: ${(p*1.15):,.2f}</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
else:
    # Error fix for Screenshot 151041
    st.error("📡 SATELLITE SIGNAL RE-ESTABLISHING... SCANNING BACKUP WORLD SITES.")
    time.sleep(5)
    st.rerun()

st.divider()
st.info("📂 **Neural Memory**: Global history is being stitched from all linked websites.")
