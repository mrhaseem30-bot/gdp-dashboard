import streamlit as st
import pandas as pd
import requests
from streamlit_autorefresh import st_autorefresh

# --- 🔱 CORE SETUP ---
CMC_KEY = "04d81f211e234e55a3e281b9ae23256f"
GROQ_KEY = "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"

st.set_page_config(page_title="H32 OMNISCIENT V170", layout="wide")

# Error Fix: Ye function ab library install hone ke baad hi chalega
try:
    st_autorefresh(interval=30000, key="v170_final_sync")
except:
    st.warning("Installing refresh engine... Please wait.")

# --- 🎨 FINAL TERMINAL UI ---
st.markdown("""
<style>
    .stApp { background-color: #05070a !important; color: #e2e8f0; }
    .terminal-card {
        background: #0d1117; border: 1px solid #30363d;
        border-radius: 12px; padding: 15px; margin-bottom: 15px;
    }
    .price-text { font-size: 1.8rem; font-weight: 800; color: #ffffff; }
    .gauge-bg { height: 12px; background: #21262d; border-radius: 6px; margin: 10px 0; display: flex; overflow: hidden; }
    .gauge-short { background: #ff4444; height: 100%; }
    .gauge-long { background: #00ff9d; height: 100%; }
    .whale-signal { 
        background: rgba(36, 129, 204, 0.1); border: 1px solid #2481cc; 
        padding: 8px; border-radius: 6px; font-size: 0.8rem; text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# --- 📡 DATA EXECUTION ---
st.title("🔱 H32 OMNISCIENT V170")

target_coins = ["BTC", "ETH", "SOL", "SUI", "XRP", "BONE"]

try:
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    headers = {'X-CMC_PRO_API_KEY': CMC_KEY}
    params = {'symbol': ",".join(target_coins), 'convert': 'USD'}
    
    r = requests.get(url, headers=headers, params=params)
    data = r.json()['data']

    for sym in target_coins:
        coin = data[sym]
        p = coin['quote']['USD']['price']
        c24 = coin['quote']['USD']['percent_change_24h']
        
        # Liquidation Gap calculation
        gap = p * 0.05 

        # Mobile Optimized Card
        st.markdown(f"""
        <div class="terminal-card">
            <div style="display: flex; justify-content: space-between;">
                <span style="color:#58a6ff; font-weight:bold;">{sym}/USDT</span>
                <span style="color: {'#00ff9d' if c24 > 0 else '#ff4444'}">{c24:+.2f}%</span>
            </div>
            <div class="price-text">${p:,.2f}</div>
            
            <div style="background:#161b22; padding:8px; border-radius:6px; font-family:monospace; margin:10px 0;">
                <span style="color:#8b949e">LIQ GAP:</span> <span style="color:#ff4444">±${gap:,.2f}</span>
            </div>

            <div class="gauge-bg">
                <div class="gauge-short" style="width: 45%;"></div>
                <div class="gauge-long" style="width: 55%;"></div>
            </div>
            
            <div class="whale-signal">
                🐋 WHALE FLOW: {'Heavy Accumulation' if c24 > 0 else 'Squeeze Risk Detected'}
            </div>
        </div>
        """, unsafe_allow_html=True)

except Exception as e:
    st.error("Waiting for Data Core...")
