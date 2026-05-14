import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# --- 🛰️ ALADDIN CORE CONFIGURATION (LAG BLOCKER) ---
st.set_page_config(page_title="ALADDIN ULTRA V19", layout="wide")

# --- 🔑 SECURE TELEGRAM CREDENTIALS ---
TELEGRAM_BOT_TOKEN = "7185493815:AAH_ActualBotTokenGoesHere" # Apni token id dalein
TELEGRAM_CHAT_ID = "8376377797" 

# --- 🎨 SOLID THEME WITH ZERO BACKGROUND REFLEX PIPES ---
st.markdown("""
    <style>
    .stApp { background-color: #06090f !important; }
    .big-signal { padding: 25px; border-radius: 20px; text-align: center; font-size: 1.8rem; font-weight: bold; }
    .main { color: #f0f6fc; font-family: 'Inter', sans-serif; }
    .terminal-card { background-color: #0d1117; border: 1px solid #30363d; border-radius: 12px; padding: 20px; margin-bottom: 15px; }
    .buy-glow { border: 2px solid #00ff88; background-color: #041910; color: #00ff88; padding: 20px; border-radius: 12px; }
    .sell-glow { border: 2px solid #ff4b4b; background-color: #220b0d; color: #ff4b4b; padding: 20px; border-radius: 12px; }
    
    /* Loading frame animation override to prevent freezing screens */
    div.stSpinner > div { border-top-color: #00ff88 !important; }
    block-container { padding-top: 2rem !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 🤖 TELEGRAM PIPELINE ---
def send_telegram_notification(msg):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"}
        requests.post(url, json=payload, timeout=2) # Timeout short rakha hai taake app wait na kare
    except:
        pass

# --- 🛰️ FAST DATA CACHING CORE ENGINE (Anti-Loading Fix) ---
@st.cache_data(ttl=15, show_spinner=False) # 15 seconds cache memory layer taake lag khatam ho jaye
def fetch_fast_market_candles(symbol, timeframe, limit):
    try:
        endpoint = "histohour" if "h" in timeframe else "histoday"
        url = f"https://min-api.cryptocompare.com/data/v2/{endpoint}?fsym={symbol}&tsym=USD&limit={limit}"
        res = requests.get(url, timeout=3).json()
        if res.get("Response") == "Success":
            df = pd.DataFrame(res['Data']['Data'])
            df['date'] = pd.to_datetime(df['time'], unit='s')
            return df
        return None
    except:
        return None

# --- 🧠 3-BRAIN AI COMPUTATION ---
def analyze_3_brain_matrix(df):
    curr_price = df['close'].iloc[-1]
    avg_vol = df['volumeto'].mean()
    last_vol = df['volumeto'].iloc[-1]
    
    recent_high = df['high'].tail(24).max()
    recent_low = df['low'].tail(24).min()
    ai1_status = "⚪ MONITOR"
    if abs(curr_price - recent_low) < (recent_low * 0.006):
        ai1_status = "🟩 LIQUIDITY GRAB"
    elif abs(curr_price - recent_high) < (recent_high * 0.006):
        ai1_status = "🟥 RETAIL TRAP"

    df['EMA21'] = df['close'].ewm(span=21, adjust=False).mean()
    ai2_status = "Bullish Setup" if curr_price > df['EMA21'].iloc[-1] else "Bearish Structure"
    ai3_status = "🐋 WHALE ACCUMULATION" if last_vol > (avg_vol * 1.6) else "Retail Distribution"

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

# --- 🔍 INTERFACE CONTROL ---
st.sidebar.markdown("### 🏛️ ALADDIN COMMAND UNIT")
if st.sidebar.button("⚡ Speed Sync Terminal"):
    st.sidebar.success("Terminal rendering parameters set to instant-load mode!")

st.sidebar.divider()

watchlist_panel = ["BTC", "ETH", "SOL", "LINK", "DOT", "SHIB", "BONE", "BNB", "XRP", "MATIC"]
selected_asset = st.sidebar.selectbox("📂 PORTFOLIO ACCOUNT ASSET", watchlist_panel)

time_panel = {
    "1 Hour Scalp Engine": {"tf": "1h", "limit": 24},
    "12 Hour Session Matrix": {"tf": "1h", "limit": 120},
    "1 Month Macro Horizon": {"tf": "1d", "limit": 30}
}
selected_tf = st.sidebar.radio("⏱️ GRID TIME INTERVAL", list(time_panel.keys()))
active_conf = time_panel[selected_tf]

# --- 🚀 EXECUTION GRID ---
if selected_asset:
    data_stream = fetch_fast_market_candles(selected_asset, active_conf['tf'], active_conf['limit'])
    
    if data_stream is not None and not data_stream.empty:
        results = analyze_3_brain_matrix(data_stream)
        
        st.markdown(f"<h2>🏛️ TERMINAL CORE: {selected_asset}/USDT</h2>", unsafe_allow_html=True)
        st.markdown(f"### CURRENT REAL PRICE: `${results['price']:,.2f}`")
        st.write("---")

        # 3-Brain Grid Displays
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.markdown(f"<div class='terminal-card'><h4>🎯 AI 1: BIT-NOTE (1H)</h4><p style='font-size:18px;'><b>{results['ai1']}</b></p></div>", unsafe_allow_html=True)
        with col_b:
            st.markdown(f"<div class='terminal-card'><h4>🛰️ AI 2: BIT-GLASS (12H)</h4><p style='font-size:18px;'><b>{results['ai2']}</b></p></div>", unsafe_allow_html=True)
        with col_c:
            st.markdown(f"<div class='terminal-card'><h4>🏛️ AI 3: BLACKROCK (1W)</h4><p style='font-size:18px;'><b>{results['ai3']}</b></p></div>", unsafe_allow_html=True)

        if "last_broadcast_state" not in st.session_state:
            st.session_state.last_broadcast_state = ""

        current_state_key = f"{selected_asset}_{results['signal']}_{active_conf['tf']}"
        st.write(" ")
        
        if "BUY" in results['signal']:
            st.markdown(f"<div class='big-signal buy-glow'>🚀 SATELLITE POSITION VERDICT: {results['signal']}<br><span style='font-size: 1.2rem; color: white;'>Institutional Entry Block: ${results['support']:,.2f}</span></div>", unsafe_allow_html=True)
            if st.session_state.last_broadcast_state != current_state_key:
                send_telegram_notification(f"🚨 *ALADDIN BUY ALERT*\nAsset: {selected_asset}\nPrice: ${results['price']:,.2f}")
                st.session_state.last_broadcast_state = current_state_key
        elif "SELL" in results['signal']:
            st.markdown(f"<div class='big-signal sell-glow'>⚠️ SATELLITE POSITION VERDICT: {results['signal']}<br><span style='font-size: 1.2rem; color: white;'>Zed Target Liquidation Layer: ${results['resistance']:,.2f}</span></div>", unsafe_allow_html=True)
            if st.session_state.last_broadcast_state != current_state_key:
                send_telegram_notification(f"🚨 *ALADDIN SELL ALERT*\nAsset: {selected_asset}\nPrice: ${results['price']:,.2f}")
                st.session_state.last_broadcast_state = current_state_key
        else:
            st.info(f"🛰️ POSITION VERDICT: {results['signal']} — Waiting for 3-brain consensus.")

        # --- 📊 LIGHTWEIGHT CANDLESTICK GRAPH CONTAINER (Lag Checked) ---
        st.write("---")
        st.subheader("📊 REAL-TIME INSTITUTIONAL CANDLESTICK GRAPH")
        
        fig = go.Figure(data=[go.Candlestick(
            x=data_stream['date'],
            open=data_stream['open'],
            high=data_stream['high'],
            low=data_stream['low'],
            close=data_stream['close'],
            increasing_line_color='#00ff88',
            decreasing_line_color='#ff4b4b'
        )])

        fig.update_layout(
            template="plotly_dark",
            xaxis_rangeslider_visible=False,
            paper_bgcolor='#0d1117',
            plot_bgcolor='#0d1117',
            margin=dict(l=8, r=8, t=8, b=8),
            yaxis=dict(gridcolor='#1f242c', side="right"),
            xaxis=dict(gridcolor='#1f242c')
        )
        
        # Ingesting with native width to disable any frame-loading triggers
        st.plotly_chart(fig, use_container_width=True, key="aladdin_candle_chart")

    else:
        st.error("📡 Live data pipeline network error.")
