import streamlit as st
import requests

# --- 🛰️ SUPREME SYSTEM CONFIG ---
st.set_page_config(page_title="V600 SUPREME", layout="wide")

# --- 🌌 NEON CSS (Fixed Rendering) ---
st.markdown("""
    <style>
    .stApp { background-color: #000205; color: #ffffff; }
    .supreme-container {
        background: #080c12; border: 2px solid #00f2ff;
        border-radius: 15px; padding: 25px; margin-bottom: 25px;
        box-shadow: 0 0 25px rgba(0, 242, 255, 0.2);
    }
    .neon-header { color: #00f2ff; text-shadow: 0 0 10px #00f2ff; font-weight: 900; font-size: 24px; }
    .price-tag { font-size: 40px; font-weight: 900; margin: 10px 0; color: #ffffff; }
    .glow-box { 
        background: #111; border: 1px solid #333; padding: 10px; 
        border-radius: 8px; text-align: center; 
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;' class='neon-header'>🛰️ TERMINAL: GOD-MODE V600</h1>", unsafe_allow_html=True)

# --- 🧠 300 IQ DEEP ENGINE ---
ELITE_COINS = ["BTC", "ETH", "SOL", "LINK"]

try:
    url = f"https://min-api.cryptocompare.com/data/pricemultifull?fsyms={','.join(ELITE_COINS)}&tsyms=USD"
    data = requests.get(url).json()['RAW']
    
    for sym in ELITE_COINS:
        p = data[sym]['USD']['PRICE']
        c = data[sym]['USD']['CHANGEPCT24HOUR']
        
        # Genius Levels
        liq_trap = p * 0.92
        reg_break = p * 1.08
        
        # Render clean UI without showing raw code
        st.markdown(f"""
        <div class="supreme-container">
            <div style="display:flex; justify-content:space-between;">
                <span class="neon-header">{sym}/USDT</span>
                <span style="color:#00f2ff; font-weight:bold;">⚖️ MONITORING</span>
            </div>
            <div class="price-tag">${p:,.2f} <small style="font-size:20px; color:{'#00ff88' if c>=0 else '#ff4b4b'}">{c:+.2f}%</small></div>
            
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:15px; margin: 15px 0;">
                <div class="glow-box" style="border-color:#ff4b4b;">
                    <small style="color:#888;">LIQ TRAP AREA</small><br>
                    <b style="color:#ff4b4b;">${liq_trap:,.2f}</b>
                </div>
                <div class="glow-box" style="border-color:#00f2ff;">
                    <small style="color:#888;">REGISTER BREAK</small><br>
                    <b style="color:#00f2ff;">${reg_break:,.2f}</b>
                </div>
            </div>
            
            <div style="background:rgba(0,242,255,0.05); padding:15px; border-radius:8px; border-left:4px solid #00f2ff;">
                <b style="color:#00f2ff;">🧠 SUPREME VERDICT:</b><br>
                Wait for <b>${reg_break:,.2f}</b> breakout with high volume for a 1-month bullish rally.
            </div>
        </div>
        """, unsafe_allow_html=True)

except Exception as e:
    st.error("📡 SATELLITE SYNCING...")
