import streamlit as st
import requests
from datetime import datetime
import pytz

# --- 🛰️ SUPREME SYSTEM CONFIG ---
st.set_page_config(page_title="V1200 SUPREME", layout="wide")

# --- 🌌 STABLE NEON ENGINE (Fixed All Rendering Issues) ---
st.markdown("""
    <style>
    .stApp { background-color: #000205; color: #ffffff; }
    .supreme-container {
        background: #080c12; border: 2px solid #00f2ff;
        border-radius: 12px; padding: 20px; margin-bottom: 25px;
        box-shadow: 0 0 20px rgba(0, 242, 255, 0.2);
    }
    .neon-glow { color: #00f2ff; text-shadow: 0 0 8px #00f2ff; font-weight: 900; }
    .price-text { font-size: 42px; font-weight: 900; margin: 10px 0; }
    .box-grid { display: flex; gap: 10px; justify-content: space-between; margin-top: 15px; }
    .data-box { 
        background: #111; border: 1px solid #333; flex: 1; padding: 10px; 
        border-radius: 8px; text-align: center; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- 🕒 GLOBAL SYNC ---
ist = pytz.timezone('Asia/Kolkata')
now_ist = datetime.now(ist)
st.markdown(f"<h2 style='text-align:center;' class='neon-glow'>🛰️ V1200: GLOBAL TRIPLE-AI COMMAND</h2>", unsafe_allow_html=True)

# --- 🧠 300 IQ GLOBAL RESEARCH ENGINE ---
ELITE_COINS = ["BTC", "ETH", "SOL", "DOT", "LINK"]

try:
    url = "https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,ETH,SOL,DOT,LINK&tsyms=USD"
    res = requests.get(url).json()['RAW']
    
    for sym in ELITE_COINS:
        p = res[sym]['USD']['PRICE']
        c = res[sym]['USD']['CHANGEPCT24HOUR']
        
        # RESEARCH DATA: Zed Zone & Entry Hunt
        zed_exit = p * 1.028   # 2.8% Fake Pump Trap
        puri_entry = p * 0.942 # 5.8% Liquidation Hunt
        
        # UI Rendering without Code Leaks
        ui_block = f"""
        <div class="supreme-container">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="font-size:26px;" class="neon-glow">{sym}/USDT</span>
                <span style="border:1px solid #00f2ff; padding:2px 8px; border-radius:4px; font-size:12px;">GLOBAL AI SYNC</span>
            </div>
            
            <div class="price-text">${p:,.2f} <span style="font-size:18px; color:{'#00ff88' if c>=0 else '#ff4b4b'}">{c:+.2f}%</span></div>
            
            <div class="box-grid">
                <div class="data-box" style="border-color:#ff4b4b;">
                    <small style="color:#888;">ZED ZONE (EXIT)</small><br>
                    <b style="color:#ff4b4b; font-size:18px;">${zed_exit:,.2f}</b>
                </div>
                <div class="data-box" style="border-color:#00ff88;">
                    <small style="color:#888;">PURI ENTRY (BUY)</small><br>
                    <b style="color:#00ff88; font-size:18px;">${puri_entry:,.2f}</b>
                </div>
            </div>
            
            <div style="background:rgba(0,242,255,0.05); padding:12px; border-radius:8px; margin-top:15px; border-left:4px solid #00f2ff;">
                <b style="color:#00f2ff; font-size:14px;">🧠 DELHI SESSION PSYCHOLOGY:</b><br>
                <span style="font-size:13px; color:#ccc;">
                    Wait for <b>Liquidation Hunt</b> at ${puri_entry:,.2f}. 
                    Asli kharidari wahan se hogi. Zed Zone par 100% exit karein.
                </span>
            </div>
        </div>
        """
        st.markdown(ui_block, unsafe_allow_html=True)

except Exception as e:
    st.error(f"📡 SATELLITE ERROR: {e}")
