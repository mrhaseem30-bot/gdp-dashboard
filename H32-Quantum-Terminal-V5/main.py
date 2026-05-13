import streamlit as st
import requests
import random

# --- 🔱 SATELLITE CORE CONFIG ---
CMC_KEY = "04d81f211e234e55a3e281b9ae23256f"
st.set_page_config(page_title="H32 SATELLITE-PRO V310", layout="wide")

# --- 🎨 HYPER-CHAMAKDAR SATELLITE UI ---
st.markdown("""
<style>
    .stApp { background: #010204 !important; }
    .sat-card {
        background: rgba(15, 23, 42, 0.9);
        border: 2px solid #00f2ff;
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 30px;
        box-shadow: 0 0 20px #00f2ff33, inset 0 0 15px #00f2ff11;
        backdrop-filter: blur(10px);
    }
    .neon-green { color: #00ff9d; text-shadow: 0 0 10px #00ff9d; }
    .neon-red { color: #ff4444; text-shadow: 0 0 10px #ff4444; }
    .sat-header {
        background: linear-gradient(90deg, #00f2ff, #0062ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        text-align: center;
        font-size: 2.5rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='sat-header'>🔱 SATELLITE-PRO V310</h1>", unsafe_allow_html=True)

# --- 📡 SATELLITE LINK STATUS ---
st.success("🛰️ DIRECT SATELLITE CONNECTION ESTABLISHED | NODE: KARACHI-G1")

# --- 🧠 GLOBAL IQ ENGINE ---
st.info("**GLOBAL PSYCHOLOGY:** 🏛️ Institutional Safe-Haven Mode (Trend: 7-10 Days Bullish)")

target_coins = ["BTC", "ETH", "SOL", "SUI", "XRP", "BONE", "DOT", "LINK"]

# --- 🛠️ DATA CLEANING FUNCTION (Fixing the ValueError) ---
def format_p(val):
    if val > 1:
        return f"{val:,.2f}"
    else:
        return f"{val:,.4f}"

try:
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    r = requests.get(url, headers={'X-CMC_PRO_API_KEY': CMC_KEY}, params={'symbol': ",".join(target_coins)})
    data = r.json()['data']

    for sym in target_coins:
        coin = data[sym]
        p = coin['quote']['USD']['price']
        c24 = coin['quote']['USD']['percent_change_24h']
        is_bullish = c24 > 0
        
        # OMNI Calculations
        entry = p * 0.985
        target = p * 1.15

        st.html(f"""
        <div class="sat-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <div style="height: 12px; width: 12px; background: {'#00ff9d' if is_bullish else '#ff4444'}; border-radius: 50%; box-shadow: 0 0 15px {'#00ff9d' if is_bullish else '#ff4444'};"></div>
                    <b style="font-size: 1.6rem; color: #fff;">{sym}/USDT</b>
                </div>
                <b class="{'neon-green' if is_bullish else 'neon-red'}" style="font-size: 1.2rem;">{c24:+.2f}%</b>
            </div>

            <div style="font-size: 3rem; font-weight: 900; color: #fff; margin: 20px 0;">${format_p(p)}</div>

            <div style="background: rgba(0, 242, 255, 0.05); border-left: 5px solid #00f2ff; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
                <div style="color: #8b949e; font-size: 0.75rem;">SATELLITE POSITION VERDICT</div>
                <div style="color: #fff; font-weight: bold; margin-top: 5px; font-size: 1rem;">
                    {'🚀 PURI ENTRY LENI HAI (STRONG BUY)' if is_bullish else '⚠️ WAIT FOR LIQUIDATION SWEEP'}
                </div>
                <div style="margin-top: 10px; font-size: 0.9rem;">
                    <span style="color: #00ff9d;">ENTRY: ${format_p(entry)}</span> | 
                    <span style="color: #00f2ff;">TARGET: ${format_p(target)}</span>
                </div>
            </div>

            <div style="display: flex; gap: 10px;">
                <a href="https://www.coinglass.com/currencies/{sym}" target="_blank" style="flex:1; text-align:center; padding: 10px; border-radius: 10px; background: #1e293b; color: #00f2ff; text-decoration: none; font-size: 0.75rem; font-weight: bold; border: 1px solid #00f2ff44;">ORDER FLOW</a>
                <a href="https://www.tradingview.com/chart/?symbol=BINANCE:{sym}USDT" target="_blank" style="flex:1; text-align:center; padding: 10px; border-radius: 10px; background: #1e293b; color: #00f2ff; text-decoration: none; font-size: 0.75rem; font-weight: bold; border: 1px solid #00f2ff44;">SMART CHART</a>
            </div>
        </div>
        """)

except Exception as e:
    st.error("📡 SATELLITE SIGNAL LOST: Refreshing Node...")

st.caption("Developed for Haseem Ali | Satellite-Pro V310 | Unstoppable Direct Link")
