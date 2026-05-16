import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# =========================================================
# 🏛️ H32 SMART MONEY RADAR (V59 DEEP HORIZON MATRIX)
# =========================================================

st.set_page_config(
    page_title="H32 SMART MONEY RADAR",
    layout="wide"
)

# =========================================================
# 🔄 BUILT-IN AUTO REFRESH (PULSE CONTROLLER)
# =========================================================
refresh_seconds = 2

st.markdown(
    f"""
    <script>
        setTimeout(function(){{
            window.location.reload();
        }}, {refresh_seconds * 1000});
    </script>
    """,
    unsafe_allow_html=True
)

# =========================================================
# 🎨 UI STYLE DESIGN (HIGH COMPACT CODES)
# =========================================================
st.markdown("""
<style>
.stApp{
    background:linear-gradient(135deg,#020409,#050d1a);
    color:white;
}
.main{
    padding:6px !important;
}
.block-container{
    padding-top:1rem;
}
h1,h2,h3{
    color:white;
}
.buy-box{
    background:linear-gradient(145deg,#071a12,#0a2c1d);
    border:1px solid #00ff88;
    border-radius:8px;
    padding:10px;
}
.sell-box{
    background:linear-gradient(145deg,#220d0d,#341313);
    border:1px solid #ff4b4b;
    border-radius:8px;
    padding:10px;
}
.signal-box{
    background:linear-gradient(145deg,#0a1222,#101c33);
    border:1px solid #3385ff;
    border-radius:8px;
    padding:10px;
}

/* Premium Dedicated Blue Horizon Radar Layout */
.blue-limit-radar {
    background: linear-gradient(145deg, #051529, #09254b);
    border: 2px solid #0052cc;
    border-radius: 8px;
    padding: 10px !important;
    text-align: center;
    font-weight: bold;
    color: #3385ff;
    box-shadow: 0 0 15px rgba(0, 82, 204, 0.3);
}
.big-text{
    font-size:1.15rem;
    font-weight:bold;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 📂 SIDEBAR CONFIGURATION
# =========================================================
st.sidebar.title("🏛️ H32 CONTROL PANEL")

watchlist = ["ETH", "BTC", "SOL", "DOGE", "XRP", "SHIB", "BONE"]
selected_asset = st.sidebar.selectbox("📊 SELECT ASSET", watchlist)
depth_limit = st.sidebar.slider("📚 ORDERBOOK DEPTH STREAM", 20, 500, 100)

# =========================================================
# 🌐 REQUEST SESSION & DATA INJECTOR
# =========================================================
session = requests.Session()

@st.cache_data(ttl=1)
def fetch_market_data(symbol):
    try:
        # Price
        price_url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"
        price_res = session.get(price_url, timeout=1.5).json()

        # 24H Stats
        stats_url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}USDT"
        stats_res = session.get(stats_url, timeout=1.5).json()

        # Full Depth Stack Arrays
        depth_url = f"https://api.binance.com/api/v3/depth?symbol={symbol}USDT&limit={depth_limit}"
        depth_res = session.get(depth_url, timeout=1.5).json()

        return {
            "price": float(price_res["price"]),
            "high": float(stats_res["highPrice"]),
            "low": float(stats_res["lowPrice"]),
            "change": float(stats_res["priceChangePercent"]),
            "bids": depth_res["bids"],
            "asks": depth_res["asks"]
        }
    except Exception as e:
        st.error(f"SATELLITE LINK ERROR: {e}")
        return None

# Load System Telemetry
data = fetch_market_data(selected_asset)
if data is None:
    st.stop()

live_price = data["price"]
high_price = data["high"]
low_price = data["low"]
change_percent = data["change"]
bids_raw = data["bids"]
asks_raw = data["asks"]

# =========================================================
# 🧠 EXTENDED RADAR HORIZON (Awwal se Aakhir tak Tracking)
# =========================================================
# Identify the absolute boundaries of the active seller cluster array
true_sell_start = float(asks_raw[0][0])     # Pehli selling price point jahan se queue shuru hai
true_sell_max_end = float(asks_raw[-1][0])  # Aakhri limit jahan tak order layers mapped hain

# Standard single max point matching logic for display boxes
largest_bid = max(bids_raw, key=lambda x: float(x[1]))
largest_ask = max(asks_raw, key=lambda x: float(x[1]))

buy_wall_price = float(largest_bid[0])
buy_wall_qty = float(largest_bid[1])
sell_wall_price = float(largest_ask[0])
sell_wall_qty = float(largest_ask[1])

# Volume pressure balances
total_bid_volume = sum(float(x[1]) for x in bids_raw)
total_ask_volume = sum(float(x[1]) for x in asks_raw)

signal = "🟨 SIDEWAYS"
if total_bid_volume > total_ask_volume * 1.5:
    signal = "🟩 WHALE BUY PRESSURE"
elif total_ask_volume > total_bid_volume * 1.5:
    signal = "🟥 HEAVY SELL PRESSURE"

# =========================================================
# 📊 DISPLAY MAIN PANEL
# =========================================================
st.title(f"🏛️ H32 SMART MONEY RADAR — {selected_asset}/USDT")

# Dynamic layout structure showing metrics with explicit Blue Horizon Injection
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🔴 LIVE PRICE", f"${live_price:,.2f}", f"{change_percent:+.2f}%")
with col2:
    st.metric("📈 24H HIGH", f"${high_price:,.2f}")
with col3:
    st.metric("📉 24H LOW", f"${low_price:,.2f}")
with col4:
    # 🔷 Target Blue Box showcasing absolute history endpoints of active sells
    st.markdown(
        f"<div class='blue-limit-radar'>🔷 SELLING HORIZON LIMIT<br>"
        f"<span style='font-size:1.1rem; color:white;'>${true_sell_start:,.2f} ➔ ${true_sell_max_end:,.2f}</span></div>",
        unsafe_allow_html=True
    )

st.write("---")

# =========================================================
# 🟩 BUY / SELL WALLS DETAILED CARD PANELS
# =========================================================
left, right = st.columns(2)

with left:
    st.markdown("<div class='buy-box'>", unsafe_allow_html=True)
    st.subheader("🟩 WHALE BUY ENTRY (FLOOR)")
    st.markdown(f"<div class='big-text'>${buy_wall_price:,.2f}</div>", unsafe_allow_html=True)
    st.write(f"📦 Peak Quantity: {buy_wall_qty:,.2f}")
    st.write("🎯 Key institutional accumulation base block identified.")
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown("<div class='sell-box'>", unsafe_allow_html=True)
    st.subheader("🟥 WHALE SELLING HORIZON TRACKER")
    st.markdown(f"<div class='big-text'>${true_sell_start:,.2f} Upto ${true_sell_max_end:,.2f}</div>", unsafe_allow_html=True)
    st.write(f"📦 Max Single Wall Level Price: ${sell_wall_price:,.2f} (Qty: {sell_wall_qty:,.2f})")
    st.write("⚠️ Continuous orderbook spectrum range captured from initial to terminal depth.")
    st.markdown("</div>", unsafe_allow_html=True)

st.write("---")

# =========================================================
# 🛰️ PRESSURE METRICS
# =========================================================
st.markdown("<div class='signal-box'>", unsafe_allow_html=True)
st.subheader("🛰️ INSTITUTIONAL VOLUME MATRIX BALANCE")
st.write(f"🟩 Total Cumulative Bid Volume: {total_bid_volume:,.2f}")
st.write(f"🟥 Total Cumulative Ask Volume: {total_ask_volume:,.2f}")

if signal == "🟩 WHALE BUY PRESSURE":
    st.success("Whale orders backing the book. Breakout tracking active.")
elif signal == "🟥 HEAVY SELL PRESSURE":
    st.error("Distribution ongoing across the horizon. Guard spot positions.")
else:
    st.warning("Range-bound order structures. Neutral accumulation phase.")
st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# 📊 ORDERBOOK DATA SHEETS
# =========================================================
buy_df = pd.DataFrame(bids_raw[:15], columns=["Price", "Quantity"])
sell_df = pd.DataFrame(asks_raw[:15], columns=["Price", "Quantity"])

buy_df["Price"] = buy_df["Price"].astype(float)
buy_df["Quantity"] = buy_df["Quantity"].astype(float)
sell_df["Price"] = sell_df["Price"].astype(float)
sell_df["Quantity"] = sell_df["Quantity"].astype(float)

col_a, col_b = st.columns(2)
with col_a:
    st.subheader("🟩 TOP BUY LIMIT ORDERS")
    st.dataframe(buy_df, use_container_width=True, hide_index=True)

with col_b:
    st.subheader("🟥 TOP SEQUENTIAL SELL LIMITS")
    st.dataframe(sell_df, use_container_width=True, hide_index=True)

# Footer Info
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.write("---")
st.caption(f"🏛️ H32 GLOBAL SMART MONEY RADAR V59 ACTIVE | 🕒 {current_time} | Refresh Pulse Sync Online")
