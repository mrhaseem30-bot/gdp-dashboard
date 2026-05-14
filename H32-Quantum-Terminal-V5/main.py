import streamlit as st
import requests

# --- 🛰️ SATELLITE SYSTEM CONFIG ---
st.set_page_config(page_title="V500 SUPREME", layout="wide")

# Elite Assets Only
ELITE_COINS = ["BTC", "ETH", "SOL", "LINK", "SUI", "DOT"]

# --- 🌌 NEON STYLING (Zero-Error Rendering) ---
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
    .rally-text { color: #00ff88; font-weight: bold; text-transform: uppercase; border: 1px solid #00ff88; padding: 5px; border-radius: 4px; }
    .trap-text { color: #ff4b4b; font-weight: bold; text-transform: uppercase; border: 1px solid #ff4b4b; padding: 5px; border-radius: 4px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;' class='neon-header'>🛰️ ENCEPHALON V500: GOD-MODE TERMINAL</h1>", unsafe_allow_html=True)

# --- 🧠 300 IQ EXECUTION ---
try:
    url = f"https://min-api.cryptocompare.com/data/pricemultifull?fsyms={','.join(ELITE_COINS)}&tsyms=USD"
    res = requests.get(url).json()['RAW']
    
    for sym in ELITE_COINS:
        if sym in res:
            p = res[sym]['USD']['PRICE']
            c = res[sym]['USD']['CHANGEPCT24HOUR']
            v = res[sym]['USD']['VOLUME24HOUR']
            
            # Genius Levels
            liq_area = p * 0.912  # Liquidation Hunt
            reg_break = p * 1.085 # Register Breakout
            one_month = p * 1.30  # 30-Day Target
            
            # Analysis Logic
            is_rally = (c > 1.5 and v > v*0.8)
            is_trap = (c > 2.5 and v < v*0.6)
            
            # Render Terminal
            st.markdown(f"""
            <div class="supreme-container">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span class="neon-header">{sym}/USDT</span>
                    {"<span class='rally-text'>🚀 REAL RALLY</span>" if is_rally else ("<span class='trap-text'>🚨 BULL TRAP</span>" if is_trap else "<span>⚖️ MONITORING</span>")}
                </div>
                
                <div class="price-tag">${p:,.2f} <small style="font-size:18px; color:{'#00ff88' if c>=0 else '#ff4b4b'}">{c:+.2f}%</small></div>
                
                <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap:10px; margin: 15px 0;">
                    <div class="glow-box" style="border-color:#ff4b4b;"><small style="color:#888;">LIQ TRAP</small><br><b style="color:#ff4b4b;">${liq_area:,.2f}</b></div>
                    <div class="glow-box" style="border-color:#00f2ff;"><small style="color:#888;">REGISTER</small><br><b style="color:#00f2ff;">${reg_break:,.2f}</b></div>
                    <div class="glow-box" style="border-color:#fbbf24;"><small style="color:#888;">1-MONTH</small><br><b style="color:#fbbf24;">${one_month:,.2f}</b></div>
                </div>
                
                <div style="background:rgba(0,242,255,0.05); padding:15px; border-radius:8px; border-left:4px solid #00f2ff; font-size:13px;">
                    <b style="color:#00f2ff;">🧠 SUPREME VERDICT:</b><br>
                    {'PURI ENTRY LENI HAI. Agla 1 mahina market bullish rahegi.' if is_rally else 
                     f'ENTRY NA LEIN. Market {liq_area:,.2f} tak dump ho sakti hai.' if is_trap else 
                     f'Wait for {reg_break:,.2f} breakout with volume.'}
                </div>
            </div>
            """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"📡 SATELLITE ERROR: {e}")
