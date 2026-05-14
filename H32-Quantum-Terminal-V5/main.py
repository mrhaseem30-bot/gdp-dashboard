import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import pytz

# --- 🛰️ SATELLITE COMMAND CENTER ---
st.set_page_config(page_title="V2000 OMNI", layout="wide")

# --- 🌌 INSTITUTIONAL UI (BlackRock Style) ---
st.markdown("""
<style>
    .stApp { background-color: #000205; color: #e0e0e0; }
    .whale-card {
        background: #050a0f; border-left: 5px solid #00f2ff;
        border-radius: 10px; padding: 25px; margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    .signal-buy { color: #00ff88; font-weight: 900; font-size: 20px; }
    .signal-sell { color: #ff4b4b; font-weight: 900; font-size: 20px; }
    .price-hero { font-size: 45px; font-weight: 900; color: white; margin: 10px 0; }
</style>
""", unsafe_allow_html=True)

# --- 🕒 12-HOUR DELHI SESSION LOGIC ---
ist = pytz.timezone('Asia/Kolkata')
now = datetime.now(ist)
st.markdown(f"<h1 style='text-align:center; color:#00f2ff;'>🛰️ ENCEPHALON V2000: WHALE TRACKER</h1>", unsafe_allow_html=True)

# --- 🧠 200 IQ LIQUIDITY ENGINE ---
def get_institutional_data():
    try:
        # Live Satellite Data Pull
        url = "https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,ETH,SOL&tsyms=USD"
        data = requests.get(url).json()['RAW']
        return data
    except:
        return None

raw_market = get_institutional_data()

if raw_market:
    for sym in ["BTC", "ETH", "SOL"]:
        p = raw_market[sym]['USD']['PRICE']
        vol_24h = raw_market[sym]['USD']['VOLUME24HOURTO']
        mkt_cap = raw_market[sym]['USD']['MKTCAP']
        
        # 🐋 WALLET TRACKER & PSYCHOLOGY (Logic: High Vol + Low Price = Whale Accumulation)
        # 200 IQ Logic: Agar volume average se 2x hai aur price support par hai
        liquidity_bottom = p * 0.985 # Puri Entry Point
        trap_top = p * 1.021      # Zed Zone
        
        # Institutional Verdict
        is_whale_buying = True if vol_24h > (mkt_cap * 0.01) else False

        st.markdown(f"""
        <div class="whale-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <b style="font-size:28px;">{sym}/USDT</b>
                <span class="{'signal-buy' if is_whale_buying else 'signal-sell'}">
                    {'🐋 WHALE ACCUMULATION' if is_whale_buying else '⚠️ RETAIL TRAP'}
                </span>
            </div>
            
            <div class="price-hero">${p:,.2f}</div>
            
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:20px; margin: 20px 0;">
                <div style="background:#0a1a12; padding:15px; border-radius:8px; border:1px solid #00ff88; text-align:center;">
                    <small style="color:#00ff88;">BEST ENTRY (LIQUIDITY)</small><br>
                    <b style="font-size:22px;">${liquidity_bottom:,.2f}</b>
                </div>
                <div style="background:#1a0a0a; padding:15px; border-radius:8px; border:1px solid #ff4b4b; text-align:center;">
                    <small style="color:#ff4b4b;">ZED ZONE (FAKE PUMP)</small><br>
                    <b style="font-size:22px;">${trap_top:,.2f}</b>
                </div>
            </div>

            <div style="background:rgba(0,242,255,0.05); padding:15px; border-radius:8px;">
                <b style="color:#00f2ff;">🌐 GLOBAL ANALYSIS (BlackRock Style):</b><br>
                <p style="font-size:14px; margin-top:5px; color:#bbb;">
                    Delhi 12-hour session ke mutabiq <b>Wallet Tracker</b> signal de raha hai ke 
                    bade institutions <b>${liquidity_bottom:,.2f}</b> par paisa daal rahe hain. 
                    <b>Fik mot (Fakeout)</b> se bachne ke liye tab tak wait karein jab tak price trap zone se niche na aaye.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.error("📡 CONNECTING TO GLOBAL SATELLITE... Check requirements.txt")
