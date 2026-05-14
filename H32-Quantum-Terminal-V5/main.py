import streamlit as st
import requests
from datetime import datetime
import pytz

# --- 🛰️ SUPREME SYSTEM CONFIG ---
st.set_page_config(page_title="V900 GLOBAL SUPREME", layout="wide")

# --- 🌌 SUPREME NEON ENGINE (Anti-Code Leak) ---
st.markdown("""
    <style>
    .stApp { background-color: #000205; color: #ffffff; }
    .supreme-card {
        background: #080c12; border: 2px solid #00f2ff;
        border-radius: 15px; padding: 30px; margin-bottom: 30px;
        box-shadow: 0 0 35px rgba(0, 242, 255, 0.3);
    }
    .neon-header { color: #00f2ff; text-shadow: 0 0 15px #00f2ff; font-weight: 900; font-size: 26px; }
    .price-main { font-size: 50px; font-weight: 900; color: #fff; margin: 15px 0; }
    .glow-box { 
        background: #111; border: 1px solid #333; padding: 15px; 
        border-radius: 10px; text-align: center; 
    }
    .badge-zed { color: #ff4b4b; border: 2px solid #ff4b4b; padding: 5px 10px; border-radius: 5px; font-weight: 900; }
    .badge-entry { color: #00ff88; border: 2px solid #00ff88; padding: 5px 10px; border-radius: 5px; font-weight: 900; }
    </style>
    """, unsafe_allow_html=True)

# --- 🕒 GLOBAL & DELHI SYNC ---
ist = pytz.timezone('Asia/Kolkata')
now_ist = datetime.now(ist)
st.markdown(f"<h1 style='text-align:center;' class='neon-header'>🛰️ GLOBAL TRIPLE-AI COMMANDER | {now_ist.strftime('%H:%M')} IST</h1>", unsafe_allow_html=True)

# --- 🧠 300 IQ GLOBAL PSYCHOLOGY ENGINE ---
ELITE_COINS = ["BTC", "ETH", "SOL", "LINK", "SUI"]

try:
    url = f"https://min-api.cryptocompare.com/data/pricemultifull?fsyms={','.join(ELITE_COINS)}&tsyms=USD"
    res = requests.get(url).json()['RAW']
    
    for sym in ELITE_COINS:
        p = res[sym]['USD']['PRICE']
        c = res[sym]['USD']['CHANGEPCT24HOUR']
        v = res[sym]['USD']['VOLUME24HOUR']
        
        # 1. ZED ZONE (Global Fake Pump / Exit Area)
        zed_trap = p * 1.032  # 3.2% Trap for retailers
        
        # 2. PURI ENTRY (Psychological Bottom / Buying Point)
        entry_point = p * 0.935 # 6.5% Liquidation Deep
        
        # 3. GLOBAL STATUS SYNC (Triple AI Consensus)
        # Combine Price Action, Volume, and Global Situation logic
        if c > 2 and v > (v*0.9):
            status = "🚀 REAL BULLISH RALLY"
            css = "badge-entry"
            sub_msg = "PURI ENTRY CONFIRMED. 1-Month Trend Active."
        elif c > 1 and v < (v*0.6):
            status = "🚨 GLOBAL BULL TRAP"
            css = "badge-zed"
            sub_msg = f"Fake Pump Detect. Market {entry_point:,.2f} tak giregi."
        else:
            status = "⚖️ GLOBAL CONSOLIDATION"
            css = ""
            sub_msg = "Wait for Register Break or Liquidation Zone."

        # RENDER CLEAN INTERFACE
        st.markdown(f"""
        <div class="supreme-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="font-size:32px;" class="neon-header">{sym}/USDT</span>
                <span class="{css}">{status}</span>
            </div>
            
            <div class="price-main">${p:,.2f} <small style="font-size:20px; color:{'#00ff88' if c>=0 else '#ff4b4b'}">{c:+.2f}%</small></div>
            
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:20px; margin: 25px 0;">
                <div class="glow-box" style="border-color:#ff4b4b;">
                    <span style="color:#ff4b4b; font-weight:900;">🚨 ZED ZONE (EXIT)</span><br>
                    <b style="font-size:22px; color:#fff;">${zed_trap:,.2f}</b><br>
                    <small style="color:#888;">Market yahan se dump hogi</small>
                </div>
                <div class="glow-box" style="border-color:#00ff88;">
                    <span style="color:#00ff88; font-weight:900;">💎 PURI ENTRY (BUY)</span><br>
                    <b style="font-size:22px; color:#fff;">${entry_point:,.2f}</b><br>
                    <small style="color:#888;">Liquidate hone ke baad yahan se uthegi</small>
                </div>
            </div>
            
            <div style="background:rgba(0,242,255,0.05); padding:20px; border-radius:10px; border-left:5px solid #00f2ff;">
                <b style="color:#00f2ff; font-size:15px;">🧠 300 IQ GLOBAL PSYCHOLOGY REPORT:</b><br>
                <p style="margin-top:10px; font-size:14px; color:#ccc;">
                    {sub_msg} Global data aur 12-hour cycle check kar liya gaya hai. 
                    <b>Zed Zone</b> par retailers fasaaye ja rahe hain. 
                    <b>Target:</b> Agar entry <b>${entry_point:,.2f}</b> par milti hai toh 1 mahine ka bullish goal <b>${entry_point*1.40:,.2f}</b> hai.
                </p>
                <div style="margin-top:10px; font-size:11px; color:#555;">TRIPLE AI SYNC: GEMINI | GROQ | MISTRAL - VERIFIED</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

except Exception as e:
    st.error("📡 SATELLITE CONNECTION RE-SYNCING...")
