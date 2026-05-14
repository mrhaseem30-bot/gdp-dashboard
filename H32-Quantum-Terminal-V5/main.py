import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import pytz

# --- 🛰️ SUPREME SETTINGS ---
st.set_page_config(page_title="V1700 OMNI", layout="wide")

# --- 🌌 NEON INTERFACE (Auto-Fix for Mobile) ---
st.markdown("""
<style>
    .stApp { background-color: #00050a; color: white; }
    .omni-card {
        background: #0a1118; border: 2px solid #00f2ff;
        border-radius: 12px; padding: 18px; margin-bottom: 20px;
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.2);
    }
    .neon-glow { color: #00f2ff; text-shadow: 0 0 8px #00f2ff; font-weight: bold; }
    .price-big { font-size: 34px; font-weight: 900; margin: 10px 0; }
    .alert-box { padding: 10px; border-radius: 5px; font-size: 13px; margin-top: 10px; }
</style>
""", unsafe_allow_html=True)

# --- 🕒 DELHI 12-HOUR TRACKER ---
ist = pytz.timezone('Asia/Kolkata')
now_ist = datetime.now(ist)
st.markdown(f"<h1 style='text-align:center;' class='neon-glow'>🛰️ V1700 OMNI-TRACER</h1>", unsafe_allow_html=True)
st.sidebar.write(f"🕰️ Delhi Session: {now_ist.strftime('%I:%M %p')}")

# --- 🧠 LIQUIDITY & PSYCHOLOGY LOGIC ---
coins = ["BTC", "ETH", "SOL"]

try:
    # Fetching Data
    raw_data = requests.get("https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,ETH,SOL&tsyms=USD").json()['RAW']

    for sym in coins:
        p = raw_data[sym]['USD']['PRICE']
        h = raw_data[sym]['USD']['HIGH24HOUR']
        l = raw_data[sym]['USD']['LOW24HOUR']
        v = raw_data[sym]['USD']['VOLUME24HOURTO']
        
        # 🔱 PSYCHOLOGY ENGINE: Detecting "Fik Mot" (Fakeouts)
        # 1. Best Entry: Liquidity grab niche hoti hai (Puri Entry)
        puri_entry = l * 0.992 
        # 2. Zed Zone: Retailer trap upar hota hai
        zed_zone = h * 1.008 
        
        # Filter: Agar price high ke paas hai par volume low hai = FAKEOUT
        is_fake = True if (p > h * 0.97 and v < 50000000) else False

        # --- 📱 CLEAN RENDERING (No Raw Code) ---
        st.markdown(f"""
        <div class="omni-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="font-size:22px;" class="neon-glow">{sym}/USDT</span>
                <span style="color:{'#ff4b4b' if is_fake else '#00ff88'}; font-weight:bold;">
                    {'⚠️ FIK MOT (FAKE)' if is_fake else '✅ REAL VOLUME'}
                </span>
            </div>
            
            <div class="price-big">${p:,.2f}</div>
            
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px;">
                <div style="background:#1a0d0d; border:1px solid #ff4b4b; padding:10px; border-radius:8px; text-align:center;">
                    <small style="color:#ff4b4b;">ZED ZONE (SELL)</small><br>
                    <b>${zed_zone:,.2f}</b>
                </div>
                <div style="background:#0d1a10; border:1px solid #00ff88; padding:10px; border-radius:8px; text-align:center;">
                    <small style="color:#00ff88;">PURI ENTRY (BUY)</small><br>
                    <b>${puri_entry:,.2f}</b>
                </div>
            </div>

            <div class="alert-box" style="background:rgba(0,242,255,0.05); border-left:4px solid #00f2ff;">
                <b style="color:#00f2ff;">🧠 LIQUIDITY ANALYSIS:</b><br>
                Delhi 12-hour cycle ke mutabiq, retailers <b>${h:,.2f}</b> par trap ho rahe hain. 
                Asli <b>Whale Liquidity</b> niche <b>${puri_entry:,.2f}</b> par hai. 
                Wahan wick lagne ka intezar karein.
            </div>
        </div>
        """, unsafe_allow_html=True)

except Exception as e:
    st.error("📡 SATELLITE SYNC ERROR: Please update requirements.txt")
