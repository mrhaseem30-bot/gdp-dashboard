import streamlit as st
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time

# ====================== CONFIG ======================
st.set_page_config(page_title="H32 GLOBAL RADAR V58", layout="wide", initial_sidebar_state="expanded")

# Persistent 30-day Vaults
if "persistent_buy_vault_30d" not in st.session_state:
    st.session_state.persistent_buy_vault_30d = []
if "persistent_sell_vault_30d" not in st.session_state:
    st.session_state.persistent_sell_vault_30d = []

# ====================== STYLING ======================
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #020409, #050a14); color: #f0f6fc; }
    .main { padding: 8px !important; }
    h2, h3 { margin: 4px 0 !important; font-weight: 800; }
    
    .blue-limit-radar {
        background: linear-gradient(145deg, #051429, #092347);
        border: 2px solid #0052cc;
        border-radius: 8px;
        padding: 12px;
        text-align: center;
        font-weight: bold;
        color: #3385ff;
        box-shadow: 0 0 20px rgba(0, 82, 204, 0.4);
    }
    
    .terminal-card {
        background-color: #080d16;
        border: 1px solid #162235;
        border-radius: 8px;
        padding: 12px;
        text-align: center;
    }
    .split-box-inflow { background: linear-gradient(145deg, #041a10, #082618); border: 1px solid #00ff88; border-radius: 8px; padding: 12px; }
    .split-box-outflow { background: linear-gradient(145deg, #200a0c, #301013); border: 1px solid #ff4b4b; border-radius: 8px; padding: 12px; }
    
    .stMetricValue { font-size: 1.1rem !important; font-weight: bold; }
    .stDataFrame { font-size: 0.78rem; }
</style>
""", unsafe_allow_html=True)

def format_cash(val):
    if abs(val) >= 1_000_000_000:
        return f"${val/1e9:.3f}B"
    elif abs(val) >= 1_000_000:
        return f"${val/1e6:.2f}M"
    return f"${val:,.0f}"

# ====================== DATA FETCH ======================
@st.cache_data(ttl=2)
def fetch_market_data(ticker):
    try:
        price_res = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={ticker}USDT", timeout=1.5).json()
        depth = requests.get(f"https://api.binance.com/api/v3/depth?symbol={ticker}USDT&limit=50", timeout=1.5).json()
        stats = requests.get(f"https://api.binance.com/api/v3/ticker/24hr?symbol={ticker}USDT", timeout=1.5).json()

        current = float(price_res['price'])
        high = float(stats['highPrice'])
        low = float(stats['lowPrice'])
        change = float(stats['priceChangePercent'])

        bids = depth['bids']
        asks = depth['asks']

        return {
            "price": current,
            "high": high,
            "low": low,
            "change": change,
            "buy_floor": float(bids[0][0]),
            "sell_start": float(asks[0][0]),
            "sell_end": float(asks[-1][0])
        }
    except:
        # Fallback
        fallback_data = {
            "ETH": {"price": 2194.21, "high": 2350, "low": 2110.5, "change": -3.2, "buy_floor": 2150, "sell_start": 2210, "sell_end": 2450},
            "BTC": {"price": 68250, "high": 69500, "low": 67000, "change": 1.2, "buy_floor": 67500, "sell_start": 69000, "sell_end": 72000}
        }.get(ticker, {"price": 1.0, "high": 1.1, "low": 0.9, "change": 0, "buy_floor": 0.95, "sell_start": 1.0, "sell_end": 1.1})
        return fallback_data

# ====================== SIDEBAR ======================
st.sidebar.markdown("### 🏛️ HORIZON ENGINE CONTROLS V58")
watchlist = ["ETH", "BTC", "SOL", "DOT", "SHIB", "BONE"]
selected_asset = st.sidebar.selectbox("📂 SELECT ASSET", watchlist)
refresh_rate = st.sidebar.slider("🔄 Sync Pulse Speed (sec)", 1, 5, 2)

# ====================== LIVE DATA ======================
data = fetch_market_data(selected_asset)
live_price = data["price"]
d_high = data["high"]
d_low = data["low"]
d_change = data["change"]
true_buy_floor = data["buy_floor"]
true_sell_start = data["sell_start"]
true_sell_end = data["sell_end"]

# ETH special override (as per original)
if selected_asset == "ETH":
    true_buy_floor = 2150.00
    true_sell_start = 2210.00
    true_sell_end = 2450.00

dec = 6 if live_price < 0.1 else 2
now_time = datetime.now()

# ====================== UI ======================
st.markdown(f"<h2>🏛:// ALADDIN QUANTUM NERVE CENTER — {selected_asset}/USDT</h2>", unsafe_allow_html=True)

col_m1, col_m2, col_m3, col_m4 = st.columns(4)
with col_m1:
    st.metric("🔴 Live Spot Price", f"${live_price:,.{dec}f}", f"{d_change:+.2f}%")
with col_m2:
    st.metric("📈 24h High", f"${d_high:,.{dec}f}")
with col_m3:
    st.metric("📉 24h Low", f"${d_low:,.{dec}f}")
with col_m4:
    st.markdown(f"""
    <div class='blue-limit-radar'>
        🔷 SELL WALL (SHURU → AAKHIR)<br>
        <span style='font-size:1.1rem;color:white;'>${true_sell_start:,.{dec}f} → ${true_sell_end:,.{dec}f}</span>
    </div>
    """, unsafe_allow_html=True)

# ====================== 3-BRAIN PANEL ======================
st.markdown("### 🧠 SATELLITE 3-BRAIN INTEGRATION")
col_b1, col_b2, col_b3 = st.columns(3)
with col_b1:
    st.markdown(f"<div class='terminal-card'><b>🎯 AI 1: BIT-NOTE</b><br><span style='color:#00ff88;font-size:1.1rem;'>BUY FLOOR → ${true_buy_floor:,.{dec}f}</span></div>", unsafe_allow_html=True)
with col_b2:
    st.markdown(f"<div class='terminal-card'><b>🛰️ AI 2: BIT-GLASS</b><br><span style='color:#ff4b4b;font-size:1.1rem;'>SELL RADAR ACTIVE</span></div>", unsafe_allow_html=True)
with col_b3:
    st.markdown(f"<div class='terminal-card'><b>🏛️ AI 3: BLACKROCK VAULT</b><br><span style='color:#ff9b05;font-size:1.1rem;'>30-DAY ARCHIVE SYNC</span></div>", unsafe_allow_html=True)

st.write("---")

# ====================== SIMULATED INSTITUTIONAL DATA ======================
exchanges = ["Binance Core Book", "Coinbase Prime", "OKX Liquidity", "Bybit Institutional", "Upbit Whale Vault"]
desks = ["0xBlackRock_Aladdin..8812", "0xFidelity..4221", "0xMicroStrategy..1102", "0xGrayscale..5590", "0xAbuDhabi..3012"]

np.random.seed(int(time.time() * 1000) % 10000)

for i in range(len(desks)):
    offset_days = np.random.randint(0, 29)
    sim_date = now_time - timedelta(days=offset_days, hours=i*4, minutes=i*15)
    ts_str = sim_date.strftime("%Y-%m-%d %H:%M:%S")

    # Buy Simulation
    buy_level = true_buy_floor * (1 - i * 0.0015)
    cash_buy = 52_000_000 + i * 4_800_000
    qty_buy = cash_buy / buy_level

    st.session_state.persistent_buy_vault_30d.append({
        "Timestamp Log": ts_str,
        "Exchange": exchanges[i],
        "Whale Desk": desks[i],
        "Price": f"${buy_level:,.{dec}f}",
        "Qty": f"{qty_buy:,.2f} {selected_asset}",
        "Capital": format_cash(cash_buy),
        "RawTime": sim_date,
        "Type": "BUY"
    })

    # Sell Simulation
    step = i / max(1, len(desks)-1)
    sell_level = true_sell_start + step * (true_sell_end - true_sell_start)
    cash_sell = 39_000_000 + i * 7_800_000
    qty_sell = cash_sell / sell_level

    st.session_state.persistent_sell_vault_30d.append({
        "Timestamp Log": ts_str,
        "Exchange": exchanges[(i+2)%5],
        "Whale Desk": desks[(i+3)%5],
        "Price": f"${sell_level:,.{dec}f}",
        "Qty": f"{qty_sell:,.2f} {selected_asset}",
        "Capital": format_cash(cash_sell),
        "RawTime": sim_date,
        "Type": "SELL"
    })

# Cleanup older than 30 days
cutoff = now_time - timedelta(days=30)
st.session_state.persistent_buy_vault_30d = [x for x in st.session_state.persistent_buy_vault_30d if x["RawTime"] >= cutoff]
st.session_state.persistent_sell_vault_30d = [x for x in st.session_state.persistent_sell_vault_30d if x["RawTime"] >= cutoff]

# ====================== DISPLAY VAULTS ======================
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("<div class='split-box-inflow'><div style='color:#00ff88;font-weight:bold;text-align:center;'>🟩 AI 1: BUYING VAULT (Accumulation)</div>", unsafe_allow_html=True)
    df_buy = pd.DataFrame(st.session_state.persistent_buy_vault_30d[-7:]).drop(columns=["RawTime", "Type"], errors='ignore')
    st.dataframe(df_buy, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_right:
    st.markdown("<div class='split-box-outflow'><div style='color:#ff4b4b;font-weight:bold;text-align:center;'>🟥 AI 2: SELLING VAULT (Shuru → Aakhir)</div>", unsafe_allow_html=True)
    df_sell = pd.DataFrame(st.session_state.persistent_sell_vault_30d[-7:]).drop(columns=["RawTime", "Type"], errors='ignore')
    st.dataframe(df_sell, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Auto Refresh
st.components.v1.html(f"""
<script>
    setTimeout(() => location.reload(), {refresh_rate * 1000});
</script>
""", height=0)

st.caption("H32 GLOBAL RADAR V58 • Deep Horizon Scanner • Optimized & Accelerated")
