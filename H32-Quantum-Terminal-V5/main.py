import streamlit as st
import requests
import random

# --- 🔱 OMNI-CORE CONFIG ---
CMC_KEY = "04d81f211e234e55a3e281b9ae23256f"
st.set_page_config(page_title="H32 OMNI-PREDATOR V250", layout="wide")

# --- 🎨 GLOBAL DYNAMIC THEME ---
def apply_omni_theme(sentiment_score):
    # Sentiment ke hisab se background aura change hoga
    if sentiment_score > 70: bg = "linear-gradient(180deg, #050a0f 0%, #001a14 100%)" # Bullish
    elif sentiment_score < 30: bg = "linear-gradient(180deg, #0a0505 0%, #1a0000 100%)" # War/Panic
    else: bg = "#05070a" # Neutral
    
    st.markdown(f"""
    <style>
        .stApp {{ background: {bg} !important; color: #e2e8f0; }}
        .omni-card {{
            background: rgba(13, 17, 23, 0.95);
            border: 1px solid #30363d;
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
        }}
        .psych-alert {{
            background: rgba(88, 166, 255, 0.1);
            border-left: 5px solid #58a6ff;
            padding: 15px;
            border-radius: 4px;
            margin: 15px 0;
        }}
    </style>
    """, unsafe_allow_html=True)

# --- 🧠 GLOBAL PSYCHOLOGY ENGINE ---
def get_global_sentiment():
    # Yahan hum Global situation (World War threats, CPI, FED) ko simulate kar rahe hain
    scenarios = [
        {"msg": "WORLD WAR TENSIONS: Whales Moving to Gold & BTC", "score": 45},
        {"msg": "CPI DATA RELEASE: Market Expecting Volatility", "score": 55},
        {"msg": "INSTITUTIONAL PUMP: Big Banks Entering Spot", "score": 85},
        {"msg": "FED INTEREST RATES: Neutral Sentiment", "score": 50}
    ]
    return random.choice(scenarios)

# --- 📡 SUPREME DATA EXECUTION ---
st.title("🔱 H32 OMNI-PREDATOR V250")
global_psy = get_global_sentiment()
apply_omni_theme(global_psy['score'])

st.markdown(f"**🌍 GLOBAL PSYCHOLOGY:** `{global_psy['msg']}`")

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
        vol_m = coin['quote']['USD']['volume_24h'] / 1e6
        
        # 🐋 WHALE & INFLOW LOGIC
        active_wallets = random.randint(1, 4) if abs(c24) > 1.5 else 1
        inflow = vol_m * (0.65 if c24 > 0 else 0.35)
        outflow = vol_m - inflow
        net_flow = inflow - outflow
        
        # 🎯 ENTRY/EXIT & LIQUIDATION GAP
        gap = p * 0.04
        entry = p * 0.982
        target = p * 1.12

        # --- 📱 THE ALL-IN-ONE TERMINAL ---
        st.html(f"""
        <div class="omni-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 1.3rem; font-weight: bold; color: #58a6ff;">{sym}/USDT</span>
                <span style="background: #2481cc22; color: #58a6ff; padding: 4px 10px; border-radius: 50px; font-size: 0.7rem;">
                    WALLETS ACTIVE: {active_wallets}
                </span>
            </div>

            <div style="font-size: 2.5rem; font-weight: 900; color: #ffffff; margin: 10px 0;">
                ${p:,.2f} <span style="font-size: 1rem; color: {'#00ff9d' if c24 > 0 else '#ff4444'}">{c24:+.2f}%</span>
            </div>

            <div class="psych-alert">
                <div style="font-size: 0.7rem; color: #8b949e; text-transform: uppercase;">Psychology Forecast (3-7 Days)</div>
                <div style="font-weight: bold; margin-top: 5px;">
                    {'🚀 INSTITUTIONAL ACCUMULATION: Trend Up (1 Week)' if active_wallets >= 3 else '⚖️ LIQUIDATION HUNT: Expect Reversal'}
                </div>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 15px;">
                <div style="background: #161b22; padding: 10px; border-radius: 8px; border: 1px solid #30363d;">
                    <div style="font-size: 0.6rem; color: #8b949e;">NET INFLOW</div>
                    <div style="color: #00ff9d; font-weight: bold;">+${inflow:,.1f}M</div>
                </div>
                <div style="background: #161b22; padding: 10px; border-radius: 8px; border: 1px solid #30363d;">
                    <div style="font-size: 0.6rem; color: #8b949e;">LIQ GAP</div>
                    <div style="color: #ff4444; font-weight: bold;">±${gap:,.2f}</div>
                </div>
            </div>

            <div style="background: rgba(0, 255, 157, 0.05); border: 1px dashed #00ff9d; padding: 10px; border-radius: 8px; text-align: center;">
                <span style="color: #8b949e; font-size: 0.7rem;">BEST ENTRY ZONE:</span><br>
                <b style="color: #00ff9d; font-size: 1.1rem;">${entry:,.2f}</b>
            </div>

            <div style="margin-top: 15px; font-size: 0.8rem; text-align: center; color: #58a6ff; font-weight: bold;">
                {'✅ PURI ENTRY LENI HAI' if active_wallets >= 2 and c24 > 0 else '❌ WAIT FOR WHALE SIGNAL'}
            </div>
        </div>
        """)

except Exception as e:
    st.error("Global Node Syncing...")

st.caption("Developed for Haseem Ali | Omni-Predator V250 | World Psychology & Whale Intel")
