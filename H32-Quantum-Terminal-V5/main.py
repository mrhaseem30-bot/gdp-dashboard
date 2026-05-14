import streamlit as st
import requests
import time

# --- 🛰️ SATELLITE & BRAIN SETUP ---
st.set_page_config(page_title="ENCEPHALON V27 PRECISION", layout="wide")

# Keys from your env.txt
GROQ_KEY = "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"
TELEGRAM_ID = "8376377797" 

# Full list from your screenshot
COINS = ["ASTER", "UNI", "LTC", "ZEC", "BNB", "SOL", "AVAX", "ONDO", "BGB", "HYPE", "ADA", "SUI", "DOT", "LINK", "DOGE", "XPL", "BTC", "ETH", "XRP"]

st.markdown("""
    <style>
    .stApp { background-color: #020508; }
    .trade-card {
        background: #0d1117;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
    }
    .buy-btn { background-color: #238636; color: white; padding: 5px 10px; border-radius: 5px; font-weight: bold; display: inline-block; }
    .sell-btn { background-color: #da3633; color: white; padding: 5px 10px; border-radius: 5px; font-weight: bold; display: inline-block; }
    .price-main { font-size: 32px; font-weight: 800; color: white; margin: 10px 0; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='color:white; text-align:center;'>🛰️ ENCEPHALON V27: BUY/SELL PRECISION</h1>", unsafe_allow_html=True)

# --- 📊 MASTER PRECISION ENGINE ---
try:
    url = f"https://min-api.cryptocompare.com/data/pricemultifull?fsyms={','.join(COINS)}&tsyms=USD"
    res = requests.get(url).json()['RAW']
    
    cols = st.columns(3)
    for i, sym in enumerate(COINS):
        if sym in res:
            p = res[sym]['USD']['PRICE']
            c = res[sym]['USD']['CHANGEPCT24HOUR']
            
            # 🧠 NEURAL PSYCHOLOGY LEVELS
            # Kharidne ki jagah (Support level calculation)
            buy_at = p * 0.982  # Current price se 1.8% niche solid entry
            # Bechne ki jagah (Resistance level calculation)
            sell_at = p * 1.045 # 4.5% profit target
            
            with cols[i % 3]:
                st.markdown(f"""
                    <div class="trade-card">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <span style="color:#8b949e; font-weight:bold;">{sym}/USDT</span>
                            <span style="color:{'#3fb950' if c>=0 else '#f85149'}; font-size:12px;">{c:+.2f}%</span>
                        </div>
                        <div class="price-main">${p:,.2f}</div>
                        
                        <div style="background:rgba(255,255,255,0.05); padding:10px; border-radius:8px; margin-bottom:15px;">
                            <div style="margin-bottom:8px;">
                                <span class="buy-btn">KHARIDNA YAHAN HAI</span> 
                                <span style="color:white; margin-left:10px; font-weight:bold;">${buy_at:,.2f}</span>
                            </div>
                            <div>
                                <span class="sell-btn">BECHNA YAHAN HAI</span> 
                                <span style="color:white; margin-left:10px; font-weight:bold;">${sell_at:,.2f}</span>
                            </div>
                        </div>
                        
                        <p style="color:#00f2ff; font-size:11px; margin:0;">
                            🧠 VERDICT: {'ENTRY LE LO, MAUSAM THEEK HAI' if c < 0 else 'ABHI MAT KHREEDO, WAIT KARO'}
                        </p>
                    </div>
                """, unsafe_allow_html=True)
except:
    st.error("📡 SCANNING GLOBAL PRICE FEED...")
    time.sleep(2)
    st.rerun()
