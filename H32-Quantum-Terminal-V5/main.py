import streamlit as st
import pandas as pd
import requests
from macro_sentinel import get_macro_context
from smc_engine import get_quantum_decision
from ai_analyst import get_ai_verdict_with_timeframe
from tts_urdu import speak_urdu

st.set_page_config(page_title="H32 Quantum V9.7", layout="wide")

st.markdown("""
<style>
    .stApp { background: #05070f !important; color: #e0e0e0; }
    .big-signal { padding: 35px; border-radius: 22px; text-align: center; font-size: 2.6rem; font-weight: bold; margin: 20px 0; }
    .alert-box { background: #0f1629; padding: 22px; border-radius: 16px; border-left: 7px solid #00ff9d; margin: 15px 0; }
</style>
""", unsafe_allow_html=True)

st.title("📊 H32 QUANTUM TRADING TERMINAL V9.7")
st.caption("CoinMarketCap Live + Macro + Satellite")

CMC_API_KEY = "04d81f211e234e55a3e281b9ae23256f"

with st.sidebar:
    st.header("📍 Watchlist")
    coins = ["BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT", "XRP/USDT", "AVAX/USDT", "SUI/USDT"]
    symbol = st.selectbox("Select Coin", coins)
    tf = st.selectbox("Timeframe", ["15m", "1h", "4h", "1d"])

@st.cache_data(ttl=12)
def get_data(symbol, timeframe):
    coin = symbol.split('/')[0].lower()
    try:
        # CoinMarketCap Latest Data
        url = f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
        headers = {'X-CMC_PRO_API_KEY': CMC_API_KEY}
        params = {'symbol': coin.upper(), 'convert': 'USD'}
        resp = requests.get(url, headers=headers, params=params, timeout=15)
        
        if resp.status_code == 200:
            data = resp.json()
            price = data['data'][coin.upper()]['quote']['USD']['price']
            
            # Simple OHLC for analysis
            df = pd.DataFrame({
                'timestamp': pd.date_range(end=pd.Timestamp.now(), periods=100, freq='5T'),
                'open': [price * 0.995] * 100,
                'high': [price * 1.008] * 100,
                'low': [price * 0.99] * 100,
                'close': [price + (i-50)*price*0.0005 for i in range(100)],
                'volume': [5000000] * 100
            })
            return df
    except:
        pass
    
    # Fallback
    st.warning("CoinMarketCap busy → Test Mode")
    base = 80000 if "BTC" in symbol else 2500
    df = pd.DataFrame({
        'timestamp': pd.date_range(end=pd.Timestamp.now(), periods=80, freq='5T'),
        'open': [base] * 80,
        'high': [base + 400] * 80,
        'low': [base - 350] * 80,
        'close': [base + i*2 for i in range(80)],
        'volume': [2000000] * 80
    })
    return df

if st.button("🚀 FULL QUANTUM + MACRO ANALYSIS", type="primary", use_container_width=True):
    with st.spinner("CoinMarketCap + Macro + Whale Analysis..."):
        df = get_data(symbol, tf)
        macro = get_macro_context(symbol.split('/')[0])
        signal = get_quantum_decision(df, symbol)
        
        col1, col2 = st.columns([1,1])
        with col1:
            st.metric("Current Price", f"${signal['price']:,}")
        with col2:
            color = "#00ff9d" if "BUY" in signal['decision'] else "#ff4444"
            st.markdown(f"<div class='big-signal' style='background:{color}; color:black;'>{signal['decision']}</div>", unsafe_allow_html=True)
        
        st.markdown(f"<div class='alert-box'><b>🌍 Macro + Global Situation:</b><br>{macro[:700]}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='alert-box'><b>⚡ Early Alert (1-3 Hours):</b><br>{signal['early_alert']}</div>", unsafe_allow_html=True)
        
        if st.button("🔊 Voice Mein Suno", use_container_width=True):
            text = f"{symbol} abhi {signal['decision']} signal hai. {signal['early_alert']}"
            filename = speak_urdu(text)
            if filename:
                st.audio(filename, format='audio/mp3')

st.caption("V9.7 • CoinMarketCap Live + Macro + Early Warning")
