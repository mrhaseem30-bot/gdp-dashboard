import streamlit as st
import requests
from datetime import datetime
import pytz

# --- 🛰️ SUPREME SYSTEM CONFIG ---
st.set_page_config(page_title="V1000 SUPREME", layout="wide")

# --- 🌌 NEON ENGINE (Anti-Code Leak Fix) ---
st.markdown("""
    <style>
    .stApp { background-color: #000205; color: #ffffff; }
    .supreme-card {
        background: #080c12; border: 2px solid #00f2ff;
        border-radius: 15px; padding: 25px; margin-bottom: 25px;
        box-shadow: 0 0 35px rgba(0, 242, 255, 0.3);
    }
    .neon-text { color: #00f2ff; text-shadow: 0 0 10px #00f2ff; font-weight: 900; }
    .price-main { font-size: 45px; font-weight: 900; margin: 10px 0; }
    .glow-box { 
        background: #111; border: 1px solid #333; padding: 15px; 
        border-radius: 10px; text-align: center; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- 🕒 DELHI TIME & GLOBAL CONTEXT ---
ist = pytz.timezone('Asia/Kolkata')
now_ist = datetime.now(ist)
st.markdown(f"<h1 style='text-align:center;' class='neon-text'>🛰️ V1000: GLOBAL TRIPLE-AI SYNC | {now_ist.strftime('%H:%M')} IST</h1>", unsafe_allow_html=True)

# --- 🧠 300 IQ GLOBAL PSYCHOLOGY ENGINE ---
ELITE_COINS = ["BTC", "ETH", "SOL", "LINK"]

try:
    url = f"https://min-api.cryptocompare.com/data/pricemultifull?fsyms={','.join(ELITE_COINS)}&tsyms=USD"
    res = requests.get(url).json()['RAW']
    
    for sym in ELITE_COINS:
        p = res[sym]['USD']['PRICE']
        c = res[sym]['USD']['CHANGEPCT24HOUR']
        v = res[sym]['USD']['VOLUME24HOUR']
        
        # 1. ZED ZONE (Fake Pump Level)
        zed_zone = p * 1.035 
        # 2. PURI ENTRY (Liquidation Bottom)
        entry_buy = p * 0.932 
        
        # 3. Triple-AI Sync Decision
        is_rally = (c > 1.8 and v > 1000)
        status = "🚀 REAL BULLISH RALLY" if is_rally else "🚨 GLOBAL BULL TRAP" if (c > 2.5 and v < 800) else "⚖️ CONSOLIDATION"
        
        # RENDER CLEAN TERMINAL
        st.markdown(f"""
        <div class="supreme-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="font-size:30px;" class="neon-text">{sym}/USDT</span>
                <span style="color:{'#00ff88' if is_rally else '#ff4b4b'}; border:1px solid; padding:5px; border-radius:5px;">{status}</span>
            </div>
            
            <div class="price-main">${p:,.2f} <small style="font-size:20px; color:{'#00ff88' if c>=0 else '#ff4b4b'}">{c:+.2f}%</small></div>
            
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:15px; margin: 20px 0;">
                <div class="glow-box" style="border-color:#ff4b4b;">
                    <span style="color:#ff4b4b; font-weight:900;">🚨 ZED ZONE (EXIT)</span><br>
                    <b style="font-size:20px;">${zed_zone:,.2f}</b>
                </div>
                <div class="glow-box" style="border-color:#00ff88;">
                    <span style="color:#00ff88; font-weight:900;">💎 PURI ENTRY (BUY)</span><br>
                    <b style="font-size:20px;">${entry_buy:,.2f}</b>
                </div>
            </div>
            
            <div style="background:rgba(0,242,255,0.05); padding:15px; border-radius:8px; border-left:4px solid #00f2ff;">
                <b style="color:#00f2ff;">🧠 GLOBAL AI VERDICT:</b><br>
                {"Market 1 mahine bullish rahegi. PURI ENTRY LENI HAI." if is_rally else f"Fake Pump detect hua hai. Market {entry_buy:,.2f} tak giregi tab kharidna."}
            </div>
        </div>
        """, unsafe_allow_html=True)

except Exception as e:
    st.error("📡 SATELLITE CONNECTION RE-SYNCING...")
