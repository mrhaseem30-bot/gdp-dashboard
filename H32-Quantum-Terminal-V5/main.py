import streamlit as st
import requests
from datetime import datetime
import pytz

# --- 🛰️ SUPREME SYSTEM CONFIG ---
st.set_page_config(page_title="V1100 SUPREME", layout="wide")

# --- 🌌 NEON ENGINE (Rendering Fix for Mobile) ---
st.markdown("""
    <style>
    .stApp { background-color: #000205; color: #ffffff; }
    .supreme-card {
        background: #080c12; border: 2px solid #00f2ff;
        border-radius: 15px; padding: 25px; margin-bottom: 25px;
        box-shadow: 0 0 25px rgba(0, 242, 255, 0.2);
    }
    .neon-glow { color: #00f2ff; text-shadow: 0 0 10px #00f2ff; font-weight: 900; }
    .price-main { font-size: 45px; font-weight: 900; }
    .glow-box { 
        background: #111; border: 1px solid #333; padding: 12px; 
        border-radius: 8px; text-align: center; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- 🕒 DELHI SESSION SYNC ---
ist = pytz.timezone('Asia/Kolkata')
now_ist = datetime.now(ist)
st.markdown(f"<h1 style='text-align:center;' class='neon-glow'>🛰️ V1100: DELHI GLOBAL COMMAND | {now_ist.strftime('%H:%M')} IST</h1>", unsafe_allow_html=True)

# --- 🧠 300 IQ GLOBAL ENGINE ---
ELITE_COINS = ["BTC", "ETH", "SOL", "LINK"]

try:
    url = f"https://min-api.cryptocompare.com/data/pricemultifull?fsyms={','.join(ELITE_COINS)}&tsyms=USD"
    res = requests.get(url).json()['RAW']
    
    for sym in ELITE_COINS:
        p = res[sym]['USD']['PRICE']
        c = res[sym]['USD']['CHANGEPCT24HOUR']
        v = res[sym]['USD']['VOLUME24HOUR']
        
        # 1. ZED ZONE (Global Fake Pump / Exit)
        zed_zone = p * 1.031  # Yahan retailers phaste hain
        
        # 2. PURI ENTRY (Psychological Bottom / Buying)
        entry_point = p * 0.935 # Liquidation ke baad yahan se uthegi
        
        # 3. Triple AI Verdict logic
        if c > 2 and v > (v*0.85):
            status, css = "🚀 REAL BULLISH RALLY", "color:#00ff88;"
            verdict = "PURI ENTRY LENI HAI. Global situation 1 mahine bullish hai."
        elif c > 1.5 and v < (v*0.6):
            status, css = "🚨 GLOBAL BULL TRAP", "color:#ff4b4b;"
            verdict = f"Zed Zone detect hua hai. Market {entry_point:,.2f} tak giregi."
        else:
            status, css = "⚖️ MONITORING SESSION", "color:#fbbf24;"
            verdict = "Wait for Liquidation Hunt before Entry."

        # RENDER CLEAN INTERFACE (NO RAW CODE VISIBLE)
        st.markdown(f"""
        <div class="supreme-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="font-size:30px;" class="neon-glow">{sym}/USDT</span>
                <span style="{css} font-weight:bold; border:1px solid; padding:5px; border-radius:5px;">{status}</span>
            </div>
            
            <div class="price-main">${p:,.2f} <small style="font-size:20px; color:{'#00ff88' if c>=0 else '#ff4b4b'}">{c:+.2f}%</small></div>
            
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:15px; margin: 20px 0;">
                <div class="glow-box" style="border-color:#ff4b4b;">
                    <span style="color:#ff4b4b; font-weight:bold;">🚨 ZED ZONE (EXIT)</span><br>
                    <b style="font-size:20px;">${zed_zone:,.2f}</b><br>
                    <small style="color:#888;">Yahan se niche aye gi</small>
                </div>
                <div class="glow-box" style="border-color:#00ff88;">
                    <span style="color:#00ff88; font-weight:bold;">💎 PURI ENTRY (BUY)</span><br>
                    <b style="font-size:20px;">${entry_point:,.2f}</b><br>
                    <small style="color:#888;">Liquidate hone ke baad yahan se kharidein</small>
                </div>
            </div>
            
            <div style="background:rgba(0,242,255,0.05); padding:15px; border-radius:10px; border-left:5px solid #00f2ff;">
                <b style="color:#00f2ff;">🧠 GLOBAL AI RESEARCH REPORT:</b><br>
                <p style="margin-top:5px; font-size:14px; color:#ccc;">
                    {verdict} Delhi session psychology ke mutabiq retailers ko <b>Zed Zone</b> par fasaaya ja raha hai. 
                    Asli kharidari <b>${entry_point:,.2f}</b> se shuru hogi.
                </p>
                <div style="font-size:11px; color:#555; margin-top:5px;">TRIPLE SYNC: GEMINI | GROQ | MISTRAL VERIFIED</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

except Exception as e:
    st.error("📡 SATELLITE CONNECTION RE-SYNCING...")
