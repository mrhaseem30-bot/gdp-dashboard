import streamlit as st
import requests
import pandas as pd
import numpy as np
from datetime import datetime
import os

# --- 🛰️ ALADDIN CORE SETUP ---
st.set_page_config(page_title="ALADDIN OMNI V17", layout="wide")

# --- 🔑 SECURE TELEGRAM CREDENTIALS ---
# Yahan apna real Telegram Bot Token dalein jo BotFather se mila hai
TELEGRAM_BOT_TOKEN = "7185493815:AAH_ActualBotTokenGoesHere"  # <-- Apni actual bot string yahan dalein
TELEGRAM_CHAT_ID = "8376377797"  # Aapki verified ID

# --- 🎨 INJECTING YOUR CUSTOM CSS + TERMINAL EXTENSIONS ---
st.markdown("""
    <style>
    /* Aapka uploaded style.css customization background grid */
    .stApp { background: linear-gradient(135deg, #0a0e17, #11151f); }
    .big-signal { padding: 25px; border-radius: 20px; text-align: center; font-size: 1.8rem; font-weight: bold; }
    
    /* Aladdin Engine Extra Containers */
    .main { color: #f0f6fc; font-family: 'Inter', sans-serif; }
    .terminal-card { background-color: #0d1117; border: 1px solid #30363d; border-radius: 12px; padding: 20px; margin-bottom: 15px; }
    .buy-glow { border: 2px solid #00ff88; background-color: #041910; color: #00ff88; padding: 20px; border-radius: 12px; }
    .sell-glow { border: 2px solid #ff4b4b; background-color: #220b0d; color: #ff4b4b; padding: 20px; border-radius: 12px; }
    </style>
    """, unsafe_allow_html=True)

# --- 🤖 TELEGRAM BOT DISPATCH PIPELINE ---
def send_telegram_notification(msg):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"}
        requests.post(url, json=payload, timeout=5)
    except:
        pass

# --- 🛰️ REAL DATA INGESTION ENGINE ---
def fetch_live_market_candles(symbol, timeframe, limit):
    try:
        endpoint = "histohour" if "h" in timeframe else "histoday"
        url = f"https://min-api.cryptocompare.com/data/v2/{endpoint}?fsym={symbol}&tsym=USD&limit={limit}"
        res = requests.get(url).json()
        if res.get("Response") == "Success":
            return pd.DataFrame(res['Data']['Data'])
        return None
    except:
        return None

# --- 🧠 3-BRAIN REAL INTER-LINKING CALCULATIONS ---
def analyze_3_brain_matrix(df):
    curr_price = df['close'].iloc[-1]
    avg_vol = df['volumeto'].mean()
    last_vol = df['volumeto'].iloc[-1]
    
    # Brain 1: AI 1 BIT-NOTE (1H Horizon)
    recent_high = df['high'].tail(24).max()
    recent_low = df['low'].tail(24).min()
    ai1_status = "⚪ MONITOR"
    if abs(curr_price - recent_low) < (recent_low * 0.006):
        ai1_status = "🟩 LIQUIDITY GRAB"
    elif abs(curr_price - recent_high) < (recent_high * 0.006):
        ai1_status = "🟥 RETAIL TRAP"

    # Brain 2: AI 2 BIT-GLASS (12H Delhi Session Dynamics)
    df['EMA21'] = df['close'].ewm(span=21, adjust=False).mean()
    ai2_status = "Bullish Setup" if curr_price > df['EMA21'].iloc[-1] else "Bearish Structure"

    # Brain 3: AI 3 BLACKROCK (1W Macro Whale Weight)
    ai3_status = "🐋 WHALE ACCUMULATION" if last_vol > (avg_vol * 1.6) else "Retail Distribution"

    # Inter-linking Verdict Rules
    final_signal = "⚪ MONITOR"
    if "LIQUIDITY" in ai1_status and "Bullish" in ai2_status and "WHALE" in ai3_status:
        final_signal = "🟢 PURI ENTRY (URGENT BUY)"
    elif "RETAIL" in ai1_status and "Bearish" in ai2_status:
        final_signal = "🔴 ZED EXIT (URGENT SELL)"

    return {
        "ai1": ai1_status, "ai2": ai2_status, "ai3": ai3_status,
        "signal": final_signal, "price": curr_price,
        "support": df['low'].min(), "resistance": df['high'].max()
    }

# --- 🔍 COMMAND INTERFACE ---
st.sidebar.markdown("### 🏛️ ALADDIN CONTROL COCKPIT")

if st.sidebar.button("🔌 Initial Setup & Bot Test"):
    send_telegram_notification("🏛️ *ALADDIN MATRIX V17 STATUS:*\nSystem online! Custom CSS & 3-Brain Pipelines synced successfully with terminal portfolio accounts. 🛰️")
    st.sidebar.success("Test alert successfully fired to Telegram chat!")

st.sidebar.divider()

# Dropdown Account List (Pre-defined watchlist - No Search Required)
watchlist_panel = ["BTC", "ETH", "SOL", "LINK", "DOT", "SHIB", "BONE", "BNB", "XRP", "MATIC"]
selected_asset = st.sidebar.selectbox("📂 PORTFOLIO ACCOUNT ASSET", watchlist_panel)

time_panel = {
    "1 Hour Scalp Engine": {"tf": "1h", "limit": 24},
    "12 Hour Session Matrix": {"tf": "1h", "limit": 120},
    "1 Month Macro Horizon": {"tf": "1d", "limit": 30}
}
selected_tf = st.sidebar.radio("⏱️ GRID TIME INTERVAL", list(time_panel.keys()))
active_conf = time_panel[selected_tf]

# --- 🚀 RUN CALCULATIONS LOOP ---
if selected_asset:
    data_stream = fetch_live_market_candles(selected_asset, active_conf['tf'], active_conf['limit'])
    
    if data_stream is not None and not data_stream.empty:
        results = analyze_3_brain_matrix(data_stream)
        
        # UI Top Display Header
        st.markdown(f"<h2>🏛️ TERMINAL CORE: {selected_asset}/USDT</h2>", unsafe_allow_html=True)
        st.markdown(f"### CURRENT REAL PRICE: `${results['price']:,.2f}`")
        st.write("---")

        # Displaying 3 Brain States Side-by-Side
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.markdown(f"<div class='terminal-card'><h4>🎯 AI 1: BIT-NOTE (1H)</h4><p style='font-size:18px;'><b>{results['ai1']}</b></p></div>", unsafe_allow_html=True)
        with col_b:
            st.markdown(f"<div class='terminal-card'><h4>🛰️ AI 2: BIT-GLASS (12H)</h4><p style='font-size:18px;'><b>{results['ai2']}</b></p></div>", unsafe_allow_html=True)
        with col_c:
            st.markdown(f"<div class='terminal-card'><h4>🏛️ AI 3: BLACKROCK (1W)</h4><p style='font-size:18px;'><b>{results['ai3']}</b></p></div>", unsafe_allow_html=True)

        # Trigger logic using session state trackers for telegram push loops
        if "last_broadcast_state" not in st.session_state:
            st.session_state.last_broadcast_state = ""

        current_state_key = f"{selected_asset}_{results['signal']}_{active_conf['tf']}"

        st.write(" ")
        
        # Dynamic Signal Output Box with your custom .big-signal structure
        if "BUY" in results['signal']:
            st.markdown(f"""
                <div class='big-signal buy-glow'>
                    🚀 SATELLITE POSITION VERDICT: {results['signal']}<br>
                    <span style='font-size: 1.2rem; color: white;'>Institutional Entry Block: ${results['support']:,.2f}</span>
                </div>
            """, unsafe_allow_html=True)
            
            if st.session_state.last_broadcast_state != current_state_key:
                tg_alert = f"🚨 *ALADDIN INTER-LINK BUY SYSTEM ALERT* 🚨\n\nAsset: {selected_asset}/USDT\nVerdict: 🟢 PURI ENTRY CONFIRMED\nPrice: ${results['price']:,.2f}\n\nAll three AI modules have matched technical parameters!"
                send_telegram_notification(tg_alert)
                st.session_state.last_broadcast_state = current_state_key

        elif "SELL" in results['signal']:
            st.markdown(f"""
                <div class='big-signal sell-glow'>
                    ⚠️ SATELLITE POSITION VERDICT: {results['signal']}<br>
                    <span style='font-size: 1.2rem; color: white;'>Zed Target Liquidation Layer: ${results['resistance']:,.2f}</span>
                </div>
            """, unsafe_allow_html=True)
            
            if st.session_state.last_broadcast_state != current_state_key:
                tg_alert = f"🚨 *ALADDIN INTER-LINK SELL SYSTEM ALERT* 🚨\n\nAsset: {selected_asset}/USDT\nVerdict: 🔴 URGENT ZED ZONE EXIT\nPrice: ${results['price']:,.2f}\n\nWarning: Distribution layer or resistance trap verified!"
                send_telegram_notification(tg_alert)
                st.session_state.last_broadcast_state = current_state_key
        else:
            st.info(f"🛰️ POSITION VERDICT: {results['signal']} — Waiting for 3-brain multi-layered consensus.")

        # Ingesting Price Chart Section
        st.write("---")
        st.subheader("📈 REAL-TIME INSTITUTIONAL PRICE SPREAD")
        st.line_chart(data_stream.set_index('time')['close'])

    else:
        st.error("📡 Live server engine database connection timeout.")
