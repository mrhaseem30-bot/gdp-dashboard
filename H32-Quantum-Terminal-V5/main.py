import streamlit as st
import pandas as pd
import requests
from macro_sentinel import get_macro_context
from smc_engine import get_quantum_decision
from ai_analyst import get_ai_verdict_with_timeframe
from tts_urdu import speak_urdu

st.set_page_config(page_title="H32 Quantum V9.5", layout="wide")

st.markdown("""
<style>
    .stApp { background: #05070f !important; color: #e0e0e0; }
    .big-signal { padding: 35px; border-radius: 22px; text-align: center; font-size: 2.6rem; font-weight: bold; margin: 20px 0; }
    .alert-box { background: #0f1629; padding: 22px; border-radius: 16px; border-left: 7px solid #00ff9d; margin: 15px 0; }
</style>
""", unsafe_allow_html=True)

st.title("📊 H32 QUANTUM TRADING TERMINAL V9.5")
st.caption("Satellite + Macro + Global Intelligence")

with st.sidebar:
    st.header("📍 Watchlist")
    coins = ["BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT", "XRP/USDT", "AVAX/USDT", "SUI/USDT"]
    symbol = st.selectbox("Select Coin", coins)
    tf = st.selectbox("Timeframe", ["15m", "1h", "4h", "1d"])

# ================== STRONG DATA FETCH ==================
@st.cache_data(ttl=10)
def get_data(symbol, timeframe, limit=150):
    # CoinGecko Fallback (sabse reliable yahan)
    try:
        coin_id = symbol.lower().replace("/usdt", "")
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/ohlc?vs_currency=usd&days=2"
        resp = requests.get(url, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close'])
            df['volume'] = 0
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            return df
    except:
        pass
    
    st.error("Data source busy hai. 10-15 seconds baad dubara try karo.")
    return None

if st.button("🚀 FULL QUANTUM + MACRO ANALYSIS", type="primary", use_container_width=True):
    with st.spinner("Satellite Data + Macro Analysis chal raha hai..."):
        df = get_data(symbol, tf)
        
        if df is not None and not df.empty:
            macro = get_macro_context(symbol.split('/')[0])
            signal = get_quantum_decision(df, symbol)
            
            col1, col2 = st.columns([1,1])
            with col1:
                st.metric("Current Price", f"${signal['price']:,}")
            with col2:
                color = "#00ff9d" if "BUY" in signal['decision'] else "#ff4444"
                st.markdown(f"<div class='big-signal' style='background:{color}; color:black;'>{signal['decision']}</div>", unsafe_allow_html=True)
            
            st.markdown(f"<div class='alert-box'><b>🌍 Macro Situation:</b><br>{macro[:500]}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='alert-box'><b>⚡ Early Alert:</b><br>{signal['early_alert']}</div>", unsafe_allow_html=True)
            
            if st.button("🔊 Voice Mein Suno", use_container_width=True):
                text = f"{symbol} abhi {signal['decision']} hai. {signal['early_alert']}"
                filename = speak_urdu(text)
                if filename:
                    st.audio(filename, format='audio/mp3')
        else:
            st.warning("Data abhi nahi aa raha. 15 seconds wait karke button dubara dabao.")

st.caption("V9.5 • CoinGecko Strong Fallback + Fixed")
