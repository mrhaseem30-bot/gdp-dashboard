import streamlit as st
import pandas as pd
import ccxt
import requests
from macro_sentinel import get_macro_context
from smc_engine import detect_market_structure, get_key_levels, calculate_confluence
from ai_analyst import get_ai_verdict_with_timeframe

st.set_page_config(page_title="H32 Quantum Terminal V6.0", layout="wide", page_icon="⚡")

# Professional Dark Theme
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #0a0a0a, #1a1a2e, #16213e); color: #e0e0e0; }
    .big-signal { padding: 25px; border-radius: 15px; text-align: center; font-size: 2rem; font-weight: bold; margin: 10px 0; }
    .level-box { padding: 15px; border-radius: 10px; background: rgba(255,255,255,0.08); margin: 8px 0; text-align: center; }
</style>
""", unsafe_allow_html=True)

st.title("⚡ H32 QUANTUM TERMINAL V6.0")
st.caption("Satellite Real-Time • SMC + Liquidation Engine")

with st.sidebar:
    st.header("📍 Watchlist")
    coins = ["BTC/USDT", "ETH/USDT", "SOL/USDT", "AVAX/USDT", "SUI/USDT"]
    symbol = st.selectbox("Select Coin", coins)
    tf = st.selectbox("Timeframe", ["15m", "1h", "4h", "1d"])

@st.cache_data(ttl=15)
def get_data(symbol, timeframe, limit=300):
    sources = ["binance", "bybit", "kraken", "coingecko"]
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
            continue
    return None

# ===================== MAIN ANALYSIS =====================
if st.button("🚀 SATELLITE QUANTUM ANALYSIS", type="primary"):
    with st.spinner("Fetching live data + AI analyzing..."):
        df = get_data(symbol, tf)
        
        if df is not None and not df.empty:
            price = float(df['close'].iloc[-1])
            macro = get_macro_context(symbol.split('/')[0])
            structure_data = detect_market_structure(df)
            levels = get_key_levels(df)
            score, reasons = calculate_confluence(df, price)
            
            ai_verdict = get_ai_verdict_with_timeframe(
                symbol, price, structure_data['structure'], score, reasons, macro
            )
            
            col1, col2 = st.columns([1, 1])
            with col1:
                st.metric(f"**{symbol}**", f"${price:,.4f}")
                st.progress(score / 100)
                st.success(f"Confluence: {score}%")
            
            with col2:
                color = "#00ff9d" if "BULL" in structure_data['structure'] else "#ff4444"
                st.markdown(f"<div class='big-signal' style='background:{color}; color:black;'>{structure_data['structure']}</div>", unsafe_allow_html=True)
            
            # Key Levels
            st.subheader("🔑 Key Levels & Liquidation Zones")
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.markdown(f"<div class='level-box'>Support<br><b>${levels['strong_support']}</b></div>", unsafe_allow_html=True)
            with c2:
                st.markdown(f"<div class='level-box'>Resistance<br><b>${levels['strong_resistance']}</b></div>", unsafe_allow_html=True)
            with c3:
                st.markdown(f"<div class='level-box' style='color:#ff6666'>Long Liq<br><b>${levels['liq_long_zone']}</b></div>", unsafe_allow_html=True)
            with c4:
                st.markdown(f"<div class='level-box' style='color:#66ff99'>Short Liq<br><b>${levels['liq_short_zone']}</b></div>", unsafe_allow_html=True)
            
            st.info(f"**Long Entry:** ${levels['long_entry']}   |   **Suggested SL:** ${levels['suggested_sl']}")
            st.markdown("### 🧠 AI Verdict")
            st.write(ai_verdict)
        else:
            st.error("Data fetch failed. Try again in 10 seconds.")

st.caption("V6.0 • Fixed Version • Every 15 seconds refresh")
