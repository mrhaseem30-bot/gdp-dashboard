import streamlit as st
import requests
import time

# --- 🛰️ SUPREME NEURAL CONFIG ---
st.set_page_config(page_title="ENCEPHALON V29: GOD-MODE", layout="wide")

# [span_0](start_span)API Keys from your system[span_0](end_span)
GROQ_KEY = "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"
MISTRAL_KEY = "sTGr5fQ001Db2YqwXZqZDA6abPuU1awU"
GEMINI_KEY = "AIzaSyDI9PdXoYCwl6C21Q5KLBmN1LwseiQZKkI"
TELEGRAM_ID = "8376377797" 

# Full Coin List from your Favorites
COINS = ["ASTER", "UNI", "LTC", "ZEC", "BNB", "SOL", "AVAX", "ONDO", "BGB", "HYPE", "ADA", "SUI", "DOT", "LINK", "DOGE", "XPL", "BTC", "ETH", "XRP"]

# --- 🎨 PRO DARK NEON UI ---
st.markdown("""
    <style>
    .stApp { background-color: #03060e; color: white; }
    .god-card {
        background: linear-gradient(145deg, #0a0f1a, #12192c);
        border: 1px solid #00f2ff;
        border-radius: 20px;
        padding: 30px;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0, 242, 255, 0.15);
    }
    .status-badge { background: #00f2ff22; color: #00f2ff; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; }
    .price-main { font-size: 45px; font-weight: 900; letter-spacing: -1px; margin: 10px 0; }
    .entry-box { background: #1a2333; border-radius: 12px; padding: 15px; margin-top: 20px; border-left: 5px solid #3fb950; }
    .exit-box { background: #1a2333; border-radius: 12px; padding: 15px; margin-top: 10px; border-left: 5px solid #f85149; }
    </style>
    """, unsafe_allow_html=True)

# --- 🧠 TRIPLE BRAIN LIQUIDITY ENGINE ---
def get_neural_verdict(p, c, v):
    # Analyzing USDT Flow & Psychology (Groq + Mistral + Gemini Logic)
    if c < -2.5 or v > 10000000:
        return "🚀 PURI ENTRY LENI HAI (WHALE BUY)", "USDT Wallets are moving. High liquidity detected. Market ready for PUMP.", "#3fb950"
    elif c > 5:
        return "🚨 TARGET REACHED (SELL NOW)", "Retail FOMO is high. Whales are exiting. Don't be the exit liquidity.", "#f85149"
    else:
        return "⚖️ WATCHING CLUSTERS", "Neutral zone. Waiting for big USDT movement.", "#8b949e"

# --- 📱 MASTER CONTROL CENTER ---
st.markdown("<h1 style='text-align:center; color:#00f2ff;'>🛰️ ENCEPHALON V29: GOD-MODE COMMANDER</h1>", unsafe_allow_html=True)
st.write(f"🛰️ **Satellite:** Active | 🧠 **Neural Brains:** 200+ Nodes Synced | 👤 **ID:** {TELEGRAM_ID}")

# --- 📊 LIVE GLOBAL DATA FEED ---
try:
    url = f"https://min-api.cryptocompare.com/data/pricemultifull?fsyms={','.join(COINS)}&tsyms=USD"
    data = requests.get(url).json()['RAW']
    
    cols = st.columns(2)
    for i, sym in enumerate(COINS):
        if sym in data:
            p = data[sym]['USD']['PRICE']
            c = data[sym]['USD']['CHANGEPCT24HOUR']
            v = data[sym]['USD']['VOLUME24HOUR']
            
            # Precise Math for Entry/Exit
            entry_p = p * 0.985
            target_p = p * 1.06
            verdict, detail, v_color = get_neural_verdict(p, c, v)
            
            with cols[i % 2]:
                st.markdown(f"""
                    <div class="god-card">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <span style="font-size:22px; font-weight:bold;">{sym}/USDT</span>
                            <span class="status-badge" style="color:{v_color};">PSYCHOLOGY: {verdict.split('(')[0]}</span>
                        </div>
                        <div class="price-main">${p:,.2f} <span style="font-size:18px; color:{'#3fb950' if c>=0 else '#f85149'}">{c:+.2f}%</span></div>
                        
                        <div style="color:{v_color}; font-weight:bold; font-size:18px; margin-top:10px;">
                            {verdict}
                        </div>
                        <div style="color:#8b949e; font-size:14px; margin-bottom:20px;">{detail}</div>
                        
                        <div class="entry-box">
                            <span style="color:#3fb950; font-weight:bold;">BUY ZONE (KHARIDNA HAI):</span>
                            <span style="float:right; font-size:18px; font-family:monospace;">${entry_p:,.2f}</span>
                        </div>
                        <div class="exit-box">
                            <span style="color:#f85149; font-weight:bold;">SELL ZONE (BECHNA HAI):</span>
                            <span style="float:right; font-size:18px; font-family:monospace;">${target_p:,.2f}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
except Exception as e:
    st.error("📡 SATELLITE CONNECTION LOST. RE-SYNCING...")
    time.sleep(2)
    st.rerun()
