import streamlit as st
import pandas as pd
import ccxt
import requests
from macro_sentinel import get_macro_context
from smc_engine import get_quantum_decision
from ai_analyst import get_ai_verdict_with_timeframe
from tts_urdu import speak_urdu

st.set_page_config(page_title="H32 Quantum V9.0", layout="wide", page_icon="📊")

# Binance Style Background + UI
st.markdown("""
<style>
    .stApp { background: #0f0f1a; color: #ffffff; }
    .coin-row { padding: 12px; border-radius: 8px; background: #1a1a2e; margin: 4px 0; }
    .positive { color: #00ff9d; font-weight: bold; }
    .negative { color: #ff4444; font-weight: bold; }
    .big-signal { padding: 25px; border-radius: 15px; text-align: center; font-size: 2.2rem; font-weight: bold; }
    .alert-box { background: #1f2a44; padding: 15px; border-radius: 12px; border-left: 5px solid #00ff9d; }
</style>
""", unsafe_allow_html=True)

st.title("📊 H32 QUANTUM TRADING TERMINAL V9.0")
st.caption("Binance Style • Early Warning • Liquidation Engine")

with st.sidebar:
    st.header("⚙️ Settings")
    tf = st.selectbox("Timeframe", ["15m", "1h", "4h", "1d"])
    st.markdown("---")
    if st.button("🔍 SCAN ALL COINS", type="primary", use_container_width=True):
        scan_all_coins()

coins = ["BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT", "XRP/USDT", "ADA/USDT", 
         "AVAX/USDT", "SUI/USDT", "DOGE/USDT", "LINK/USDT", "DOT/USDT", "UNI/USDT", 
         "LTC/USDT", "ONDO/USDT", "ZEC/USDT"]

@st.cache_data(ttl=15)
def get_data(symbol, timeframe, limit=200):
    # ... same as before (copy from previous version)
    sources = ["binance", "bybit", "kraken"]
    for source in sources:
        try:
            exchange = getattr(ccxt, source)({'enableRateLimit': True})
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            return df
        except:
            continue
    return None

def scan_all_coins():
    with st.spinner("Scanning Market..."):
        results = []
        for coin in coins:
            df = get_data(coin, tf)
            if df is not None:
                signal = get_quantum_decision(df, coin)
                results.append(signal)
        
        st.subheader("🚀 MARKET SCANNER")
        for sig in sorted(results, key=lambda x: x['score'], reverse=True):
            change_color = "positive" if sig['score'] > 60 else "negative"
            st.markdown(f"""
            <div class="coin-row">
                <b>{sig['coin']}</b> — 
                <span class="{change_color}">{sig['decision']}</span> ({sig['score']}%)<br>
                Price: <b>\( {sig['price']}</b> | Support: <b> \){sig['support']}</b><br>
                <small>{sig['early_alert']}</small>
            </div>
            """, unsafe_allow_html=True)

# ================= SINGLE COIN ANALYSIS =================
if st.button("🚀 ANALYZE SELECTED COIN", type="primary"):
    df = get_data(symbol, tf)
    if df is not None:
        signal = get_quantum_decision(df, symbol)
        
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            st.metric("Price", f"${signal['price']}")
        with col2:
            color = "#00ff9d" if "BUY" in signal['decision'] else "#ff4444"
            st.markdown(f"<div class='big-signal' style='background:{color}; color:black;'>{signal['decision']}</div>", unsafe_allow_html=True)
        
        st.markdown(f"<div class='alert-box'><b>Early Alert (1-3 Hours):</b> {signal['early_alert']}</div>", unsafe_allow_html=True)
        
        st.write("**Support:**", signal['support'], "**Resistance:**", signal['resistance'])
        
        if st.button("🔊 Voice Alert Suno", use_container_width=True):
            text = f"{symbol} {signal['decision']}. {signal['early_alert']}"
            try:
                filename = speak_urdu(text)
                st.audio(filename, format='audio/mp3')
            except:
                st.error("Voice issue, baad mein try karo")

st.caption("V9.0 • Binance Style UI • Liquidation + Early Warning")
