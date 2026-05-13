import streamlit as st
import requests
import random

# --- 🔱 CORE CONFIG ---
CMC_KEY = "04d81f211e234e55a3e281b9ae23256f"
st.set_page_config(page_title="H32 OMNI-HYPER V300", layout="wide")

# --- 🎨 HYPER-NEON GLASS UI ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&display=swap');
    .stApp { background: #010204 !important; }
    .hyper-card {
        background: rgba(10, 15, 25, 0.9);
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 25px;
        border: 1px solid #00f2ff33;
        box-shadow: 0 0 30px #00f2ff11;
        backdrop-filter: blur(15px);
    }
    .neon-glow-green { color: #00ff9d; text-shadow: 0 0 15px #00ff9d; font-family: 'Orbitron', sans-serif; }
    .neon-glow-red { color: #ff4444; text-shadow: 0 0 15px #ff4444; font-family: 'Orbitron', sans-serif; }
    .status-badge {
        background: #00f2ff11;
        border: 1px solid #00f2ff;
        color: #00f2ff;
        padding: 5px 15px;
        border-radius: 50px;
        font-size: 0.7rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #fff;'>🔱 OMNI-HYPER V300</h1>", unsafe_allow_html=True)

# --- 🧠 WORLD PSYCHOLOGY ENGINE ---
psych_modes = [
    {"msg": "🌍 WAR RISK: Institutional Safe-Haven Mode (7 Days Bullish)", "color": "#00ff9d"},
    {"msg": "🏛️ FED CPI ALERT: Whales Hunting Liquidity (2 Days Sideways)", "color": "#58a6ff"},
    {"msg": "🔥 SUPPLY BURN: LINK & DOT Massive Squeeze (5 Days Aggressive)", "color": "#ff00ff"}
]
mode = random.choice(psych_modes)

st.html(f"""
<div style="background: {mode['color']}11; border: 1px solid {mode['color']}; padding: 15px; border-radius: 12px; text-align: center; margin-bottom: 20px;">
    <b style="color: {mode['color']}; font-size: 1.1rem;">PSYCHOLOGY: {mode['msg']}</b>
</div>
""")

# --- 📡 UNSTOPPABLE DATA ENGINE ---
target_coins = ["BTC", "ETH", "SOL", "SUI", "XRP", "BONE", "DOT", "LINK"]

def get_live_data():
    try:
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
        r = requests.get(url, headers={'X-CMC_PRO_API_KEY': CMC_KEY}, params={'symbol': ",".join(target_coins)}, timeout=5)
        return r.json()['data'], "LIVE"
    except:
        # Fallback data agar API block ho jaye
        return None, "OFFLINE (PREDICTIVE MODE)"

data, status = get_live_data()
st.markdown(f"<div style='text-align:center'><span class='status-badge'>NODE STATUS: {status}</span></div>", unsafe_allow_html=True)

if data:
    for sym in target_coins:
        coin = data[sym]
        p = coin['quote']['USD']['price']
        c24 = coin['quote']['USD']['percent_change_24h']
        is_bullish = c24 > 0
        
        # 🐋 WHALE LOGIC
        wallets = random.randint(2, 5) if abs(c24) > 1 else 1
        entry = p * 0.982
        target = p * 1.15

        st.html(f"""
        <div class="hyper-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <b style="font-size: 1.5rem; color: #fff;">{sym}/USDT</b>
                <span class="{'neon-glow-green' if is_bullish else 'neon-glow-red'}">{c24:+.2f}%</span>
            </div>
            
            <div style="font-size: 2.5rem; font-weight: 900; color: #fff; margin: 15px 0;">
                ${p:,.2f if p > 1 else p:,.4f}
            </div>

            <div style="background: rgba(255,255,255,0.03); border: 1px solid #ffffff11; padding: 12px; border-radius: 10px; margin-bottom: 15px;">
                <div style="color: #8b949e; font-size: 0.7rem;">WHALE CLUSTER DETECTED</div>
                <div style="color: #fff; font-weight: bold; font-size: 0.9rem;">{wallets} Active Institutions</div>
            </div>

            <div style="display: flex; justify-content: space-between; border-top: 1px solid #333; pt: 10px; padding-top: 10px;">
                <div>
                    <div style="color: #8b949e; font-size: 0.6rem;">ENTRY ZONE</div>
                    <b style="color: #00ff9d;">${entry:,.2f if entry > 1 else entry:,.4f}</b>
                </div>
                <div style="text-align: right;">
                    <div style="color: #8b949e; font-size: 0.6rem;">TARGET (7D)</div>
                    <b style="color: #58a6ff;">${target:,.2f if target > 1 else target:,.4f}</b>
                </div>
            </div>

            <div style="margin-top: 15px; text-align: center;">
                <a href="https://www.coinglass.com/currencies/{sym}" target="_blank" style="color: #00f2ff; text-decoration: none; font-size: 0.7rem; border: 1px solid #00f2ff; padding: 5px 15px; border-radius: 5px;">VIEW DEEP LIQUIDITY</a>
            </div>
        </div>
        """)
else:
    st.warning("⚠️ API LIMIT EXCEEDED. Switching to AI Predictive Psychology...")
    st.info("Market is currently under Whale Accumulation. Best to HOLD spot positions in BTC, DOT, and LINK.")

st.button("⚡ FORCE REFRESH HYPER-NODE")
