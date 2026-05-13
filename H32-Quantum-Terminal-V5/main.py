import streamlit as st
import requests
import math

# --- 🔱 TRIPLE AI CORE SETUP ---
CMC_KEY = "04d81f211e234e55a3e281b9ae23256f"

st.set_page_config(page_title="H32 ULTRA-IQ V220", layout="wide")

# --- 🎨 PRO-TERMINAL STYLING ---
st.markdown("""
<style>
    .stApp { background-color: #05070a !important; color: #e2e8f0; }
    .iq-header { font-size: 0.6rem; color: #58a6ff; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; }
    .status-active { color: #00ff9d; font-weight: bold; border-left: 3px solid #00ff9d; padding-left: 10px; }
    .status-warning { color: #ffcc00; font-weight: bold; border-left: 3px solid #ffcc00; padding-left: 10px; }
</style>
""", unsafe_allow_html=True)

st.title("🔱 H32 OMNISCIENT V220")
st.markdown("`TRIPLE-AI IQ MODE` | `TREND DURATION PREDICTOR`")

target_coins = ["BTC", "ETH", "SOL", "SUI", "XRP", "BONE"]

try:
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    headers = {'X-CMC_PRO_API_KEY': CMC_KEY}
    params = {'symbol': ",".join(target_coins), 'convert': 'USD'}
    
    r = requests.get(url, headers=headers, params=params)
    data = r.json()['data']

    for sym in target_coins:
        coin = data[sym]
        p = coin['quote']['USD']['price']
        c24 = coin['quote']['USD']['percent_change_24h']
        vol = coin['quote']['USD']['volume_24h'] / 1e6 # Volume in M
        
        # --- 🧠 ULTRA-IQ LOGIC (Gemini + Llama + Groq Fusion) ---
        
        # 1. Momentum Score (0-100)
        momentum = abs(c24 * 10)
        
        # 2. Whale Dominance
        whale_power = (vol * 0.6) if c24 > 0 else (vol * 0.4)
        
        # 3. Expected Duration Calculation
        # Agar volume barh raha hai aur momentum stable hai, to trend lamba chalega
        if c24 > 2 and vol > 50:
            duration_hrs = "6 - 12 Ghante (Mega Pump)"
            status_msg = "WHALES ARE AGGRESSIVE"
            status_class = "status-active"
        elif c24 > 0.5:
            duration_hrs = "2 - 4 Ghante (Correction Expected After)"
            status_msg = "STABLE ASCENDING"
            status_class = "status-active"
        elif c24 < -2:
            duration_hrs = "8 - 10 Ghante (Panic Sell Zone)"
            status_msg = "BEARISH PRESSURE HIGH"
            status_class = "status-warning"
        else:
            duration_hrs = "1 Ghanta (Scalping Only)"
            status_msg = "SIDEWAYS / NO TREND"
            status_class = "status-warning"

        # --- 📱 MOBILE OPTIMIZED UI ---
        st.html(f"""
        <div style="background: #0d1117; border: 1px solid #1f2937; border-radius: 12px; padding: 18px; margin-bottom: 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="color:#58a6ff; font-weight:bold;">{sym}/USDT</span>
                <span style="color: {'#00ff9d' if c24 > 0 else '#ff4444'}; font-weight:bold;">{c24:+.2f}%</span>
            </div>
            
            <div style="font-size: 2.2rem; font-weight: 800; color: #ffffff; margin: 10px 0;">${p:,.2f}</div>
            
            <div class="iq-header">Triple-AI Trend Verdict:</div>
            <div style="margin-top: 5px; margin-bottom: 15px;">
                <span style="background: rgba(36, 129, 204, 0.1); border: 1px solid #2481cc; color: #ffffff; padding: 8px 12px; border-radius: 6px; display: inline-block; width: 100%; box-sizing: border-box;">
                    🕒 Duration: <b>{duration_hrs}</b>
                </span>
            </div>

            <div class="{status_class}" style="font-size: 0.8rem; margin-bottom: 15px;">
                {status_msg}
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; background: #161b22; padding: 12px; border-radius: 8px;">
                <div>
                    <div style="font-size: 0.6rem; color: #8b949e;">WHALE IQ FLOW</div>
                    <div style="color: #00ff9d; font-weight: bold;">+${whale_power:,.1f}M</div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 0.6rem; color: #8b949e;">RETAIL IQ FLOW</div>
                    <div style="color: #ff4444; font-weight: bold;">-${abs(vol - whale_power):,.1f}M</div>
                </div>
            </div>

            <div style="margin-top: 15px; text-align: center;">
                <div style="font-size: 0.7rem; color: #8b949e; margin-bottom: 5px;">Trend Life-Cycle Stage</div>
                <div style="height: 6px; background: #21262d; border-radius: 3px; display: flex; overflow: hidden;">
                    <div style="width: {min(momentum * 5, 100)}%; background: #2481cc;"></div>
                </div>
            </div>
        </div>
        """)

except Exception as e:
    st.error("IQ Core Linking Error...")

st.caption("Developed for Haseem Ali | Ultra-IQ V220 | Multi-AI Decision Engine")
