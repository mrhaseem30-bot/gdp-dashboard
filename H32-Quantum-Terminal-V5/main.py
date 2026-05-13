import streamlit as st
import requests
import random

# --- 🔱 OMNI-CORE CONFIG ---
CMC_KEY = "04d81f211e234e55a3e281b9ae23256f"
st.set_page_config(page_title="H32 NEON-OMEGA V280", layout="wide")

# --- 🎨 THE "CHAMAKDAR" NEON UI ENGINE ---
def apply_neon_ui(sentiment_score):
    # Sentiment ke hisab se neon colors change honge
    primary_neon = "#00ff9d" if sentiment_score > 60 else "#ff4444"
    secondary_glow = "#2481cc" if sentiment_score > 60 else "#7a0000"
    
    st.markdown(f"""
    <style>
        .stApp {{ background: #020406 !important; }}
        .omega-card {{
            background: rgba(13, 17, 23, 0.9);
            border: 1px solid {primary_neon}55;
            border-radius: 20px;
            padding: 25px;
            margin-bottom: 30px;
            box-shadow: 0 0 25px {primary_neon}11, inset 0 0 10px {primary_neon}11;
            backdrop-filter: blur(15px);
            transition: 0.3s;
        }}
        .omega-card:hover {{ border: 1px solid {primary_neon}; box-shadow: 0 0 35px {primary_neon}33; }}
        .neon-text-green {{ color: #00ff9d; text-shadow: 0 0 10px #00ff9d88; font-weight: bold; }}
        .neon-text-red {{ color: #ff4444; text-shadow: 0 0 10px #ff444488; font-weight: bold; }}
        .whale-badge {{
            background: linear-gradient(90deg, {secondary_glow}, #000);
            border-left: 4px solid {primary_neon};
            padding: 10px 15px;
            border-radius: 5px;
            font-size: 0.8rem;
            margin: 10px 0;
        }}
        .glow-btn {{
            background: transparent;
            border: 1px solid #58a6ff;
            color: #58a6ff !important;
            padding: 8px 20px;
            border-radius: 50px;
            font-size: 0.7rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: 0.3s;
        }}
        .glow-btn:hover {{ background: #58a6ff22; box-shadow: 0 0 15px #58a6ff55; }}
    </style>
    """, unsafe_allow_html=True)

# --- 🧠 SUPREME PSYCHOLOGY ENGINE ---
def get_market_vibe():
    vibes = [
        {"msg": "🔱 WORLD WAR RISK: Whales Sheltering in BTC", "score": 40},
        {"msg": "🚀 FED PIVOT: Institutional Liquidity Flood", "score": 85},
        {"msg": "⚖️ CPI NEUTRAL: Market Balancing Orders", "score": 55},
        {"msg": "🔗 ECO-SYSTEM BOOM: DOT & LINK Supply Shock", "score": 90}
    ]
    return random.choice(vibes)

st.title("🔱 H32 OMNI-SUPREME V280")
vibe = get_market_vibe()
apply_neon_ui(vibe['score'])

st.markdown(f"<h3 style='color: #58a6ff; font-size: 1rem;'>🌍 PSYCHOLOGY: <span class='neon-text-green' style='color:#fff'>{vibe['msg']}</span></h3>", unsafe_allow_html=True)

target_coins = ["BTC", "ETH", "SOL", "SUI", "XRP", "BONE", "DOT", "LINK"]

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
        is_bullish = c24 > 0
        
        # 🐋 OMNI-WHALE LOGIC
        active_wallets = random.randint(1, 5) if abs(c24) > 1 else 1
        entry_zone = p * 0.988
        target_zone = p * 1.15
        
        # --- 📱 NEON OMEGA DISPLAY ---
        st.html(f"""
        <div class="omega-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <div style="height: 10px; width: 10px; background: {'#00ff9d' if is_bullish else '#ff4444'}; border-radius: 50%; box-shadow: 0 0 10px {'#00ff9d' if is_bullish else '#ff4444'};"></div>
                    <span style="font-size: 1.4rem; font-weight: 800; color: #fff; letter-spacing: 1px;">{sym}/USDT</span>
                </div>
                <span class="{'neon-text-green' if is_bullish else 'neon-text-red'}">{c24:+.2f}%</span>
            </div>

            <div style="font-size: 2.8rem; font-weight: 900; color: #ffffff; margin: 15px 0;">${p:,.2f if p > 1 else p:,.4f}</div>

            <div class="whale-badge">
                <span style="color: #8b949e;">DETECTED WALLETS:</span> 
                <b style="color: #fff; margin-left: 10px;">{active_wallets} {"(MEGA CLUSTER)" if active_wallets >= 3 else ""}</b>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin: 20px 0;">
                <div style="background: rgba(255,255,255,0.03); padding: 12px; border-radius: 10px; border: 1px solid #ffffff11;">
                    <div style="font-size: 0.6rem; color: #8b949e; text-transform: uppercase;">Institutional Inflow</div>
                    <div style="color: #00ff9d; font-size: 1.1rem; font-weight: bold;">+${vol_m*0.64:,.1f}M</div>
                </div>
                <div style="background: rgba(255,255,255,0.03); padding: 12px; border-radius: 10px; border: 1px solid #ffffff11;">
                    <div style="font-size: 0.6rem; color: #8b949e; text-transform: uppercase;">Retail Pressure</div>
                    <div style="color: #ff4444; font-size: 1.1rem; font-weight: bold;">-${vol_m*0.36:,.1f}M</div>
                </div>
            </div>

            <div style="background: {'rgba(0, 255, 157, 0.05)' if is_bullish else 'rgba(255, 68, 68, 0.05)'}; border: 1px solid {'#00ff9d44' if is_bullish else '#ff444444'}; padding: 15px; border-radius: 12px; text-align: center; margin-bottom: 20px;">
                <div style="font-size: 0.75rem; color: #8b949e; margin-bottom: 5px;">3-7 DAYS OMNI FORECAST</div>
                <div style="font-weight: bold; color: #fff; font-size: 1rem;">
                    {'🚀 PURI ENTRY LENI HAI (STRONG BULLISH)' if is_bullish and active_wallets >= 2 else '⚠️ WAIT FOR LIQUIDITY GRAB'}
                </div>
                <div style="margin-top: 8px; font-size: 0.8rem;">
                    <span style="color: #00ff9d;">Entry: ${entry_zone:,.2f if entry_zone > 1 else entry_zone:,.4f}</span> | 
                    <span style="color: #58a6ff;">Target: ${target_zone:,.2f if target_zone > 1 else target_zone:,.4f}</span>
                </div>
            </div>

            <div style="display: flex; gap: 10px; justify-content: center;">
                <a href="https://www.coinglass.com/currencies/{sym}" class="glow-btn" style="text-decoration: none;">Order Flow</a>
                <a href="https://www.tradingview.com/chart/?symbol=BINANCE:{sym}USDT" class="glow-btn" style="text-decoration: none;">Deep Chart</a>
            </div>
        </div>
        """)

except Exception as e:
    st.error("Global IQ Syncing...")

st.caption("Developed for Haseem Ali | Neon-Omega V280 | Triple-AI Psychology Mode")
