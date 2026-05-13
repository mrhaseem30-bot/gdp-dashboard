import streamlit as st
import pandas as pd
import ccxt
import time
from macro_sentinel import get_macro_context
from smc_engine import detect_market_structure, get_key_levels, calculate_confluence
from ai_analyst import get_ai_verdict_with_timeframe

st.set_page_config(page_title="H32 Quantum Terminal V6.0", layout="wide", page_icon="⚡")

# Professional Dark Theme
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #0a0a0a, #1a1a2e, #16213e); color: #e0e0e0; }
    .big-signal { padding: 20px; border-radius: 15px; text-align: center; font-size: 2rem; font-weight: bold; margin: 10px 0; }
    .level-box { padding: 12px; border-radius: 10px; background: rgba(255,255,255,0.05); margin: 5px 0; }
</style>
""", unsafe_allow_html=True)

st.title("⚡ H32 QUANTUM TERMINAL V6.0")
st.caption("Satellite Real-Time • SMC + Liquidation Engine + AI")

with st.sidebar:
    st.header("📍 Watchlist")
    coins = ["BTC/USDT", "ETH/USDT", "SOL/USDT", "AVAX/USDT", "SUI/USDT"]
    symbol = st.selectbox("Select Coin", coins)
    tf = st.selectbox("Timeframe", ["5m", "15m", "1h", "4h", "1d"])

@st.cache_data(ttl=10)  # Fast refresh
def get_data(symbol, timeframe, limit=300):
    # ... (tumhara purana get_data function same rakh sakte ho, better fallback ke saath)

# FULL ANALYSIS BUTTON
if st.button("🚀 SATELLITE QUANTUM ANALYSIS", type="primary"):
    with st.spinner("Satellite data fetching + AI analyzing..."):
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
            
            # UI Display
            col1, col2 = st.columns([1, 1])
            with col1:
                st.metric(f"**{symbol}**", f"${price:,.4f}", delta=None)
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
                st.markdown(f"<div class='level-box level-down'>Long Liq<br><b>${levels['liq_long_zone']}</b></div>", unsafe_allow_html=True)
            with c4:
                st.markdown(f"<div class='level-box level-up'>Short Liq<br><b>${levels['liq_short_zone']}</b></div>", unsafe_allow_html=True)
            
            st.info(f"**Long Entry:** ${levels['long_entry']} | **SL:** ${levels['suggested_sl']}")
            
            st.markdown("### 🧠 AI Verdict (24h - 1 Week)")
            st.write(ai_verdict)
            
            # Risk Suggestion
            st.warning("**Risk Management:** Max 1-2% capital per trade | RR 1:2.5+")

st.caption("V6.0 • Real-time Levels + Liquidation Engine • Every 10s refresh")
