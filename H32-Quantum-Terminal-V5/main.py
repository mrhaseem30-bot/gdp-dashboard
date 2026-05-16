import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# =========================================================
# 🏛️ H32 SMART MONEY RADAR
# =========================================================

st.set_page_config(
    page_title="H32 SMART MONEY RADAR",
    layout="wide"
)

# =========================================================
# 🔄 BUILT-IN AUTO REFRESH
# =========================================================

refresh_seconds = 3

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
# 🎨 UI STYLE
# =========================================================

st.markdown("""
<style>

.stApp{
    background:linear-gradient(135deg,#020409,#07111f);
    color:white;
}

.main{
    padding:8px !important;
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
    border-radius:10px;
    padding:12px;
}

.sell-box{
    background:linear-gradient(145deg,#220d0d,#341313);
    border:1px solid #ff4b4b;
    border-radius:10px;
    padding:12px;
}

.signal-box{
    background:linear-gradient(145deg,#0a1222,#101c33);
    border:1px solid #3385ff;
    border-radius:10px;
    padding:12px;
}

.big-text{
    font-size:1.2rem;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# 📂 SIDEBAR
# =========================================================

st.sidebar.title("🏛️ H32 CONTROL PANEL")

watchlist = [
    "BTC",
    "ETH",
    "SOL",
    "DOGE",
    "XRP",
    "SHIB",
    "BONE"
]

selected_asset = st.sidebar.selectbox(
    "📊 SELECT ASSET",
    watchlist
)

depth_limit = st.sidebar.slider(
    "📚 ORDERBOOK DEPTH",
    20,
    500,
    100
)

# =========================================================
# 🌐 REQUEST SESSION
# =========================================================

session = requests.Session()

# =========================================================
# 📡 FETCH MARKET DATA
# =========================================================

@st.cache_data(ttl=2)
def fetch_market_data(symbol):

    try:

        # PRICE
        price_url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"
        price_res = session.get(price_url, timeout=2).json()

        # 24H
        stats_url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}USDT"
        stats_res = session.get(stats_url, timeout=2).json()

        # DEPTH
        depth_url = f"https://api.binance.com/api/v3/depth?symbol={symbol}USDT&limit={depth_limit}"
        depth_res = session.get(depth_url, timeout=2).json()

        price = float(price_res["price"])

        high = float(stats_res["highPrice"])
        low = float(stats_res["lowPrice"])
        change = float(stats_res["priceChangePercent"])

        bids = depth_res["bids"]
        asks = depth_res["asks"]

        return {
            "price": price,
            "high": high,
            "low": low,
            "change": change,
            "bids": bids,
            "asks": asks
        }

    except Exception as e:

        st.error(f"API ERROR: {e}")

        return None

# =========================================================
# 📊 LOAD DATA
# =========================================================

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
# 🧠 SMART MONEY ANALYSIS
# =========================================================

largest_bid = max(
    bids_raw,
    key=lambda x: float(x[1])
)

largest_ask = max(
    asks_raw,
    key=lambda x: float(x[1])
)

buy_wall_price = float(largest_bid[0])
buy_wall_qty = float(largest_bid[1])

sell_wall_price = float(largest_ask[0])
sell_wall_qty = float(largest_ask[1])

# =========================================================
# 📈 VOLUME PRESSURE
# =========================================================

total_bid_volume = sum(
    float(x[1]) for x in bids_raw
)

total_ask_volume = sum(
    float(x[1]) for x in asks_raw
)

# =========================================================
# 🚨 AI SIGNAL ENGINE
# =========================================================

signal = "🟨 SIDEWAYS"

if total_bid_volume > total_ask_volume * 1.5:
    signal = "🟩 WHALE BUY PRESSURE"

elif total_ask_volume > total_bid_volume * 1.5:
    signal = "🟥 HEAVY SELL PRESSURE"

# =========================================================
# 📊 HEADER
# =========================================================

st.title(f"🏛️ H32 SMART MONEY RADAR — {selected_asset}/USDT")

# =========================================================
# 📌 METRICS
# =========================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "🔴 LIVE PRICE",
        f"${live_price:,.2f}",
        f"{change_percent:+.2f}%"
    )

with col2:
    st.metric(
        "📈 24H HIGH",
        f"${high_price:,.2f}"
    )

with col3:
    st.metric(
        "📉 24H LOW",
        f"${low_price:,.2f}"
    )

with col4:
    st.metric(
        "🧠 AI SIGNAL",
        signal
    )

st.write("---")

# =========================================================
# 🟩 BUY / SELL WALLS
# =========================================================

left, right = st.columns(2)

with left:

    st.markdown("<div class='buy-box'>", unsafe_allow_html=True)

    st.subheader("🟩 WHALE BUY ENTRY")

    st.markdown(
        f"<div class='big-text'>${buy_wall_price:,.2f}</div>",
        unsafe_allow_html=True
    )

    st.write(f"📦 Buy Quantity: {buy_wall_qty:,.2f}")

    st.write("🎯 Large limit buyers detected.")

    st.markdown("</div>", unsafe_allow_html=True)

with right:

    st.markdown("<div class='sell-box'>", unsafe_allow_html=True)

    st.subheader("🟥 WHALE SELL WALL")

    st.markdown(
        f"<div class='big-text'>${sell_wall_price:,.2f}</div>",
        unsafe_allow_html=True
    )

    st.write(f"📦 Sell Quantity: {sell_wall_qty:,.2f}")

    st.write("⚠️ Distribution zone detected.")

    st.markdown("</div>", unsafe_allow_html=True)

st.write("---")

# =========================================================
# 🛰️ PRESSURE ANALYSIS
# =========================================================

st.markdown("<div class='signal-box'>", unsafe_allow_html=True)

st.subheader("🛰️ INSTITUTIONAL PRESSURE ANALYSIS")

st.write(f"🟩 Total Bid Volume: {total_bid_volume:,.2f}")
st.write(f"🟥 Total Ask Volume: {total_ask_volume:,.2f}")

if signal == "🟩 WHALE BUY PRESSURE":

    st.success("Buyers dominating orderbook. Breakout possible.")

elif signal == "🟥 HEAVY SELL PRESSURE":

    st.error("Sellers dominating orderbook. Dump risk elevated.")

else:

    st.warning("Market neutral. Accumulation phase.")

st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# 📚 ORDERBOOK TABLES
# =========================================================

buy_df = pd.DataFrame(
    bids_raw[:15],
    columns=["Price", "Quantity"]
)

sell_df = pd.DataFrame(
    asks_raw[:15],
    columns=["Price", "Quantity"]
)

buy_df["Price"] = buy_df["Price"].astype(float)
buy_df["Quantity"] = buy_df["Quantity"].astype(float)

sell_df["Price"] = sell_df["Price"].astype(float)
sell_df["Quantity"] = sell_df["Quantity"].astype(float)

# =========================================================
# 📊 DISPLAY TABLES
# =========================================================

col_a, col_b = st.columns(2)

with col_a:

    st.subheader("🟩 TOP BUY LIMIT ORDERS")

    st.dataframe(
        buy_df,
        use_container_width=True,
        hide_index=True
    )

with col_b:

    st.subheader("🟥 TOP SELL LIMIT ORDERS")

    st.dataframe(
        sell_df,
        use_container_width=True,
        hide_index=True
    )

# =========================================================
# 🕒 FOOTER
# =========================================================

current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

st.write("---")

st.caption(f"""
🏛️ H32 GLOBAL SMART MONEY RADAR ACTIVE  
🛰️ Live Binance Orderbook Connected  
🕒 {current_time}
""")
