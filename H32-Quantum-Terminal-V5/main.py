import streamlit as st
import pandas as pd
import ccxt
import requests
import time

st.set_page_config(page_title="H32 Quantum Terminal V5.1", layout="wide", page_icon="⚡")

st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #0a0e17, #11151f); color: #e0e0e0; }
    .big-signal { padding: 25px; border-radius: 20px; text-align: center; font-size: 1.8rem; font-weight: bold; margin: 10px 0; }
</style>
""", unsafe_allow_html=True)

st.title("⚡ H32 QUANTUM TERMINAL V5.1")
st.caption("Multi-Source Data • SMC + Time Intelligence")

with st.sidebar:
    st.header("📍 Watchlist")
    coins = ["BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT", "XRP/USDT", 
             "DOGE/USDT", "ADA/USDT", "AVAX/USDT", "SUI/USDT"]
    symbol = st.selectbox("Select Coin", coins)
    tf = st.selectbox("Timeframe", ["15m", "1h", "4h", "1d"])

@st.cache_data(ttl=30)
def get_data(symbol, timeframe, limit=250):
    sources = ["binance", "kraken", "bybit", "coingecko"]
    
    for source in sources:
        try:
            if source == "coingecko":
                coin = symbol.lower().replace("/usdt", "")
                url = f"https://api.coingecko.com/api/v3/coins/{coin}/ohlc?vs_currency=usd&days=1"
                resp = requests.get(url, timeout=10)
                if resp.status_code == 200:
                    data = resp.json()
                    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close'])
                    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
                    df['volume'] = 0
                    return df
            else:
                exchange = getattr(ccxt, source)({'enableRateLimit': True})
                ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
                df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
                df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
                return df
                
        except:
            continue   # Agla source try karo
    
    return None

# ===================== ANALYSIS =====================
if st.button("🚀 FULL QUANTUM ANALYSIS", type="primary"):
    with st.spinner("Multi sources se data le raha hun..."):
        df = get_data(symbol, tf)
        
        if df is not None and not df.empty:
            price = df['close'].iloc[-1]
            ma20 = df['close'].rolling(20).mean().iloc[-1] if len(df) > 20 else price
            ma50 = df['close'].rolling(50).mean().iloc[-1] if len(df) > 50 else price
            
            if price > ma20 > ma50:
                score = 85
                signal = "🚀 STRONG BUY"
                color = "linear-gradient(90deg,#00ff9d,#00cc7a)"
            else:
                score = 50
                signal = "⛔ HOLD"
                color = "#ff4444"

            col1, col2 = st.columns([2, 3])
            with col1:
                st.metric(f"**{symbol}**", f"${price:,.4f}")
                st.progress(score / 100)
                st.success(f"Confluence: {score}%")
            
            with col2:
                st.markdown(f"<div class='big-signal' style='background:{color}; color:black;'>{signal}</div>", unsafe_allow_html=True)
                st.info("**Structure:** Bullish" if score >= 75 else "**Structure:** Neutral")
                st.write("Next 24-96 hours mein move possible hai.")
        else:
            st.warning("Sab sources busy hain. 15-20 seconds wait karke dubara try karo.")

st.caption("✅ 4 Sources Auto Fallback (Binance + Kraken + Bybit + CoinGecko)")
