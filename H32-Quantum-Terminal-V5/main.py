import streamlit as st
import requests
from datetime import datetime
import pytz

# --- 🛰️ SUPREME SYSTEM CONFIG ---
st.set_page_config(page_title="V1300 SUPREME", layout="wide")

# --- 🌌 NEON ENGINE (Anti-Leak Fix) ---
st.markdown("""
<style>
    .stApp { background-color: #000205; color: #ffffff; }
    .supreme-card {
        background: #080c12; border: 2px solid #00f2ff;
        border-radius: 12px; padding: 20px; margin-bottom: 25px;
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.2);
    }
    .neon-text { color: #00f2ff; text-shadow: 0 0 8px #00f2ff; font-weight: 900; }
    .price-val { font-size: 40px; font-weight: 900; margin: 10px 0; }
    .grid-wrap { display: flex; gap: 10px; margin: 15px 0; }
    .box-stat { 
        background: #111; border: 1px solid #333; flex: 1; padding: 10px; 
        border-radius: 8px; text-align: center; 
    }
</style>
""", unsafe_allow_html=True)

# --- 🕒 DELHI SESSION SYNC ---
ist = pytz.timezone('Asia/Kolkata')
now_ist = datetime.now(ist)
st.markdown(f"<h1 style='text-align:center;' class='neon-text'>🛰️ V1300 DELHI GLOBAL COMMAND</h1>", unsafe_allow_html=True)

# --- 🧠 300 IQ TRIPLE-AI ENGINE ---
ELITE_COINS = ["BTC", "ETH", "SOL", "LINK"]

try:
    # API Research Pull
    url = "https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,ETH,SOL,LINK&tsyms=USD"
    data = requests.get(url).json()['RAW']
    
    for sym in ELITE_COINS:
        p = data[sym]['USD']['PRICE']
        c = data[sym]['USD']['CHANGEPCT24HOUR']
        
        # Psychology Levels
        zed_zone = p * 1.025  # Fake Pump Area
        puri_entry = p * 0.945 # Real Liquidation Bottom
        
        # Clean Logic Block (Fixed for Mobile)
        status = "🚀 RALLY" if c > 1.5 else "🚨 TRAP" if c > 1 and p > zed_zone*0.98 else "⚖️ CONSOL"
        
        card_html = f"""
        <div class="supreme-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <b style="font-size:24px;" class="neon-text">{sym}/USDT</b>
                <span style="border:1px solid #00f2ff; padding:2px 10px; border-radius:15px; font-size:12px;">{status}</span>
            </div>
            <div class="price-val">${p:,.2f} <small style="color:{'#00ff88' if c>=0 else '#ff4b4b'}">{c:+.2f}%</small></div>
            
            <div class="grid-wrap">
                <div class="box-stat" style="border-color:#ff4b4b;">
                    <small style="color:#888;">ZED ZONE (EXIT)</small><br>
                    <b style="color:#ff4b4b;">${zed_zone:,.2f}</b>
                </div>
                <div class="box-stat" style="border-color:#00ff88;">
                    <small style="color:#888;">PURI ENTRY (BUY)</small><br>
                    <b style="color:#00ff88;">${puri_entry:,.2f}</b>
                </div>
            </div>
            
            <div style="background:rgba(0,242,255,0.05); padding:12px; border-radius:8px; border-left:4px solid #00f2ff;">
                <b style="color:#00f2ff; font-size:14px;">🧠 GLOBAL AI RESEARCH:</b><br>
                <span style="font-size:13px;">Wait for <b>Liquidation</b> at ${puri_entry:,.2f}. Zed Zone par retailers fasaaye ja rahe hain, wahan sell karein.</span>
            </div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)

except Exception as e:
    st.error("📡 SATELLITE SYNCING...")
