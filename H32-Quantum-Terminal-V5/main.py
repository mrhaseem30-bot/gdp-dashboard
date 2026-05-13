import streamlit as st
import pandas as pd
import ccxt
import requests
from macro_sentinel import get_macro_context
from smc_engine import get_quantum_decision
from ai_analyst import get_ai_verdict_with_timeframe
from tts_urdu import speak_urdu

st.set_page_config(page_title="H32 Quantum V9.1", layout="wide", page_icon="📊")

st.markdown("""
<style>
    .stApp { background: #0a0a12; color: #ffffff; }
    .big-signal { padding: 28px; border-radius: 18px; text-align: center; font-size: 2.3rem; font-weight: bold; margin: 12px 0; }
    .alert-box { background: #1a2238; padding: 16px; border-radius: 12px; border-left: 5px solid #00ff9d; margin: 10px 0; }
    .coin-row { background: #161625; padding: 14px; border-radius: 10px; margin: 6px 0; }
</style>
""", unsafe_allow_html=True)

st.title("📊 H32 QUANTUM TRADING TERMINAL V9.1")
st.caption("Binance Style • Early Warning • Liquidation Engine")

with st.sidebar:
    st.header("⚙️ Controls")
    coins = ["BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT", "XRP/USDT",
             "ADA/USDT", "AVAX/USDT", "SUI/USDT", "DOGE/USDT", "LINK/USDT",
             "DOT/USDT", "UNI/USDT", "LTC/USDT", "ONDO/USDT", "ZEC/USDT"]
    
    symbol = st.selectbox("Select Coin", coins)
    tf = st.selectbox("Timeframe", ["15m", "1h", "4h", "1d"])

    st.markdown("---")
    if st.button("🔍 SCAN ALL COINS", type="primary", use_container_width=True):
        scan_all_coins()

# ================== GET DATA FUNCTION ==================
@st.cache_data(ttl=15)
def get_data(symbol, timeframe, limit=200):
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
    # Fallback CoinGecko
    try:
        coin_id = symbol.lower().replace("/usdt", "")
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/ohlc?vs_currency=usd&days=1"
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close'])
            df['volume'] = 0
            return df
    except:
        pass
    return None

# ================== SCANNER ==================
def scan_all_coins():
    with st.spinner("Scanning all coins..."):
        results = []
        for coin in coins:
            df = get_data(coin, tf)
            if df is not None and not df.empty:
                signal = get_quantum_decision(df, coin)
                results.append(signal)
        
        if results:
            st.subheader("🚀 MARKET SCANNER")
            for sig in sorted(results, key=lambda x: x['score'], reverse=True):
                st.markdown(f"""
                <div class="coin-row">
                    <b>{sig['coin']}</b> — {sig['decision']} ({sig['score']}%)<br>
                    Price: <b>${sig['price']}</b> | Support: ${sig['support']}
                </div>
                """, unsafe_allow_html=True)

# ================== SINGLE COIN ANALYSIS ==================
if st.button("🚀 ANALYZE SELECTED COIN", type="primary"):
    with st.spinner("Analyzing..."):
        df = get_data(symbol, tf)
        if df is not None:
            signal = get_quantum_decision(df, symbol)
            
            col1, col2 = st.columns([1, 1])
            with col1:
                st.metric("Current Price", f"${signal['price']}")
            with col2:
                color = "#00ff9d" if "BUY" in signal['decision'] else "#ff4444"
                st.markdown(f"<div class='big-signal' style='background:{color}; color:black;'>{signal['decision']}</div>", unsafe_allow_html=True)
            
            st.markdown(f"<div class='alert-box'><b>Early Alert:</b> {signal['early_alert']}</div>", unsafe_allow_html=True)
            st.write("**Support:**", signal['support'], " | **Resistance:**", signal['resistance'])
            
            if st.button("🔊 Voice Mein Suno", use_container_width=True):
                text = f"{symbol} {signal['decision']}. {signal['early_alert']}"
                filename = speak_urdu(text)
                st.audio(filename, format='audio/mp3')

st.caption("V9.1 • Fixed Version")
