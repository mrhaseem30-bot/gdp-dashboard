import streamlit as st
import pandas as pd
import requests
from macro_sentinel import get_macro_context
from smc_engine import get_quantum_decision
from ai_analyst import get_ai_verdict_with_timeframe
from tts_urdu import speak_urdu

st.set_page_config(page_title="H32 Quantum V9.3", layout="wide")

st.markdown("""
<style>
    .stApp { background: #0a0a12 !important; color: #ffffff; }
    .big-signal { padding: 35px; border-radius: 20px; text-align: center; font-size: 2.6rem; font-weight: bold; margin: 20px 0; box-shadow: 0 0 30px rgba(0,255,150,0.5); }
    .alert-box { background: #1a2238; padding: 20px; border-radius: 15px; border-left: 6px solid #00ff9d; }
</style>
""", unsafe_allow_html=True)

st.title("📊 H32 QUANTUM TRADING TERMINAL V9.3")
st.caption("Satellite + Macro + Finance Intelligence")

with st.sidebar:
    coins = ["BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT", "XRP/USDT", "AVAX/USDT", "SUI/USDT"]
    symbol = st.selectbox("Coin", coins)
    tf = st.selectbox("Timeframe", ["15m", "1h", "4h"])

if st.button("🚀 FULL QUANTUM + MACRO ANALYSIS", type="primary", use_container_width=True):
    with st.spinner("Satellite + Global Macro Analyzing..."):
        df = get_data(symbol, tf)  # tumhara function
        if df is not None:
            macro_summary = get_macro_context(symbol.split('/')[0])
            signal = get_quantum_decision(df, symbol)
            
            col1, col2 = st.columns([1,1])
            with col1:
                st.metric("Current Price", f"${signal['price']:,}")
            with col2:
                color = "#00ff9d" if "BUY" in signal['decision'] else "#ff4444"
                st.markdown(f"<div class='big-signal' style='background:{color}; color:black;'>{signal['decision']}</div>", unsafe_allow_html=True)
            
            st.markdown(f"<div class='alert-box'><b>Macro Situation:</b><br>{macro_summary[:300]}...</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='alert-box'><b>Early Alert (1-3 Hours):</b><br>{signal['early_alert']}</div>", unsafe_allow_html=True)
            
            if st.button("🔊 Voice Suno (Urdu)"):
                text = f"{symbol} {signal['decision']}. Global situation tense hai. {signal['early_alert']}"
                filename = speak_urdu(text)
                st.audio(filename, format='audio/mp3')

st.caption("V9.3 • Macro + Satellite Integrated")
