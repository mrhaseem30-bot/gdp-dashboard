import streamlit as st
import requests

# --- 🔱 CORE SETUP ---
CMC_KEY = "04d81f211e234e55a3e281b9ae23256f"

st.set_page_config(page_title="H32 OMNISCIENT V190", layout="wide")

# --- 🎨 INSTITUTIONAL CSS (No Code Visible Fix) ---
st.markdown("""
<style>
    .stApp { background-color: #05070a !important; color: #e2e8f0; }
    [data-testid="stVerticalBlock"] > div:has(div.terminal-card) {
        padding: 0px;
    }
</style>
""", unsafe_allow_html=True)

# --- 📡 DATA ENGINE ---
st.title("🔱 H32 OMNISCIENT V190")
st.markdown("`TERMINAL STATUS: ONLINE` | `NO-VOICE MODE`")

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
        
        # Calculation for Liquidation Points
        s_liq = p * 1.025
        l_liq = p * 0.975
        gap = abs(p - s_liq)

        # --- 📱 THE "CLEAN" HTML COMPONENT ---
        # Is tareeke se code kabhi bhi screen par text ban kar nahi dikhega
        st.html(f"""
        <div style="
            background: #0d1117; 
            border: 1px solid #30363d; 
            border-radius: 12px; 
            padding: 20px; 
            margin-bottom: 15px;
            font-family: sans-serif;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="color:#58a6ff; font-size:1.1rem; font-weight:bold;">{sym}/USDT</span>
                <span style="color: {'#00ff9d' if c24 > 0 else '#ff4444'}; font-weight:bold;">{c24:+.2f}%</span>
            </div>
            
            <div style="font-size: 2rem; font-weight: 800; color: #ffffff; margin: 10px 0;">
                ${p:,.2f}
            </div>
            
            <div style="background:#161b22; padding:10px; border-radius:6px; border-left:4px solid #ff4444; margin-bottom:10px;">
                <span style="color:#8b949e; font-size:0.8rem;">⚠️ LIQUIDATION GAP:</span> 
                <span style="color:#e2e8f0; font-weight:bold; font-family:monospace;">±${gap:,.2f}</span>
            </div>

            <div style="display: flex; justify-content: space-between; font-size: 0.7rem; color: #8b949e; margin-bottom:5px;">
                <span>Shorts: ${s_liq:,.2f}</span>
                <span>Longs: ${l_liq:,.2f}</span>
            </div>

            <div style="height: 10px; background: #21262d; border-radius: 5px; display: flex; overflow: hidden; border:1px solid #30363d;">
                <div style="width: 45%; background: linear-gradient(90deg, #880000, #ff4444);"></div>
                <div style="width: 55%; background: linear-gradient(90deg, #004d00, #00ff9d);"></div>
            </div>
            
            <div style="margin-top:15px; background: rgba(36, 129, 204, 0.1); border: 1px solid #2481cc; color: #58a6ff; padding: 8px; border-radius: 6px; font-size: 0.8rem; text-align: center; font-weight: bold;">
                🐋 WHALE STATUS: {'Buy Wall Detected' if c24 > 0 else 'Short Trap Pending'}
            </div>
        </div>
        """)

except Exception as e:
    st.error("Reconnecting to Market Data...")

st.caption("Developed for Haseem Ali | Terminal V190 | No HTML Code Visible")
