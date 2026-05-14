import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime
import os

# --- 🔱 CORE CONFIG & DNA MEMORY ---
st.set_page_config(page_title="ENCEPHALON V12", layout="wide")

MEMORY_FILE = "neural_memory_v12.csv"
if not os.path.exists(MEMORY_FILE):
    pd.DataFrame(columns=['Time', 'Symbol', 'Price', 'Signal', 'Target']).to_csv(MEMORY_FILE, index=False)

# --- 🎨 SATELLITE UI (AS PER SCREENSHOT 214819) ---
st.markdown("""
    <style>
    .stApp { background-color: #050a10; }
    .satellite-card {
        background-color: #0d1621;
        border: 2px solid #00f2ff;
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.2);
    }
    .verdict-box {
        background: rgba(0, 242, 255, 0.05);
        border-left: 5px solid #00f2ff;
        padding: 10px;
        margin-top: 15px;
        border-radius: 5px;
    }
    .btn-row { display: flex; gap: 10px; margin-top: 15px; }
    .custom-btn {
        background: transparent;
        border: 1px solid #30363d;
        color: #58a6ff;
        padding: 5px 15px;
        border-radius: 8px;
        font-size: 12px;
        text-transform: uppercase;
    }
    .price-text { color: white; font-size: 45px; font-weight: bold; margin: 10px 0; }
    .symbol-text { color: white; font-size: 22px; font-weight: bold; }
    .percent-text { color: #3fb950; float: right; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 🌍 MULTI-SOURCE SEARCH ENGINE ---
def fetch_global_data():
    # Attempting multiple sources for "Puri Duniya Ka Data"
    sources = [
        "https://api.binance.com/api/v3/ticker/24hr",
        "https://api1.binance.com/api/v3/ticker/24hr"
    ]
    for url in sources:
        try:
            res = requests.get(url, timeout=5)
            if res.status_code == 200:
                data = res.json()
                targets = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "DOTUSDT"]
                return {i['symbol'].replace('USDT',''): i for i in data if i['symbol'] in targets}
        except: continue
    return None

# --- 📱 MASTER INTERFACE ---
st.markdown("<h2 style='color:white; text-align:center;'>🛰️ SATELLITE POSITION VERDICT</h2>", unsafe_allow_html=True)

intel = fetch_global_data()

if intel:
    cols = st.columns(len(intel))
    for i, (sym, d) in enumerate(intel.items()):
        price = float(d['lastPrice'])
        change = float(d['priceChangePercent'])
        target_price = price * 1.15 # 200 IQ Target Logic
        
        with cols[i]:
            st.markdown(f"""
                <div class="satellite-card">
                    <div>
                        <span class="symbol-text">● {sym}/USDT</span>
                        <span class="percent-text">{change:+.2f}%</span>
                    </div>
                    <div class="price-text">${price:,.2f}</div>
                    
                    <div class="verdict-box">
                        <p style="color:#8b949e; font-size:10px; margin:0;">SATELLITE POSITION VERDICT</p>
                        <p style="color:white; font-weight:bold; margin:5px 0;">🚀 PURI ENTRY LENI HAI (STRONG BUY)</p>
                        <p style="color:#3fb950; font-size:12px; margin:0;">ENTRY: ${price:,.2f} | TARGET: ${target_price:,.2f}</p>
                    </div>
                    
                    <div class="btn-row">
                        <div class="custom-btn">ORDER FLOW</div>
                        <div class="custom-btn">SMART CHART</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Save to Neural Memory (Zero Forgetting)
            if abs(change) > 1.5:
                new_h = pd.DataFrame([[datetime.now(), sym, price, "STRONG_BUY", target_price]], columns=['Time', 'Symbol', 'Price', 'Signal', 'Target'])
                new_h.to_csv(MEMORY_FILE, mode='a', header=False, index=False)
else:
    st.error("❌ GLOBAL CONNECTION LOST! CHECKING BACKUP SOURCES...")
    time.sleep(5)
    st.rerun()

# --- 📁 NEURAL MEMORY HISTORY ---
st.divider()
st.markdown("### 📁 Neural Memory (Puri Duniya Ki History)")
if os.path.exists(MEMORY_FILE):
    hist = pd.read_csv(MEMORY_FILE)
    st.dataframe(hist.tail(10).iloc[::-1], use_container_width=True)

time.sleep(10)
st.rerun()
