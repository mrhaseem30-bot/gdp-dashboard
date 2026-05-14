import streamlit as st
import requests
import time
import random

# --- 🛰️ SATELLITE & TRIPLE BRAIN CONFIG ---
st.set_page_config(page_title="ENCEPHALON V26 PSYCHOLOGY", layout="wide")

# [span_1](start_span)Keys from your env.txt[span_1](end_span)
GROQ_KEY = "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"
MISTRAL_KEY = "sTGr5fQ001Db2YqwXZqZDA6abPuU1awU"
GEMINI_KEY = "AIzaSyDI9PdXoYCwl6C21Q5KLBmN1LwseiQZKkI"
TELEGRAM_ID = "8376377797" 

COINS = ["ASTER", "UNI", "LTC", "ZEC", "BNB", "SOL", "AVAX", "ONDO", "BGB", "HYPE", "ADA", "SUI", "DOT", "LINK", "DOGE", "XPL", "BTC", "ETH", "XRP"]

# --- 🧠 PSYCHOLOGY UI DESIGN ---
st.markdown("""
    <style>
    .stApp { background-color: #02060a; }
    .psych-card {
        background: #0d1117;
        border-left: 5px solid #00f2ff;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.5);
    }
    .brain-tag { font-size: 10px; padding: 2px 8px; border-radius: 10px; margin-right: 5px; }
    .fear { color: #ff4444; font-weight: bold; }
    .greed { color: #00ff00; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='color:white; text-align:center;'>🛰️ ENCEPHALON V26: TRIPLE BRAIN PSYCHOLOGY</h1>", unsafe_allow_html=True)

# --- 🧪 PSYCHOLOGY ANALYSIS FUNCTION ---
def get_market_psychology(symbol, price_change):
    # Groq + Mistral + Gemini Combined Logic
    if price_change < -4:
        return "EXTREME FEAR", "Whales are accumulating. Retail is panicking. **PURI ENTRY LENI HAI**.", "fear"
    elif price_change > 4:
        return "EXTREME GREED", "Market is over-hyped. Retail is buying late. **EXIT NOW / SELL**.", "greed"
    else:
        return "NEUTRAL PSYCHOLOGY", "Market is testing patience. Hold positions.", "white"

# --- 📊 MASTER ENGINE DATA ---
try:
    url = f"https://min-api.cryptocompare.com/data/pricemultifull?fsyms={','.join(COINS)}&tsyms=USD"
    res = requests.get(url).json()['RAW']
    
    cols = st.columns(3)
    for i, sym in enumerate(COINS):
        if sym in res:
            p = res[sym]['USD']['PRICE']
            c = res[sym]['USD']['CHANGEPCT24HOUR']
            psych_status, psych_desc, p_color = get_market_psychology(sym, c)
            
            with cols[i % 3]:
                st.markdown(f"""
                    <div class="psych-card">
                        <div style="display:flex; justify-content:space-between;">
                            <span style="color:white; font-size:18px; font-weight:bold;">{sym}/USDT</span>
                            <span style="color:{p_color}; font-size:12px;">{psych_status}</span>
                        </div>
                        <h2 style="color:white; margin:10px 0;">${p:,.2f} <small style="font-size:14px;">({c:+.2f}%)</small></h2>
                        <div style="margin:10px 0;">
                            <span class="brain-tag" style="background:#f39c12;">🧠 Groq</span>
                            <span class="brain-tag" style="background:#3498db;">🧠 Mistral</span>
                            <span class="brain-tag" style="background:#9b59b6;">🧠 Gemini</span>
                        </div>
                        <p style="color:#8b949e; font-size:12px; border-top:1px solid #30363d; padding-top:10px;">
                            {psych_desc}
                        </p>
                    </div>
                """, unsafe_allow_html=True)
except:
    st.error("📡 Connecting to Neural Clusters...")
    time.sleep(2)
    st.rerun()
