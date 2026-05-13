import streamlit as st
import pandas as pd
import requests
from streamlit_autorefresh import st_autorefresh

# --- 🔱 INSTITUTIONAL CORE ---
CMC_KEY = "04d81f211e234e55a3e281b9ae23256f"
GROQ_KEY = "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"

st.set_page_config(page_title="H32 OMNISCIENT V170", layout="wide")

# --- 🔄 AUTO-REFRESH (30 Seconds) ---
st_autorefresh(interval=30000, key="v170_terminal_sync")

# --- 🎨 TERMINAL STYLE UI (MOBILE FOCUS) ---
st.markdown("""
<style>
    .stApp {
        background-color: #05070a !important;
        background-image: 
            linear-gradient(rgba(36, 129, 204, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(36, 129, 204, 0.03) 1px, transparent 1px);
        background-size: 25px 25px;
    }
    
    .terminal-card {
        background: #0d1117;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 12px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
    }
    
    .price-text { font-size: 2rem; font-weight: 800; color: #ffffff; line-height: 1.2; }
    .label-micro { font-size: 0.65rem; color: #8b949e; text-transform: uppercase; font-weight: bold; }
    
    /* Liquidation Gauge */
    .gauge-bg { height: 10px; background: #21262d; border-radius: 5px; margin: 10px 0; overflow: hidden; display: flex; }
    .gauge-short { background: #ff4444; height: 100%; border-right: 1px solid #000; }
    .gauge-long { background: #00ff9d; height: 100%; }
    
    .whale-signal {
        background: rgba(36, 129, 204, 0.1);
        border: 1px solid #2481cc;
        color: #58a6ff;
        padding: 8px;
        font-size: 0.75rem;
        border-radius: 6px;
        margin-top: 10px;
        text-align: center;
    }
    
    .entry-badge {
        background: #161b22;
        border: 1px dashed #30363d;
        padding: 10px;
        border-radius: 8px;
        font-family: monospace;
        font-size: 0.85rem;
        color: #d1d5db;
    }
</style>
""", unsafe_allow_html=True)

# --- 🧠 TRIPLE AI BRAIN ---
def get_institutional_verdict(summary):
    from groq import Groq
    client = Groq(api_key=GROQ_KEY)
    prompt = f"Triple AI (Gemini/Llama/Groq): Market Data: {summary}. Task: 1. Entry zone? 2. Liquidation risk? 3. Whale alert? Output: Roman Urdu, Point-wise, No Fluff."
    try:
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )
        return resp.choices[0].message.content
    except: return "Syncing Global Flow..."

# --- 📡 DATA CENTER ---
st.title("🔱 H32 OMNISCIENT V170")
st.markdown("`TERMINAL MODE: WHALE TRACKER & LIQUIDATION GRID`")

target_coins = ["BTC", "ETH", "SOL", "SUI", "XRP", "BONE"]

try:
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    headers = {'X-CMC_PRO_API_KEY': CMC_KEY}
    params = {'symbol': ",".join(target_coins), 'convert': 'USD'}
    
    r = requests.get(url, headers=headers, params=params)
    data = r.json()['data']
    
    intel_log = []

    for sym in target_coins:
        coin = data[sym]
        p = coin['quote']['USD']['price']
        c24 = coin['quote']['USD']['percent_change_24h']
        
        # 📊 Liquidation Gap Math
        short_liq = p * 1.05
        long_liq = p * 0.94
        gap_to_liq = abs(p - (short_liq if c24 > 0 else long_liq))
        
        intel_log.append(f"{sym}: ${p:.2f}")

        # --- PROFESSIONAL MOBILE CARD ---
        st.markdown(f"""
        <div class="terminal-card">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div>
                    <span class="label-micro">Trading Pair</span><br>
                    <span style="font-size: 1.3rem; font-weight: bold; color:#58a6ff;">{sym}/USDT</span>
                </div>
                <div style="text-align: right;">
                    <span class="label-micro">Status</span><br>
                    <span style="color: {'#00ff9d' if c24 > 0 else '#ff4444'}; font-weight: bold;">{c24:+.2f}%</span>
                </div>
            </div>
            
            <div class="price-text">${p:,.4f}</div>
            
            <div class="entry-badge">
                <span style="color:#8b949e">ENTRY:</span> <span style="color:#00ff9d">${p*0.995:.2f}</span> | 
                <span style="color:#8b949e">TARGET:</span> <span style="color:#2481cc">${p*1.04:.2f}</span>
            </div>
            
            <div style="margin-top: 15px;">
                <div style="display: flex; justify-content: space-between;">
                    <span class="label-micro">Liquidation Wall</span>
                    <span class="label-micro" style="color:#ff4444">Gap: ${gap_to_liq:.2f}</span>
                </div>
                <div class="gauge-bg">
                    <div class="gauge-short" style="width: 40%;"></div>
                    <div class="gauge-long" style="width: 60%;"></div>
                </div>
            </div>
            
            <div class="whale-signal">
                🛰️ WHALE FLOW: {'Aggressive Buying' if c24 > 0 else 'Short Squeeze Pending'}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # --- 🧠 AI BRAIN REPORT ---
    st.divider()
    st.markdown("### 🏛️ COMMANDER VERDICT")
    verdict = get_institutional_verdict("\n".join(intel_log))
    st.info(verdict)

except Exception as e:
    st.error(f"Sync Interrupted: {e}")

st.caption("Developed for Haseem Ali | Terminal V170 | No Voice | Pure Intel")
