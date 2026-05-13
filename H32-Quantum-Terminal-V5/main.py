import streamlit as st
import pandas as pd
import ccxt
import requests
from macro_sentinel import get_macro_context
from smc_engine import get_quantum_decision
from ai_analyst import get_ai_verdict_with_timeframe
from tts_urdu import speak_urdu

st.set_page_config(page_title="H32 Quantum V9.2", layout="wide", page_icon="📊")

# Professional Binance Style + Custom CSS
st.markdown("""
<style>
    .stApp { background: #0a0a12 !important; color: #ffffff; }
    .big-signal { padding: 30px; border-radius: 18px; text-align: center; font-size: 2.4rem; font-weight: bold; margin: 15px 0; box-shadow: 0 0 25px rgba(0,255,150,0.4); }
    .alert-box { background: #1a2238; padding: 18px; border-radius: 12px; border-left: 6px solid #00ff9d; margin: 12px 0; }
    .coin-row { background: #161625; padding: 16px; border-radius: 10px; margin: 8px 0; border: 1px solid #2a2a40; }
</style>
""", unsafe_allow_html=True)

# Custom CSS File Include
try:
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except:
    pass

st.title("📊 H32 QUANTUM TRADING TERMINAL V9.2")
st.caption("Professional Binance Style • Early Warning • Liquidation")

with st.sidebar:
    st.header("⚙️ Controls")
    coins = ["BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT", "XRP/USDT", "ADA/USDT", "AVAX/USDT", "SUI/USDT", "DOGE/USDT"]
    symbol = st.selectbox("Select Coin", coins)
    tf = st.selectbox("Timeframe", ["15m", "1h", "4h"])

    if st.button("🔍 SCAN ALL COINS", type="primary", use_container_width=True):
        scan_all_coins()

@st.cache_data(ttl=15)
def get_data(symbol, timeframe, limit=200):
    sources = ["binance", "bybit"]
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
    with st.spinner("Market Scan chal raha hai..."):
        results = []
        for coin in coins:
            df = get_data(coin, tf)
            if df is not None:
                signal = get_quantum_decision(df, coin)
                results.append(signal)
        
        st.subheader("🚀 TOP MARKET SIGNALS")
        for sig in sorted(results, key=lambda x: x['score'], reverse=True):
            st.markdown(f"""
            <div class="coin-row">
                <b>{sig['coin']}</b> — <span style="color:#00ff9d">{sig['decision']}</span> ({sig['score']}%)<br>
                Price: <b>${sig['price']}</b> | Support: ${sig['support']}
            </div>
            """, unsafe_allow_html=True)

if st.button("🚀 ANALYZE SELECTED COIN", type="primary"):
    with st.spinner("Quantum Analysis chal raha hai..."):
        df = get_data(symbol, tf)
        if df is not None:
            signal = get_quantum_decision(df, symbol)
            macro = get_macro_context(symbol.split('/')[0])
            
            col1, col2 = st.columns([1,1])
            with col1:
                st.metric("Current Price", f"${signal['price']:,}")
            with col2:
                color = "#00ff9d" if "BUY" in signal['decision'] else "#ff4444"
                st.markdown(f"<div class='big-signal' style='background:{color}; color:black;'>{signal['decision']}</div>", unsafe_allow_html=True)
            
            st.markdown(f"<div class='alert-box'><b>Early Alert (1-3 Hours):</b><br>{signal['early_alert']}</div>", unsafe_allow_html=True)
            
            if st.button("🔊 Voice Mein Suno", use_container_width=True):
                text = f"{symbol} abhi {signal['decision']} hai. {signal['early_alert']}"
                filename = speak_urdu(text)
                if filename:
                    st.audio(filename, format='audio/mp3')

st.caption("V9.2 • Fixed Background + Voice + Scanner")
