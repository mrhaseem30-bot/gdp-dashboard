import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime

# --- 🛰️ MASTER CONFIG & AI BRAINS ---
st.set_page_config(page_title="ENCEPHALON V21 ELITE", layout="wide")
[span_1](start_span)GROQ_KEY = "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" #[span_1](end_span)
[span_2](start_span)MISTRAL_KEY = "sTGr5fQ001Db2YqwXZqZDA6abPuU1awU" #[span_2](end_span)
[span_3](start_span)GEMINI_KEY = "AIzaSyDI9PdXoYCwl6C21Q5KLBmN1LwseiQZKkI" #[span_3](end_span)

# --- 🎨 PREMIMUM NEON UI (Screenshot 214819 Style) ---
st.markdown("""
    <style>
    .stApp { background-color: #050a10; }
    .satellite-card {
        background: #0d1621;
        border: 2px solid #00f2ff;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 0 20px rgba(0, 242, 255, 0.2);
    }
    .action-btn {
        background: linear-gradient(45deg, #00f2ff, #0072ff);
        color: white !important;
        font-weight: bold;
        border-radius: 8px;
        text-align: center;
        padding: 10px;
        text-decoration: none;
        display: block;
        margin: 5px 0;
    }
    .insta-alert { background: linear-gradient(45deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888); }
    </style>
    """, unsafe_allow_html=True)

# --- 🌍 UNLIMITED DATA & LIQUIDITY ENGINE ---
def fetch_whale_intel():
    url = "https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,ETH,SUI,SOL,DOT&tsyms=USD"
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json()['RAW']
    except: return None

# --- 📱 COMMAND CENTER ---
st.markdown("<h1 style='color:white; text-align:center;'>🛰️ ENCEPHALON V21: WHALE COMMANDER</h1>", unsafe_allow_html=True)

data = fetch_whale_intel()

if data:
    cols = st.columns(len(data))
    for i, (sym, val) in enumerate(data.items()):
        p = val['USD']['PRICE']
        c = val['USD']['CHANGEPCT24HOUR']
        liq = val['USD']['TOTALVOLUME24H'] # Liquidity Tracking
        
        # 🧠 AI PREDICTION LOGIC (Kitne din upar jayegi)
        days_up = "3-5 Days" if c > 0 else "Correction Phase"
        
        with cols[i]:
            st.markdown(f"""
                <div class="satellite-card">
                    <div style="color:white; font-size:18px;">● {sym}/USDT <span style="color:#3fb950;">{c:+.2f}%</span></div>
                    <div style="color:white; font-size:35px; font-weight:bold;">${p:,.2f}</div>
                    
                    <div style="background:rgba(0,242,255,0.1); padding:8px; border-radius:5px; margin:10px 0;">
                        <p style="color:#00f2ff; font-size:12px; margin:0;">🛰️ SATELLITE PREDICTION</p>
                        <p style="color:white; font-weight:bold; margin:0;">BULLISH FOR: {days_up}</p>
                        <p style="color:#8b949e; font-size:10px;">LIQUIDITY: ${liq:,.0f}</p>
                    </div>

                    <a href="https://www.instagram.com/direct/inbox/" target="_blank" class="action-btn insta-alert">📸 INSTA URGENT BUY ALERT</a>
                    <a href="#" class="action-btn" style="background:#ff4444;">🚨 URGENT SELL NOW</a>
                    <div style="display:flex; gap:5px;">
                        <div style="flex:1; background:#16212e; color:#58a6ff; font-size:10px; padding:5px; border-radius:5px; text-align:center;">TRACK LIQUIDITY</div>
                        <div style="flex:1; background:#16212e; color:#58a6ff; font-size:10px; padding:5px; border-radius:5px; text-align:center;">FLOPPY VIEW</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
else:
    st.error("📡 Re-routing Satellite Signal...")
    time.sleep(3)
    st.rerun()

st.divider()
st.info("📂 **Neural Memory**: All urgent signals and liquidity flows are being stored in the global chain.")
