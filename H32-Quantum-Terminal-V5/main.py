import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import pytz

# --- 🛰️ GLOBAL COMMAND CENTER ---
st.set_page_config(page_title="V1600 QUANTUM", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #000308; color: white; }
    .liquidity-card {
        background: linear-gradient(145deg, #0a1118, #0e1a26);
        border: 1px solid #00f2ff; border-radius: 15px;
        padding: 25px; margin-bottom: 20px;
        box-shadow: 0 0 20px rgba(0, 242, 255, 0.1);
    }
    .trap-alert { color: #ff4b4b; font-weight: bold; animation: blinker 1.5s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }
    .stat-val { font-size: 32px; font-weight: 900; color: #00f2ff; }
</style>
""", unsafe_allow_html=True)

# --- 🕒 12-HOUR DELHI SESSION TRACKER ---
ist = pytz.timezone('Asia/Kolkata')
now = datetime.now(ist)
session_start = now.replace(hour=now.hour - (now.hour % 12), minute=0, second=0)

st.markdown(f"<h1 style='text-align:center;'>🛰️ V1600 PSYCHOLOGY COMMAND</h1>", unsafe_allow_html=True)
st.sidebar.info(f"🕰️ Active Session: {session_start.strftime('%I %p')} - 12 Hour Cycle")

# --- 🧠 LIQUIDITY & TECHNICAL ENGINE ---
COINS = ["BTC", "ETH", "SOL"]

try:
    # 📡 Live Market Data
    url = "https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,ETH,SOL&tsyms=USD"
    res = requests.get(url).json()['RAW']

    for sym in COINS:
        p = res[sym]['USD']['PRICE']
        high = res[sym]['USD']['HIGH24HOUR']
        low = res[sym]['USD']['LOW24HOUR']
        vol = res[sym]['USD']['VOLUME24HOURTO']
        
        # 🧪 PSYCHOLOGY LOGIC (The "No Fakeout" Filter)
        # Retailers trap at 24h Highs. Liquidity is below 24h Lows.
        liquidity_grab = low * 0.995  # Sniper Entry (Wick grab)
        fakeout_zone = high * 1.005   # Trap Zone (Retailer Buy)
        
        # 🛡️ SMART FILTER
        is_fake_pump = True if (p > high * 0.98 and vol < (vol * 0.8)) else False

        with st.container():
            st.markdown(f"""
            <div class="liquidity-card">
                <div style="display:flex; justify-content:space-between;">
                    <h2 style="margin:0; color:#00f2ff;">{sym}/USDT</h2>
                    <span class="trap-alert">{'⚠️ FAKE PUMP DETECTED' if is_fake_pump else '✅ REAL VOLUME'}</span>
                </div>
                
                <div class="stat-val">${p:,.2f}</div>
                
                <div style="display:grid; grid-template-columns: 1fr 1fr; gap:15px; margin-top:20px;">
                    <div style="background:#1a0a0a; padding:10px; border-radius:8px; border:1px solid #ff4b4b;">
                        <small style="color:#ff4b4b;">LIQUIDITY TRAP (SELL)</small><br>
                        <b>${fakeout_zone:,.2f}</b>
                    </div>
                    <div style="background:#0a1a0f; padding:10px; border-radius:8px; border:1px solid #00ff88;">
                        <small style="color:#00ff88;">BEST SNIPER ENTRY</small><br>
                        <b>${liquidity_grab:,.2f}</b>
                    </div>
                </div>

                <div style="margin-top:20px; padding:15px; background:rgba(255,255,255,0.03); border-radius:10px;">
                    <b style="color:#00f2ff;">🧠 MARKET PSYCHOLOGY VERDICT:</b><br>
                    <p style="font-size:14px; color:#bbb; margin-top:5px;">
                        Delhi 12-hour session ke mutabiq, retailers <b>${high:,.2f}</b> par buy kar rahe hain. 
                        Lekin <b>Big Whale Liquidity</b> niche <b>${liquidity_grab:,.2f}</b> par baithi hai. 
                        <b>Fik mot (Fakeout)</b> se bachne ke liye wait karein jab tak price niche wick na maare.
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)

except Exception as e:
    st.error("📡 RESYNCING GLOBAL SATELLITE...")
