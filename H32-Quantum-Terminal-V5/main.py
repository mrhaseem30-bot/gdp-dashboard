import streamlit as st
import pandas as pd
import requests
from macro_sentinel import get_macro_context
from smc_engine import get_intelligent_signal
from ai_analyst import get_ai_verdict_with_timeframe
from tts_urdu import speak_urdu
import time

st.set_page_config(page_title="H32 Quantum Intelligence V7.0", layout="wide", page_icon="🛰️")

st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #0a0a0a, #1a1a2e, #0f1626); color: #00ff9d; }
    .big-signal { padding: 25px; border-radius: 20px; text-align: center; font-size: 2.2rem; font-weight: bold; }
    .alert-box { padding: 15px; border-radius: 12px; background: rgba(255, 100, 100, 0.2); border: 1px solid #ff6666; }
</style>
""", unsafe_allow_html=True)

st.title("🛰️ H32 QUANTUM INTELLIGENCE V7.0")
st.caption("Self-Thinking AI Trader • Early Warning • Whale Flow • 2-Hour Alerts")

with st.sidebar:
    coins = ["BTC/USDT", "ETH/USDT", "SOL/USDT", "AVAX/USDT", "SUI/USDT"]
    symbol = st.selectbox("Coin Select", coins)
    tf = st.selectbox("Timeframe", ["15m", "1h", "4h"])

# Data Fetch (existing function use karo)

if st.button("🚀 LAUNCH QUANTUM ANALYSIS", type="primary"):
    with st.spinner("Satellite + Whale Data Analyzing..."):
        df = get_data(symbol, tf)  # tumhara purana function
        
        if df is not None:
            signal = get_intelligent_signal(df, symbol)
            macro = get_macro_context(symbol.split('/')[0])
            ai_verdict = get_ai_verdict_with_timeframe(symbol, signal['price'], 
                                                       signal['action'], signal['score'], signal['reasons'], macro)
            
            # Display
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Current Price", f"${signal['price']:,}")
                st.progress(signal['score']/100)
            
            with col2:
                color = "#00ff9d" if "BUY" in signal['action'] else "#ff4444"
                st.markdown(f"<div class='big-signal' style='background:{color}; color:black;'>{signal['action']}</div>", unsafe_allow_html=True)
            
            st.subheader("🛎️ Early Warning (Next 1-3 Hours)")
            st.info(signal['early_alert'])
            
            st.subheader("🔑 Levels")
            st.write(f"Support: **\( {signal['support']}** | Resistance: ** \){signal['resistance']}**")
            st.write(f"Long Liq Zone: **\( {signal['long_liq']}** | Short Liq: ** \){signal['short_liq']}**")
            
            if st.button("🔊 Voice Alert Suno"):
                text = f"{symbol} mein {signal['action']} signal hai. {signal['early_alert']}"
                file = speak_urdu(text)
                st.audio(file, format='audio/mp3')
            
            st.markdown("### 🧠 Full AI Verdict")
            st.write(ai_verdict)

st.caption("V7.0 • Self Decision AI • Early Alerts System")
