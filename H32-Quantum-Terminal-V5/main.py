import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# --- 🛰️ ALADDIN SATELLITE CORE CONFIG ---
st.set_page_config(page_title="ALADDIN SATELLITE V21", layout="wide")

# --- 🔑 CREDENTIALS ---
TELEGRAM_BOT_TOKEN = "7185493815:AAH_ActualBotTokenGoesHere"  # Apna Bot Token lagayein
TELEGRAM_CHAT_ID = "8376377797" 

# --- 🎨 TRADING INTERFACE (SOLID DEEP BLACK) ---
st.markdown("""
    <style>
    .stApp { background-color: #06090f !important; }
    .main { color: #f0f6fc; font-family: 'Inter', sans-serif; }
    .terminal-card { background-color: #0d1117; border: 1px solid #30363d; border-radius: 12px; padding: 20px; margin-bottom: 15px; }
    
    /* Institutional Alert & Target Boxes */
    .signal-box { padding: 25px; border-radius: 15px; text-align: center; font-size: 1.5rem; font-weight: bold; margin-bottom: 20px; }
    .pure-buy { border: 2px solid #00ff88; background-color: #041910; color: #00ff88; box-shadow: 0 0 15px rgba(0,255,136,0.2); }
    .pure-sell { border: 2px solid #ff4b4b; background-color: #220b0d; color: #ff4b4b; box-shadow: 0 0 15px rgba(255,75,75,0.2); }
    .pure-monitor { border: 1px solid #30363d; background-color: #0d1117; color: #8b949e; }
    </style>
    """, unsafe_allow_html=True)

def send_telegram_message(msg):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"}
        requests.post(url, json=payload, timeout=3)
    except:
        pass

# --- 📡 SATELLITE REAL-TIME STREAM PIPELINE ---
@st.cache_data(ttl=10, show_spinner=False)
def fetch_satellite_data(symbol, timeframe, limit=100):
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

# --- 🧠 3-BRAIN SMC LIQUIDITY SEARCH ENGINE ---
def execute_aladdin_research(df):
    curr_price = float(df['close'].iloc[-1])
    
    # SMC Engine: Detect Liquidity Grabs (Last 30 Candles Range)
    recent_high = float(df['high'].tail(30).max())
    recent_low = float(df['low'].tail(30).min())
    current_high = float(df['high'].iloc[-1])
    current_low = float(df['low'].iloc[-1])
    
    # Indicators Layer
    df['EMA21'] = df['close'].ewm(span=21, adjust=False).mean()
    ema21 = df['EMA21'].iloc[-1]
    
    # Volume Whale Filter
    avg_vol = df['volumeto'].mean()
    last_vol = df['volumeto'].iloc[-1]
    
    # --- Brain 1: BIT-NOTE (Liquidity Tracker) ---
    liquidity_status = "Scanning Floor"
    lower_grab = False
    upper_grab = False
    
    if abs(current_low - recent_low) < (recent_low * 0.003): # 0.3% Precision Range
        liquidity_status = "🔥 LOWER LIQUIDITY GRAB DETECTED"
        lower_grab = True
    elif abs(current_high - recent_high) < (recent_high * 0.003):
        liquidity_status = "🔥 UPPER LIQUIDITY GRAB DETECTED"
        upper_grab = True

    # --- Brain 2: BIT-GLASS (Session Trend Matrix) ---
    trend_status = "Bullish Structural Flow" if curr_price > ema21 else "Bearish Structural Flow"

    # --- Brain 3: BLACKROCK (Whale Volume Sentinel) ---
    whale_active = last_vol > (avg_vol * 1.5)
    whale_status = "🐋 WHALE ACCUMULATION TRIGGERED" if whale_active else "Retail Order Distribution"

    # --- 🎯 PURE ENTRY / EXIT COCKPIT DECISION LOGIC ---
    final_verdict = "MONITOR"
    entry_point = None
    exit_point = None
    reasoning = "Waiting for Smart Money Liquidity Grab or Institutional Rejection."

    # Rule 1: Lower Liquidity Grab + Bullish Trend = PURI ENTRY (BUY)
    if lower_grab and curr_price > ema21:
        final_verdict = "BUY"
        entry_point = curr_price
        exit_point = recent_high  # Next major liquidity pool high target
        reasoning = "Lower Liquidity Grab + Bullish EMA structure confirmed. Safe entry initialized."
        
    # Rule 2: Upper Liquidity Grab + Bearish Trend = ZED EXIT (SELL)
    elif upper_grab and curr_price < ema21:
        final_verdict = "SELL"
        entry_point = recent_low  # Drop floor target
        exit_point = curr_price
        reasoning = "Upper Liquidity Grab + Retail Trap confirmed near resistance layer."

    return {
        "price": curr_price,
        "ai1": liquidity_status,
        "ai2": trend_status,
        "ai3": whale_status,
        "verdict": final_verdict,
        "entry": entry_point,
        "exit": exit_point,
        "reason": reasoning
    }

# --- 🔍 COMMAND BOARD ---
st.sidebar.markdown("### 🏛️ ALADDIN SATELLITE COMMAND")
watchlist = ["BTC", "ETH", "SOL", "LINK", "DOT", "SHIB", "BONE", "BNB", "XRP", "MATIC"]
selected_asset = st.sidebar.selectbox("📂 PORTFOLIO TARGET", watchlist)

time_panel = {
    "1 Hour Scalp Engine": {"tf": "1h", "limit": 35},
    "12 Hour Session Matrix": {"tf": "1h", "limit": 120},
    "1 Month Macro Horizon": {"tf": "1d", "limit": 30}
}
selected_tf = st.sidebar.radio("⏱️ STREAM REFRESH INTERVAL", list(time_panel.keys()))
active_conf = time_panel[selected_tf]

# --- 🚀 RUN COMPILER ---
if selected_asset:
    data_stream = fetch_satellite_data(selected_asset, active_conf['tf'], active_conf['limit'])
    
    if data_stream is not None and not data_stream.empty:
        analysis = execute_aladdin_research(data_stream)
        
        st.markdown(f"<h2>🏛️ SATELLITE LINK: {selected_asset}/USDT</h2>", unsafe_allow_html=True)
        st.markdown(f"### CURRENT REAL PRICE: `${analysis['price']:,.4f}`")
        st.write("---")

        # --- 🎯 DYNAMIC TARGET ENGINE WINDOWS ---
        if analysis['verdict'] == "BUY":
            st.markdown(f"""
                <div class='signal-box pure-buy'>
                    🚀 ALADDIN BREAKOUT SIGNAL: 🟢 PURI ENTRY CONFIRMED<br>
                    <span style='font-size: 1.8rem; color: white;'>👉 TARGET ENTRY POINT: ${analysis['entry']:,.4f}</span><br>
                    <span style='font-size: 1.2rem; color: #a3e6be;'>Take Profit / Zed Ceiling Target: ${analysis['exit']:,.4f}</span><br>
                    <p style='font-size: 1rem; font-weight: normal; margin-top: 10px;'>{analysis['reason']}</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Send Urgent Telegram Notification Only On Pure Signal Hits
            if st.session_state.get("last_tg_state") != f"{selected_asset}_BUY":
                tg_msg = f"🏛️ *ALADDIN OMNI-SATELLITE ACTION* 🏛️\n\nAsset: {selected_asset}/USDT\nVerdict: 🟢 *PURI ENTRY CONFIRMED*\nEntry Point: ${analysis['entry']:,.4f}\nExit Layer: ${analysis['exit']:,.4f}\n\nSMC Research Status: {analysis['reason']}"
                send_telegram_message(tg_msg)
                st.session_state.last_tg_state = f"{selected_asset}_BUY"

        elif analysis['verdict'] == "SELL":
            st.markdown(f"""
                <div class='signal-box pure-sell'>
                    ⚠️ ALADDIN BREAKOUT SIGNAL: 🔴 ZED EXIT ZONE ACTIVE<br>
                    <span style='font-size: 1.8rem; color: white;'>👉 LIQUIDATION EXIT POINT: ${analysis['exit']:,.4f}</span><br>
                    <span style='font-size: 1.2rem; color: #fba3a3;'>Next Demand Target Floor: ${analysis['entry']:,.4f}</span><br>
                    <p style='font-size: 1rem; font-weight: normal; margin-top: 10px;'>{analysis['reason']}</p>
                </div>
            """, unsafe_allow_html=True)
            
            if st.session_state.get("last_tg_state") != f"{selected_asset}_SELL":
                tg_msg = f"🏛️ *ALADDIN OMNI-SATELLITE ACTION* 🏛️\n\nAsset: {selected_asset}/USDT\nVerdict: 🔴 *ZED EXIT TRIGGERED*\nLiquidation Layer: ${analysis['exit']:,.4f}\nNext Demand Floor: ${analysis['entry']:,.4f}"
                send_telegram_message(tg_msg)
                st.session_state.last_tg_state = f"{selected_asset}_SELL"

        else:
            st.markdown(f"""
                <div class='signal-box pure-monitor'>
                    ⚪ NO PURE ENTRY LAYER YET (SAFELY SCANNING)<br>
                    <span style='font-size: 1.2rem; color: #8b949e;'>{analysis['reason']}</span>
                </div>
            """, unsafe_allow_html=True)
            st.session_state.last_tg_state = f"{selected_asset}_MONITOR"

        # --- 🤖 3-BRAIN SEPARATE STATUS PIPELINE ---
        st.subheader("🤖 LAYERED AI ANALYTICS CONTEXT")
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.markdown(f"<div class='terminal-card'><h4>🎯 AI 1: BIT-NOTE (SMC-1H)</h4><p style='font-size:16px;'><b>{analysis['ai1']}</b></p></div>", unsafe_allow_html=True)
        with col_b:
            st.markdown(f"<div class='terminal-card'><h4>🛰️ AI 2: BIT-GLASS (Session Flow)</h4><p style='font-size:16px;'><b>{analysis['ai2']}</b></p></div>", unsafe_allow_html=True)
        with col_c:
            st.markdown(f"<div class='terminal-card'><h4>🏛️ AI 3: BLACKROCK (Whale Size)</h4><p style='font-size:16px;'><b>{analysis['ai3']}</b></p></div>", unsafe_allow_html=True)

        # --- 📊 INSTITUTIONAL CANDLESTICK GRAPH CONTAINER ---
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
        
        st.plotly_chart(fig, use_container_width=True, key="aladdin_satellite_v21")
    else:
        st.error("📡 Satellite matrix down. Check exchange data sync streams.")
