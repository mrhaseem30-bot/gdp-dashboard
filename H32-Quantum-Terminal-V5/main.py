import streamlit as st
import pandas as pd
import ccxt
import requests
from macro_sentinel import get_macro_context
from smc_engine import get_quantum_decision
from ai_analyst import get_ai_verdict_with_timeframe
from tts_urdu import speak_urdu

st.set_page_config(page_title="H32 Quantum V8.0", layout="wide", page_icon="🛰️")

st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #0a0a0a, #1a1a2e, #16213e); color: #00ff9d; }
    .big-signal { padding: 25px; border-radius: 20px; text-align: center; font-size: 2.3rem; font-weight: bold; margin: 10px 0; }
    .alert { padding: 15px; border-radius: 12px; background: rgba(0, 255, 150, 0.15); border: 1px solid #00ff9d; }
</style>
""", unsafe_allow_html=True)

st.title("🛰️ H32 QUANTUM INTELLIGENCE V8.0")
st.caption("Self-Improving AI Trader • Multi Coin Scanner • Early Alerts")

# Watchlist
with st.sidebar:
    st.header("📍 Watchlist")
    coins = ["BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT", "XRP/USDT",
             "ADA/USDT", "AVAX/USDT", "SUI/USDT", "DOGE/USDT", "LINK/USDT",
             "DOT/USDT", "UNI/USDT", "LTC/USDT", "ONDO/USDT", "ZEC/USDT"]
    
    symbol = st.selectbox("Single Coin", coins)
    tf = st.selectbox("Timeframe", ["15m", "1h", "4h"])

    st.markdown("---")
    if st.button("🔍 SCAN ALL WATCHLIST", type="primary", use_container_width=True):
        scan_all_coins()

@st.cache_data(ttl=20)
def get_data(symbol, timeframe, limit=250):
    sources = ["binance", "bybit", "kraken", "coingecko"]
    for source in sources:
        try:
            if source == "coingecko":
                coin_id = symbol.lower().replace("/usdt", "")
                url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/ohlc?vs_currency=usd&days=1"
                resp = requests.get(url, timeout=10)
                if resp.status_code == 200:
                    data = resp.json()
                    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close'])
                    df['volume'] = 0
                    return df
            else:
                exchange = getattr(ccxt, source)({'enableRateLimit': True})
                ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
                df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
                df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
                return df
        except:
            continue
    return None

def scan_all_coins():
    with st.spinner("🌐 Scanning All Coins in Satellite Mode..."):
        results = []
        progress = st.progress(0)
        
        for i, coin in enumerate(coins):
            df = get_data(coin, tf)
            if df is not None and not df.empty:
                signal = get_quantum_decision(df, coin)
                results.append(signal)
            progress.progress((i + 1) / len(coins))
        
        progress.empty()
        
        if results:
            st.success(f"✅ {len(results)} Coins Analyzed")
            st.subheader("🚀 TOP OPPORTUNITIES")
            
            top = sorted(results, key=lambda x: x['score'], reverse=True)[:7]
            for sig in top:
                color = "#00ff9d" if "BUY" in sig['decision'] else "#ff6666"
                st.markdown(f"<div class='alert'><b>{sig['coin']}</b> → <span style='color:{color}'>{sig['decision']}</span> ({sig['score']}%)</div>", unsafe_allow_html=True)
                st.caption(sig['early_alert'])
                st.write(f"Price: **\( {sig['price']}** | Support: ** \){sig['support']}**")
                st.divider()

# Single Coin Analysis
if st.button("🚀 SINGLE COIN QUANTUM ANALYSIS", type="primary"):
    with st.spinner("Analyzing..."):
        df = get_data(symbol, tf)
        if df is not None:
            signal = get_quantum_decision(df, symbol)
            macro = get_macro_context(symbol.split('/')[0])
            ai_verdict = get_ai_verdict_with_timeframe(symbol, signal['price'], signal['decision'], signal['score'], signal['reasons'], macro)
            
            col1, col2 = st.columns([1,1])
            with col1:
                st.metric("Current Price", f"${signal['price']:,}")
            with col2:
                color = "#00ff9d" if "BUY" in signal['decision'] else "#ff4444"
                st.markdown(f"<div class='big-signal' style='background:{color};color:black;'>{signal['decision']}</div>", unsafe_allow_html=True)
            
            st.info(f"**Early Alert:** {signal['early_alert']}")
            st.write("**Reasons:**", " • ".join(signal['reasons']))
            
            if st.button("🔊 Voice Mein Suno"):
                text = f"{symbol} {signal['decision']} hai. {signal['early_alert']}"
                filename = speak_urdu(text)
                st.audio(filename, format="audio/mp3")

st.caption("H32 Quantum V8.0 • Self Improving System")
