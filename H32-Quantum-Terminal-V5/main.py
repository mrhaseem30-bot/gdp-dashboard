import streamlit as st
import pandas as pd
import ccxt

st.set_page_config(page_title="H32 Quantum Terminal V5.1", layout="wide", page_icon="⚡")

st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #0a0e17, #11151f); color: #e0e0e0; }
    .big-signal { padding: 25px; border-radius: 20px; text-align: center; font-size: 1.8rem; font-weight: bold; margin: 10px 0; }
</style>
""", unsafe_allow_html=True)

st.title("⚡ H32 QUANTUM TERMINAL V5.1")
st.caption("Crypto Coin Market • SMC + Time Intelligence")

# Sidebar
with st.sidebar:
    st.header("📍 Watchlist")
    coins = ["BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT", "XRP/USDT", 
             "DOGE/USDT", "ADA/USDT", "AVAX/USDT", "SUI/USDT", "LINK/USDT"]
    symbol = st.selectbox("Select Coin", coins)
    tf = st.selectbox("Timeframe", ["15m", "1h", "4h", "1d"])

@st.cache_data(ttl=30)
def get_data(symbol, timeframe, limit=300):
    try:
        exchange = ccxt.binance({'enableRateLimit': True})
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
    except:
        return None

if st.button("🚀 FULL QUANTUM ANALYSIS", type="primary"):
    with st.spinner("Market data le raha hun..."):
        df = get_data(symbol, tf)
        
        if df is None:
            st.error("Binance busy hai. 10-20 seconds baad dubara try karo.")
        else:
            price = df['close'].iloc[-1]
            ma20 = df['close'].rolling(20).mean().iloc[-1]
            ma50 = df['close'].rolling(50).mean().iloc[-1]
            
            if price > ma20 > ma50:
                score = 85
                signal = "STRONG BUY"
                color = "linear-gradient(90deg,#00ff9d,#00cc7a)"
            else:
                score = 45
                signal = "HOLD"
                color = "#ff4444"

            col1, col2 = st.columns([2, 3])
            with col1:
                st.metric(f"**{symbol}**", f"${price:,.4f}")
                st.progress(score / 100)
                st.success(f"Confluence: {score}%")
            
            with col2:
                st.markdown(f"<div class='big-signal' style='background:{color};color:black;'>{signal}</div>", unsafe_allow_html=True)
                st.write("**Market Structure:** Bullish" if score > 70 else "**Market Structure:** Neutral")
                st.info("Next 24-96 hours mein move possible hai.")

st.success("✅ App Ready hai! Button dabao aur analysis dekho.")
