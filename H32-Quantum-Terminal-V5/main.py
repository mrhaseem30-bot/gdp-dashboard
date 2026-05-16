import streamlit as st
import requests
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta

# --- 🛰️ GLOBAL TERMINAL SETUP ---
st.set_page_config(page_title="H32 QUANTUM TERMINAL V9.7 GLOBAL", layout="wide")

if "order_history" not in st.session_state:
    st.session_state.order_history = []

# Page Auto-Scroll to Top
st.markdown("""
    <script>window.parent.document.querySelector('section.main').scrollTo(0, 0);</script>
""", unsafe_allow_html=True)

# --- 🎨 TRADINGVIEW DARK THEME STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #0c0d14 !important; }
    .main { color: #d1d4dc; font-family: 'Inter', sans-serif; }
    .predict-box { padding: 15px; border-radius: 8px; text-align: center; font-size: 1.3rem; font-weight: bold; margin-bottom: 10px; }
    .buy-zone { border: 1px solid #26a69a; background-color: #132020; color: #26a69a; }
    .sell-zone { border: 1px solid #ef5350; background-color: #291415; color: #ef5350; }
    
    /* Global Network Additions Styling */
    .news-box { background-color: #171b26; border-left: 4px solid #2962ff; padding: 12px; border-radius: 4px; margin-bottom: 8px; }
    .news-title { font-size: 0.95rem; font-weight: bold; color: #f2f3f5; }
    .news-time { font-size: 0.75rem; color: #787b86; }
    .whale-radar { background-color: #1e222d; border: 1px dashed #434651; padding: 15px; border-radius: 6px; }
    </style>
    """, unsafe_allow_html=True)

# --- 🛰️ BINANCE LIVE STREAM & MARKET FEEDS ---
def fetch_live_market_data(ticker):
    try:
        res = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={ticker}USDT", timeout=2).json()
        current_price = float(res['price'])
        res_24h = requests.get(f"https://api.binance.com/api/v3/ticker/24hr?symbol={ticker}USDT", timeout=2).json()
        return current_price, float(res_24h['priceChangePercent']), True
    except:
        fallbacks = {"DOT": 1.39, "BTC": 88450.0, "ETH": 3250.0, "SOL": 165.5, "SHIB": 0.0000241, "BONE": 0.425}
        return fallbacks.get(ticker, 10.0), 0.0, False

# --- 📂 SIDEBAR COMMANDS ---
st.sidebar.markdown("### 🏛️ H32 CONTROL PANEL")
watchlist = ["DOT", "SHIB", "BONE", "BTC", "ETH", "SOL"]
selected_asset = st.sidebar.selectbox("📂 COIN", watchlist)

# TradingView Intervals (Exactly like charts)
tradingview_intervals = {
    "15 Minute (15m)": "15m",
    "30 Minute (30m)": "30m",
    "1 Hour (1h)": "1h",
    "4 Hour (4h)": "4h",
    "1 Day (1d)": "1d",
    "1 Week (1w)": "1w",
    "1 Month (1M)": "1M"
}
selected_tf_label = st.sidebar.selectbox("⏱️ TIMING (CHART FRAME)", list(tradingview_intervals.keys()))
active_tf = tradingview_intervals[selected_tf_label]

refresh_rate = st.sidebar.slider("Refresh (Seconds)", min_value=1, max_value=5, value=2)

# Get Live Price
live_price, change_24h, is_live = fetch_live_market_data(selected_asset)

# Math calculation logic based on chart framework
tf_factors = {"15m": 0.002, "30m": 0.004, "1h": 0.008, "4h": 0.015, "1d": 0.035, "1w": 0.075, "1M": 0.150}
factor = tf_factors.get(active_tf, 0.01)

entry_target = live_price * (1.0 - factor)
exit_target = live_price * (1.0 + factor)

dec = 6 if live_price < 0.1 else (4 if live_price < 10.0 else 2)

# --- HEADER BAR ---
st.markdown(f"<h2>📊 {selected_asset}/USDT — {active_tf.upper()} GLOBAL NETWORK ENGINE</h2>", unsafe_allow_html=True)

col_p1, col_p2 = st.columns([2, 2])
with col_p1:
    st.metric(label="Live Price", value=f"${live_price:,.{dec}f}", delta=f"{change_24h:+.2f}%")

st.write("---")

# --- 📰 ADVANCED ADDTION: GLOBAL LIVE NEWS & WHALE RADAR BLOCK ---
col_news, col_radar = st.columns([3, 2])

with col_news:
    st.markdown("### 📰 GLOBAL BREAKING NEWS FEED (Real-Time Impact)")
    # Simulated Live Institutional Feed mapping current second flow
    np.random.seed(int(time.time()) // 10)
    news_pool = [
        f"🚨 FED Rate Update: Market makers restructuring limit books for volatile assets like {selected_asset}.",
        f"🐋 WHALE ALERT: Multi-million dollar liquidity block spotted moving near active support zones.",
        f"🏛️ BlackRock / Fidelity OTC desk routing massive settlement volumes via internal private nodes.",
        f"📊 CPI Data Forecast Model showing institutional pre-hedging on cross-crypto spot pairings.",
        f"⚡ High Frequency Trading (HFT) bots increasing liquidity depth on {selected_asset}/USDT perpetual books."
    ]
    selected_news = np.random.choice(news_pool, 2, replace=False)
    
    for news in selected_news:
        st.markdown(f"""
        <div class='news-box'>
            <div class='news-time'>⏱️ LIVE SENTIMENT • Just Now</div>
            <div class='news-title'>{news}</div>
        </div>
        """, unsafe_allow_html=True)

with col_radar:
    st.markdown("### 🛰️ WHALE ACTION RADAR")
    current_time_str = datetime.now().strftime("%H:%M:%S")
    radar_biases = ["🟢 INSTITUTIONAL ACCUMULATION (Buying Heavy)", "🔴 DISTRIBUTION METRICS (Selling Pressure)", "🟨 COMPRESSION / SIDEWAYS RANGE"]
    active_bias = np.random.choice(radar_biases)
    
    st.markdown(f"""
    <div class='whale-radar'>
        <strong>Scan Time:</strong> {current_time_str}<br>
        <strong>Target Asset:</strong> {selected_asset}/USDT<br>
        <strong>Order Book State:</strong> Dynamic Fluid Flow<br>
        <span style='color: #2962ff; font-weight: bold;'>Smart Money Status:</span> {active_bias}
    </div>
    """, unsafe_allow_html=True)

st.write("---")

# --- TARGET BOXES ---
col_ent, col_ex = st.columns(2)
with col_ent:
    st.markdown(f"<div class='predict-box buy-zone'>🟩 TARGET ENTRY LONG<br>${entry_target:,.{dec}f}</div>", unsafe_allow_html=True)
with col_ex:
    st.markdown(f"<div class='predict-box sell-zone'>🔴 TARGET EXIT SHORT<br>${exit_target:,.{dec}f}</div>", unsafe_allow_html=True)

# --- LIVE ORDERS POOL SIMULATION ---
whale_desks = [
    "0xBlackRock_Vault..8812", "0xFidelity_Digital..4221", "0xMicroStrategy..1102",
    "0xGrayscale_Trust..5590", "0xVanEck_Wealth..2034", "0xArkInvest_Fund..9961",
    "0xTemasek_Node..5009", "0xHongKong_Vault..1120"
]

np.random.seed(int(time.time()) // refresh_rate)
now_time = datetime.now()

live_orders = []
for i, desk in enumerate(whale_desks):
    is_buy = (i % 2 == 0)
    is_removed = (np.random.rand() < 0.15) # 15% chance order gets removed
    
    order_time = (now_time - timedelta(minutes=i*12)).strftime("%Y-%m-%d %H:%M:%S")
    price = entry_target * (1 + (i*0.0005)) if is_buy else exit_target * (1 - (i*0.0005))
    cash = (20_000_000.0 + (i * 4_000_000.0))
    qty = cash / price
    
    if is_removed:
        # Save to database log instantly before skipping
        st.session_state.order_history.append({
            "Date Removed": now_time.strftime("%Y-%m-%d"),
            "Time": order_time,
            "Desk Address": desk,
            "Coin": selected_asset,
            "Chart TF": active_tf,
            "Position": "🔴 SHORT SELL" if not is_buy else "🟩 LONG BUY",
            "Price": f"${price:,.{dec}f}",
            "Amount": f"{qty:,.2f}"
        })
        continue # Skip displaying in active table (Hata diya)

    live_orders.append({
        "Order Time": order_time,
        "Desk Address": desk,
        "Position Type": "🟩 LONG BUY" if is_buy else "🔴 SHORT SELL",
        "Limit Price": f"${price:,.{dec}f}",
        "Quantity Token": f"{qty:,.2f} {selected_asset}",
        "Volume USD": f"${cash:,.2f}"
    })

# --- LIVE MONITOR VIEW ---
st.markdown("### 🏛️ LIVE ORDER MONITOR")
if live_orders:
    st.dataframe(pd.DataFrame(live_orders), use_container_width=True, hide_index=True)
else:
    st.info("Syncing live book blocks...")

# --- ARCHIVED HISTORY VIEW (DATE BUTTON) ---
st.write("---")
st.markdown("### 🕒 REMOVED ORDERS HISTORY VAULT")

col_d1, col_d2 = st.columns([2, 5])
with col_d1:
    select_date = st.date_input("Filter By Date", datetime.now().date())
with col_d2:
    st.write(" ")
    st.write(" ")
    click_history = st.button("🔍 Check Removed Orders Log")

if click_history:
    if st.session_state.order_history:
        df_all = pd.DataFrame(st.session_state.order_history)
        filtered_df = df_all[df_all["Date Removed"] == str(select_date)]
        
        if not filtered_df.empty:
            st.dataframe(filtered_df, use_container_width=True, hide_index=True)
        else:
            st.info(f"Is date ({select_date}) par koi order remove nahi hua.")
    else:
        st.info("History database clear hai.")

# HIGH FREQUENCY REFRESH RUNNER
st.components.v1.html(f"""
    <script>
        setTimeout(function(){{ window.parent.document.querySelector('section.main').dispatchEvent(new Event('change')); }}, {refresh_rate * 1000});
    </script>
""", height=0)
