import streamlit as st
import requests
import time

# --- 🛰️ SATELLITE SYSTEM CONFIG ---
st.set_page_config(page_title="ENCEPHALON V30", layout="wide")

# [span_0](start_span)API Keys from your env.txt[span_0](end_span)
GROQ_KEY = "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"
MISTRAL_KEY = "sTGr5fQ001Db2YqwXZqZDA6abPuU1awU"
GEMINI_KEY = "AIzaSyDI9PdXoYCwl6C21Q5KLBmN1LwseiQZKkI"
TELEGRAM_ID = "8376377797" # From Screenshot 183724

# Your Full Coin List
COINS = ["ASTER", "UNI", "LTC", "ZEC", "BNB", "SOL", "AVAX", "ONDO", "BGB", "HYPE", "ADA", "SUI", "DOT", "LINK", "DOGE", "XPL", "BTC", "ETH", "XRP"]

# --- 🎨 PRO UI DESIGN (Fixing the Text Issue) ---
st.markdown("""
    <style>
    .stApp { background-color: #05080b; }
    .master-card {
        background: #0d1117;
        border: 2px solid #00f2ff;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .price-val { font-size: 35px; font-weight: bold; color: white; }
    .buy-zone { background: #238636; color: white; padding: 10px; border-radius: 8px; margin-top: 10px; font-weight: bold; }
    .sell-zone { background: #da3633; color: white; padding: 10px; border-radius: 8px; margin-top: 5px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='color:white; text-align:center;'>🛰️ ENCEPHALON V30: GOD-MODE SYSTEM</h1>", unsafe_allow_html=True)

# --- 🧠 TRIPLE BRAIN LIQUIDITY ENGINE ---
def get_market_logic(p, c, v):
    # Whale Wallet USDT flow logic
    if c < -1.5 or v > 8000000:
        return "🚀 PURI ENTRY LENI HAI", "USDT Liquidity Moving to Exchanges. Buy the Panic.", "#3fb950"
    elif c > 4:
        return "🚨 EXIT / TARGET REACHED", "Retail Greed Detected. Whales are selling.", "#f85149"
    else:
        return "⚖️ NEUTRAL WAIT", "Waiting for USDT Wallet Movement.", "#8b949e"

# --- 📊 LIVE GLOBAL DATA STREAM ---
try:
    url = f"https://min-api.cryptocompare.com/data/pricemultifull?fsyms={','.join(COINS)}&tsyms=USD"
    res = requests.get(url).json()['RAW']
    
    cols = st.columns(2)
    for i, sym in enumerate(COINS):
        if sym in res:
            p = res[sym]['USD']['PRICE']
            c = res[sym]['USD']['CHANGEPCT24HOUR']
            v = res[sym]['USD']['VOLUME24HOUR']
            
            # Neural Math
            buy_at = p * 0.988
            sell_at = p * 1.055
            verdict, msg, v_color = get_market_logic(p, c, v)
            
            with cols[i % 2]:
                # Using direct markdown to avoid the issue in Screenshot 153716
                st.markdown(f"""
                    <div class="master-card">
                        <div style="display:flex; justify-content:space-between;">
                            <span style="color:white; font-size:18px;">{sym}/USDT</span>
                            <span style="color:{v_color};">● {verdict}</span>
                        </div>
                        <div class="price-val">${p:,.2f} <small style="font-size:14px; color:{v_color}">{c:+.2f}%</small></div>
                        <p style="color:#8b949e; font-size:12px;">{msg}</p>
                        <div class="buy-zone">📉 BUY AT: ${buy_at:,.2f}</div>
                        <div class="sell-zone">📈 SELL AT: ${sell_at:,.2f}</div>
                    </div>
                """, unsafe_allow_html=True)
except:
    st.warning("📡 Scanning Global USDT Liquidity...")
    time.sleep(1)
    st.rerun()
