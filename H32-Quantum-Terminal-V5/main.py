import streamlit as st
import requests
from datetime import datetime
import pytz

# --- 🛰️ SYSTEM SETTINGS ---
st.set_page_config(page_title="V1400 SUPREME", layout="wide")

# --- 🌌 NEON UI FIX (Mobile Compatible) ---
st.markdown("""
<style>
    .stApp { background-color: #00050a; color: white; }
    .card {
        background: #0a1118; border: 2px solid #00f2ff;
        border-radius: 15px; padding: 20px; margin-bottom: 20px;
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.3);
    }
    .neon-text { color: #00f2ff; text-shadow: 0 0 10px #00f2ff; font-weight: 900; }
    .price { font-size: 38px; font-weight: 900; margin: 5px 0; }
    .zone-box { 
        background: #121921; border: 1px solid #333; padding: 10px; 
        border-radius: 8px; text-align: center; width: 48%;
    }
</style>
""", unsafe_allow_html=True)

# --- 🕒 DELHI TIME SYNC ---
ist = pytz.timezone('Asia/Kolkata')
now_ist = datetime.now(ist)
st.markdown(f"<h1 style='text-align:center;' class='neon-text'>🛰️ DELHI SESSION COMMANDER</h1>", unsafe_allow_html=True)

# --- 🧠 GLOBAL RESEARCH & PSYCHOLOGY ---
ELITE_COINS = ["BTC", "ETH", "SOL", "LINK"]

try:
    url = "https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,ETH,SOL,LINK&tsyms=USD"
    raw_data = requests.get(url).json()['RAW']
    
    for sym in ELITE_COINS:
        p = raw_data[sym]['USD']['PRICE']
        c = raw_data[sym]['USD']['CHANGEPCT24HOUR']
        
        # 🟢 PURI ENTRY (Psychological Buy Zone - 6% Drop)
        puri_entry = p * 0.941 #
        
        # 🔴 ZED ZONE (Fake Pump / Exit Area - 3% Up)
        zed_zone = p * 1.032 #

        # RENDER CLEAN INTERFACE
        st.markdown(f"""
        <div class="card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <b style="font-size:24px;" class="neon-text">{sym}/USDT</b>
                <span style="border:1px solid #00f2ff; padding:2px 8px; border-radius:5px; font-size:12px;">3-AI IQ SYNC</span>
            </div>
            <div class="price">${p:,.2f} <small style="color:{'#00ff88' if c>=0 else '#ff4b4b'}">{c:+.2f}%</small></div>
            
            <div style="display:flex; justify-content:space-between; margin: 15px 0;">
                <div class="zone-box" style="border-color:#ff4b4b;">
                    <small style="color:#ff4b4b;">ZED ZONE (SELL)</small><br>
                    <b style="font-size:18px;">${zed_zone:,.2f}</b>
                </div>
                <div class="zone-box" style="border-color:#00ff88;">
                    <small style="color:#00ff88;">PURI ENTRY (BUY)</small><br>
                    <b style="font-size:18px;">${puri_entry:,.2f}</b>
                </div>
            </div>
            
            <div style="background:rgba(0,242,255,0.05); padding:12px; border-radius:10px; border-left:4px solid #00f2ff;">
                <b style="color:#00f2ff;">🧠 RESEARCH VERDICT:</b><br>
                <span style="font-size:13px; color:#ccc;">
                    Delhi Session ke 12-hour cycle ke mutabiq retailers ko <b>Zed Zone</b> par fasaaya jayega. 
                    <b>Asli kharidari</b> tab karni hai jab market <b>${puri_entry:,.2f}</b> par aaye.
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

except Exception as e:
    st.error("📡 CONNECTION ERROR. REFRESHING DATA...")
