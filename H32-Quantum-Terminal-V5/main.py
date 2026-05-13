import streamlit as st
import pandas as pd
import requests
from macro_sentinel import get_macro_context
from smc_engine import get_quantum_decision
from ai_analyst import get_ai_verdict_with_timeframe
from tts_urdu import speak_urdu

st.set_page_config(page_title="H32 Quantum V9.4", layout="wide")

# Strong Dark Professional Background
st.markdown("""
<style>
    .stApp { background: #05070f !important; color: #e0e0e0; }
    .big-signal { padding: 35px; border-radius: 22px; text-align: center; font-size: 2.6rem; font-weight: bold; margin: 20px 0; box-shadow: 0 0 35px rgba(0,255,150,0.4); }
    .alert-box { background: #0f1629; padding: 22px; border-radius: 16px; border-left: 7px solid #00ff9d; margin: 15px 0; }
    .header { font-size: 2.8rem; font-weight: bold; color: #00ff9d; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='header'>H32 QUANTUM TRADING TERMINAL V9.4</h1>", unsafe_allow_html=True)
st.caption("Satellite + Macro + Global Finance Intelligence")

with st.sidebar:
    st.header("📍 Watchlist")
    coins = ["BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT", "XRP/USDT", "AVAX/USDT", "SUI/USDT"]
    symbol = st.selectbox("Select Coin", coins)
    tf = st.selectbox("Timeframe", ["15m", "1h", "4h", "1d"])

# ================== GET DATA FUNCTION (Fixed) ==================
@st.cache_data(ttl=15)
def get_data(symbol, timeframe, limit=250):
    # Primary: Binance + Bybit
    for ex in ["binance", "bybit"]:
        try:
            exchange = getattr(__import__('ccxt'), ex)({'enableRateLimit': True})
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            return df
        except:
            continue
    # Fallback CoinGecko
    try:
        coin_id = symbol.lower().replace("/usdt", "")
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/ohlc?vs_currency=usd&days=1"
        resp = requests.get(url, timeout=12)
        if resp.status_code == 200:
            data = resp.json()
            df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close'])
            df['volume'] = 0
            return df
    except:
        pass
    return None

if st.button("🚀 FULL QUANTUM + MACRO ANALYSIS", type="primary", use_container_width=True):
    with st.spinner("Satellite + Global Macro Data Fetching..."):
        df = get_data(symbol, tf)
        
        if df is not None and not df.empty:
            macro = get_macro_context(symbol.split('/')[0])
            signal = get_quantum_decision(df, symbol)
            
            col1, col2 = st.columns([1, 1])
            with col1:
                st.metric("Current Price", f"${signal['price']:,}")
            with col2:
                color = "#00ff9d" if "BUY" in signal['decision'] else "#ff4444"
                st.markdown(f"<div class='big-signal' style='background:{color}; color:black;'>{signal['decision']}</div>", unsafe_allow_html=True)
            
            st.markdown(f"<div class='alert-box'><b>🌍 Macro Situation:</b><br>{macro[:400]}...</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='alert-box'><b>⚡ Early Alert (Next 1-3 Hours):</b><br>{signal['early_alert']}</div>", unsafe_allow_html=True)
            
            if st.button("🔊 Voice Mein Suno", use_container_width=True):
                text = f"{symbol} abhi {signal['decision']} hai. {signal['early_alert']}"
                filename = speak_urdu(text)
                if filename:
                    st.audio(filename, format='audio/mp3')
        else:
            st.error("Data nahi aa raha. Thodi der baad try karo.")

st.caption("V9.4 • Strong Macro + Satellite + Fixed Background")
