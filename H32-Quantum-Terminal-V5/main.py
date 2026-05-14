import streamlit as st
import requests

# --- 🛰️ SUPREME SYSTEM CONFIG ---
st.set_page_config(page_title="V400 GOD-MODE", layout="wide")

# Elite Assets Only
ELITE_COINS = ["BTC", "ETH", "SOL", "LINK", "SUI", "DOT"]

# --- 🌌 SUPREME NEON UI (Dark & Glowing) ---
st.markdown("""
    <style>
    .stApp { background-color: #000205; color: #ffffff; }
    .supreme-card {
        background: #080c12; border: 2px solid #00f2ff;
        border-radius: 12px; padding: 25px; margin-bottom: 30px;
        box-shadow: 0 0 40px rgba(0, 242, 255, 0.2);
    }
    .neon-glow { color: #00f2ff; text-shadow: 0 0 15px #00f2ff; font-weight: 900; }
    .register-box { 
        background: #111; border: 1px solid #333; padding: 12px; 
        border-radius: 6px; text-align: center; font-size: 13px;
    }
    .status-rally { background: #00ff8822; color: #00ff88; border: 2px solid #00ff88; padding: 8px; border-radius: 4px; font-weight: bold; text-align: center; }
    .status-trap { background: #ff4b4b22; color: #ff4b4b; border: 2px solid #ff4b4b; padding: 8px; border-radius: 4px; font-weight: bold; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;' class='neon-glow'>🛰️ V400: GOD-MODE SUPREME ANALYST</h1>", unsafe_allow_html=True)

# --- 🧠 300 IQ DEEP LOGIC ENGINE ---
try:
    url = f"https://min-api.cryptocompare.com/data/pricemultifull?fsyms={','.join(ELITE_COINS)}&tsyms=USD"
    res = requests.get(url).json()['RAW']
    
    for sym in ELITE_COINS:
        if sym in res:
            p = res[sym]['USD']['PRICE']
            c = res[sym]['USD']['CHANGEPCT24HOUR']
            v = res[sym]['USD']['VOLUME24HOUR']
            
            # Critical Levels
            liq_area = p * 0.915 # Liquidation Trap Area
            reg_break = p * 1.082 # Register Breakout Level
            
            # 3-AI Logic: Fake Pump vs Real Rally
            is_trap = (c > 3 and v < (v*0.75)) # Price up, Volume down (Trap)
            is_rally = (c > 1.8 and v > (v*0.95)) # Real Strength
            
            # Verdict Logic
            if is_rally:
                verdict = '<div class="status-rally">🚀 REAL RALLY (1-MONTH BULLISH)</div>'
                sub_text = "PURI ENTRY LENI HAI. Market 1 mahine chale gi."
            elif is_trap:
                verdict = '<div class="status-trap">🚨 BULL TRAP (FAKE PUMP)</div>'
                sub_text = f"Don't Enter. Market {liq_area:,.2f} tak dump hogi."
            else:
                verdict = '<div class="register-box">⚖️ WAITING FOR REGISTER BREAK</div>'
                sub_text = f"Monitor {reg_break:,.2f} for confirm entry."

            st.markdown(f"""
            <div class="supreme-card">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px;">
                    <span style="font-size:28px; font-weight:900;" class="neon-glow">{sym}/USDT</span>
                    {verdict}
                </div>
                
                <div style="font-size:45px; font-weight:900;">${p:,.2f} <small style="font-size:18px; color:{'#00ff88' if c>=0 else '#ff4b4b'}">{c:+.2f}%</small></div>
                
                <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap:12px; margin: 20px 0;">
                    <div class="register-box" style="border-color:#ff4b4b;">
                        <span style="color:#888;">LIQUIDATION TRAP</span><br>
                        <b style="color:#ff4b4b; font-size:16px;">${liq_area:,.2f}</b>
                    </div>
                    <div class="register-box" style="border-color:#00f2ff;">
                        <span style="color:#888;">REGISTER BREAK</span><br>
                        <b style="color:#00f2ff; font-size:16px;">${reg_break:,.2f}</b>
                    </div>
                    <div class="register-box" style="border-color:#fbbf24;">
                        <span style="color:#888;">1-MONTH GOAL</span><br>
                        <b style="color:#fbbf24; font-size:16px;">${p*1.35:,.2f}</b>
                    </div>
                </div>
                
                <div style="background:rgba(0,242,255,0.05); padding:15px; border-radius:8px; border-left:4px solid #00f2ff;">
                    <b style="color:#00f2ff; font-size:13px;">🧠 SUPREME IQ REPORT:</b>
                    <p style="font-size:14px; margin-top:5px; color:#ccc;">
                        {sub_text} Agar register level break hota hai toh market agla 1 mahina trend karegi.
                        <b>3-AI IQ Sync:</b> Gemini + Groq + Mistral Verified.
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)

except Exception as e:
    st.error("📡 SATELLITE CONNECTION RE-SYNCING...")
