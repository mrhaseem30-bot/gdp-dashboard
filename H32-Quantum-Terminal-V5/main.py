import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime
import os

# --- 🔱 CONFIG & GLOBAL MEMORY ---
st.set_page_config(page_title="H32 ENCEPHALON V11", layout="wide")

MEMORY_FILE = "global_master_memory.csv"
if not os.path.exists(MEMORY_FILE):
    pd.DataFrame(columns=['Time', 'Symbol', 'Price', 'Vol_M', 'Signal']).to_csv(MEMORY_FILE, index=False)

# --- 🎨 VISIBLE CARTOON UI (Fix for Screenshot Issues) ---
st.markdown("""
    <style>
    .stApp {
        background-color: #121212; /* Deep dark blue-black */
        background-image: radial-gradient(#2d3436 1px, transparent 1px);
        background-size: 20px 20px; /* Comic book dot pattern */
    }
    .neon-card {
        background: #1e272e;
        border: 4px solid #00f2ff;
        border-radius: 15px;
        padding: 15px;
        box-shadow: 8px 8px 0px #ff00ff; /* Solid Cartoon Shadow */
        margin-bottom: 20px;
    }
    h1, h2, h3, p {
        color: white !important;
        font-family: 'Bangers', cursive, sans-serif;
    }
    .stSlider label { color: #00f2ff !important; font-size: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 🌍 GLOBAL SEARCH ENGINE (Puri Duniya Ka Data) ---
def fetch_global_intelligence():
    try:
        # Global API - Multiple exchanges logic
        res = requests.get("https://api.binance.com/api/v3/ticker/24hr", timeout=8)
        all_data = res.json()
        targets = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "SUIUSDT", "XRPUSDT", "BNBUSDT"]
        
        refined = {}
        for item in all_data:
            if item['symbol'] in targets:
                sym = item['symbol'].replace('USDT', '')
                refined[sym] = {
                    "p": float(item['lastPrice']),
                    "c": float(item['priceChangePercent']),
                    "v": float(item['quoteVolume']) / 1_000_000,
                    "t": datetime.now().strftime("%H:%M:%S")
                }
        return refined
    except:
        return None

# --- 📱 MASTER DASHBOARD ---
st.markdown("<h1 style='text-align:center;'>🚀 GLOBAL ENCEPHALON V11</h1>", unsafe_allow_html=True)

# 1 Week Timer (Compound Window)
time_frame = st.select_slider("Select Global Memory Window:", options=["1h", "4h", "1d", "1w"])

intel = fetch_global_intelligence()

if intel:
    # Storage Hit (Save to CSV for History)
    for s, d in intel.items():
        if d['v'] > 100: # $100M+ Volume
            new_row = pd.DataFrame([[d['t'], s, d['p'], d['v'], "WHALE_HIT"]], columns=['Time', 'Symbol', 'Price', 'Vol_M', 'Signal'])
            new_row.to_csv(MEMORY_FILE, mode='a', header=False, index=False)

    # UI Display (Visible Cards)
    cols = st.columns(len(intel))
    for i, (sym, val) in enumerate(intel.items()):
        with cols[i]:
            glow = "#00ff9d" if val['c'] >= 0 else "#ff4444"
            st.markdown(f"""
                <div class="neon-card" style="border-color: {glow};">
                    <h2 style="margin:0; font-size:25px;">{sym}</h2>
                    <h1 style="color:{glow}; font-size:35px; margin:10px 0;">${val['p']:,.2f}</h1>
                    <p style="color:#58a6ff;">Vol: {val['v']:.1f}M | {val['c']:+.2f}%</p>
                    <p style="font-size:10px; color:#8b949e;">GLOBAL SYNC: OK</p>
                </div>
            """, unsafe_allow_html=True)
else:
    st.error("⚠️ Global Connection Lost! Retrying internal chain...")

# --- 📂 NEURAL MEMORY RECALL ---
st.subheader("📁 Neural Memory (Puri Duniya Ki History)")
hist = pd.read_csv(MEMORY_FILE)
if not hist.empty:
    st.dataframe(hist.tail(15).iloc[::-1], use_container_width=True)

time.sleep(8)
st.rerun()
