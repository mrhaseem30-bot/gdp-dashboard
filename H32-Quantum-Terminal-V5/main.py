import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime
import os

# --- 🔱 ANIMATED CONFIG ---
st.set_page_config(page_title="ENCEPHALON CARTOON V10", layout="wide")

# Majedar Cartoonish Background & Neon Styling
st.markdown("""
    <style>
    /* Background with an animated-vibe gradient */
    .stApp {
        background: radial-gradient(circle, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    
    /* Neon Cartoon Cards */
    .cartoon-card {
        background: rgba(255, 255, 255, 0.05);
        border: 3px solid #00f2ff;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 10px 10px 0px #00f2ff; /* Cartoonish Drop Shadow */
        transition: 0.3s ease-in-out;
    }
    
    .cartoon-card:hover {
        transform: scale(1.05) rotate(1deg);
        box-shadow: 15px 15px 0px #ff00ff; /* Changes color on hover */
        border-color: #ff00ff;
    }

    h1 {
        font-family: 'Comic Sans MS', cursive, sans-serif;
        color: #00f2ff;
        text-shadow: 4px 4px #ff00ff;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 🧠 OMNI-DATA FETCHING ---
def fetch_data():
    try:
        res = requests.get("https://api.binance.com/api/v3/ticker/24hr", timeout=5)
        data = res.json()
        targets = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "SUIUSDT"]
        return {item['symbol'].replace('USDT',''): {
            "p": float(item['lastPrice']),
            "c": float(item['priceChangePercent']),
            "v": float(item['quoteVolume'])/1_000_000
        } for item in data if item['symbol'] in targets}
    except: return None

# --- 📱 UI DISPLAY ---
st.markdown("<h1 style='text-align:center;'>🛸 ENCEPHALON: SPACE ADVENTURE</h1>", unsafe_allow_html=True)

# Weekly Timer (Cartoon Style)
st.markdown("### 🕒 **Choose Your Time Travel:**")
time_cycle = st.select_slider("", options=["1h", "4h", "1d", "1w"])

market = fetch_data()

if market:
    cols = st.columns(4)
    for i, (sym, d) in enumerate(market.items()):
        with cols[i]:
            color = "#00ff9d" if d['c'] >= 0 else "#ff4444"
            st.markdown(f"""
                <div class="cartoon-card">
                    <h3 style="color:#ffffff; margin:0;">{sym}</h3>
                    <h2 style="color:{color}; font-size:30px;">${d['p']:,.2f}</h2>
                    <p style="color:#58a6ff; font-weight:bold;">{d['c']:+.2f}%</p>
                    <p style="font-size:10px; color:#8b949e;">WHALE ENERGY: DETECTED ⚡</p>
                </div>
            """, unsafe_allow_html=True)

# Memory Section
st.divider()
st.markdown("### 📂 **The Vault of Secrets (Neural Memory)**")
# Storage logic and dataframe display here...

time.sleep(10)
st.rerun()
