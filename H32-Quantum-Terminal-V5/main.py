import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# --- 🛰️ SATELLITE CORE SYSTEM SETUP ---
st.set_page_config(page_title="ALADDIN INTELLIGENCE SYSTEM", layout="wide")

TELEGRAM_BOT_TOKEN = "7185493815:AAH_ActualBotTokenGoesHere"  # Apna Token idhar dalein
TELEGRAM_CHAT_ID = "8376377797" 

# --- 🎨 ALADDIN PREMIUM INSTITUTIONAL DARK THEME ---
st.markdown("""
    <style>
    .stApp { background-color: #06090f !important; }
    .main { color: #f0f6fc; font-family: 'Inter', sans-serif; }
    .terminal-card { background-color: #0d1117; border: 1px solid #30363d; border-radius: 12px; padding: 20px; margin-bottom: 15px; }
    
    /* Aladdin Predictive Target Boxes */
    .predict-box { padding: 22px; border-radius: 15px; text-align: center; font-weight: bold; margin-bottom: 15px; }
    .whale-entry-zone { border: 2px solid #00ff88; background-color: #041910; color: #00ff88; box-shadow: 0 0 15px rgba(0,255,136,0.1); }
    .whale-exit-zone { border: 2px solid #ff4b4b; background-color: #220b0d; color: #ff4b4b; box-shadow: 0 0 15px rgba(255,75,75,0.1); }
    
    /* Psychology Board */
    .psychology-card { background-color: #161b22; border-left: 5px solid #58a6ff; padding: 15px; border-radius: 0 10px 10px 0; color: #c9d1d9; }
    .signal-banner { padding: 20px; border-radius: 12px; font-weight: bold; text-align: center; font-size: 1.4rem; margin-top: 15px; }
    .active-trigger { background-color: #051a10; border: 2px solid #00ff88; color: #00ff88; animation: pulse 2s infinite; }
    </style>
    """, unsafe_allow_html=True)

def send_telegram_alert(msg):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"}
        requests.post(url, json=payload, timeout=2)
    except:
        pass

# --- 📡 SATELLITE REAL-TIME TRANSMISSION PIPELINE ---
@st.cache_data(ttl=10, show_spinner=False)
def fetch_satellite_candles(symbol, timeframe, limit=100):
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

# --- 🧠 ALADDIN SMART MONEY PREDICTION MATRIX ---
def analyze_whale_prediction(df):
    curr_price = float(df['close'].iloc[-1])
    
    # 30-Candle High/Low Matrix for Predictive Mappings
    recent_high = float(df['high'].tail(30).max())
    recent_low = float(df['low'].tail(30).min())
    
    current_high = float(df['high'].iloc[-1])
    current_low = float(df['low'].iloc[-1])
    
    # Structural Indicators
    df['EMA21'] = df['close'].ewm(span=21, adjust=False).mean()
    ema21 = df['EMA21'].iloc[-1]
    
    avg_vol = df['volumeto'].mean()
    last_vol = df['volumeto'].iloc[-1]

    # Liquidity Calculations
    lower_sweep_active = abs(current_low - recent_low) < (recent_low * 0.003)
    upper_sweep_active = abs(current_high - recent_high) < (recent_high * 0.003)

    # Predictions & Targets (Aladdin Future Mapping Model)
    # Price prediction floor where big buy order limits are resting
    predicted_entry = recent_low if curr_price > recent_low else curr_price * 0.991
    # Price prediction ceiling where major whale profit takes are nested
    predicted_exit = recent_high if curr_price < recent_high else curr_price * 1.009

    # Whale Psychology State Predictor
    psychology_state = "Whale Neutral Accumulation (Sideways Market)"
    verdict = "SCANNING"
    verdict_desc = "Aladdin AI Engine is predicting order block clusters. Standing by."

    if curr_price > ema21 and last_vol > avg_vol:
        psychology_state = "🐋 WHALES ABSORBING RETAIL SELLING (Bullish Momentum)"
    elif curr_price < ema21 and last_vol > avg_vol:
        psychology_state = "⚠️ INSTITUTIONS DISTRIBUTING / DUMPING ON RETAIL (Bearish Momentum)"

    if lower_sweep_active and curr_price > ema21:
        verdict = "BUY"
        verdict_desc = f"🟢 PURI ENTRY VALIDATED! Whales grabbed liquidity at ${predicted_entry:,.2f}. Market is predicted to pump!"
    elif upper_sweep_active and curr_price < ema21:
        verdict = "SELL"
        verdict_desc = f"🔴 ZED EXIT ACTIVE! Retail trap triggered near ${predicted_exit:,.2f}. Smart money is pulling out!"

    return {
        "price": curr_price,
        "entry_target": predicted_entry,
        "exit_target": predicted_exit,
        "psychology": psychology_state,
        "verdict": verdict,
        "desc": verdict_desc,
        "high": recent_high,
        "low": recent_low
    }

# --- 🔍 CONTROL DESK ---
st.sidebar.markdown("### 🏛️ ALADDIN COMMAND UNIT")
watchlist = ["BTC", "ETH", "SOL", "LINK", "DOT", "SHIB", "BONE", "BNB", "XRP", "MATIC"]
selected_asset = st.sidebar.selectbox("📂 CHOOSE CORE ASSET", watchlist)

time_panel = {
    "1 Hour Scalp Engine": {"tf": "1h", "limit": 35},
    "12 Hour Session Matrix": {"tf": "1h", "limit": 120},
    "1 Month Macro Horizon": {"tf": "1d", "limit": 30}
}
selected_tf = st.sidebar.radio("⏱️ PREDICTION WINDOW", list(time_panel.keys()))
active_conf = time_panel[selected_tf]

# --- 🚀 EXECUTE & RENDER ENGINE ---
if selected_asset:
    data_stream = fetch_satellite_candles(selected_asset, active_conf['tf'], active_conf['limit'])
    
    if data_stream is not None and not data_stream.empty:
        aladdin = analyze_whale_prediction(data_stream)
        
        st.markdown(f"<h2>🏛️ ALADDIN AI PREDICTOR: {selected_asset}/USDT</h2>", unsafe_allow_html=True)
        st.markdown(f"### CURRENT REAL PRICE: `${aladdin['price']:,.4f}`")
        st.write("---")

        # --- 🎯 FUTURE PREDICTION TARGETS (Yeh hamesha dikhenge ke market kahan ja sakti hai) ---
        st.subheader("🔮 FUTURE MARKET TARGET PREDICTIONS")
        col_in, col_out = st.columns(2)
        
        with col_in:
            st.markdown(f"""
                <div class='predict-box whale-entry-zone'>
                    <h3 style='margin:0; color:#00ff88;'>🟩 ALADDIN PREDICTED ENTRY POINT</h3>
                    <p style='font-size:28px; margin:10px 0; color:white;'>${aladdin['entry_target']:,.4f}</p>
                    <small style='color:#a3e6be;'>Smart Money Liquidity Cluster. Buy Setup triggers here.</small>
                </div>
            """, unsafe_allow_html=True)
            
        with col_out:
            st.markdown(f"""
                <div class='predict-box whale-exit-zone'>
                    <h3 style='margin:0; color:#ff4b4b;'>🟥 ALADDIN PREDICTED EXIT / SEL POINT</h3>
                    <p style='font-size:28px; margin:10px 0; color:white;'>${aladdin['exit_target']:,.4f}</p>
                    <small style='color:#fba3a3;'>Whale Take-Profit / Retail Trap Layer. Liquidate here.</small>
                </div>
            """, unsafe_allow_html=True)

        # --- 🧠 LIVE WHALE PSYCHOLOGY ANALYTICS ---
        st.subheader("🧠 SMART MONEY PSYCHOLOGY MAP")
        st.markdown(f"""
            <div class='psychology-card'>
                <b>Whale Sentiment Engine Status:</b><br>
                <span style='font-size:1.2rem; color:white;'>{aladdin['psychology']}</span>
            </div>
        """, unsafe_allow_html=True)

        # --- 🚥 LIVE CONVERGENCE REFLEX SIGNALS ---
        st.write("---")
        st.subheader("🚨 REAL-TIME TRADE ALERT LOG")
        
        if aladdin['verdict'] == "BUY":
            st.markdown(f"<div class='signal-banner active-trigger'>{aladdin['desc']}</div>", unsafe_allow_html=True)
            if st.session_state.get("tg_lock") != f"{selected_asset}_BUY":
                send_telegram_alert(f"🔮 *ALADDIN MARKET PREDICTOR PRO*\nAsset: {selected_asset}\n🟢 *PREDICTED ENTRY HIT*: ${aladdin['entry_target']:,.4f}\n🎯 Target Exit: ${aladdin['exit_target']:,.4f}")
                st.session_state.tg_lock = f"{selected_asset}_BUY"
        elif aladdin['verdict'] == "SELL":
            st.markdown(f"<div class='signal-banner whale-exit-zone'>{aladdin['desc']}</div>", unsafe_allow_html=True)
            if st.session_state.get("tg_lock") != f"{selected_asset}_SELL":
                send_telegram_alert(f"🔮 *ALADDIN MARKET PREDICTOR PRO*\nAsset: {selected_asset}\n🔴 *PREDICTED EXIT HIT*: ${aladdin['exit_target']:,.4f}\n📉 Drop Floor: ${aladdin['entry_target']:,.4f}")
                st.session_state.tg_lock = f"{selected_asset}_SELL"
        else:
            st.markdown(f"<div class='signal-banner terminal-card' style='color:#8b949e;'>⚪ {aladdin['desc']}</div>", unsafe_allow_html=True)
            st.session_state.tg_lock = f"{selected_asset}_MONITOR"

        # --- 📊 CHART WITH PREDICTION LINES ---
        st.write("---")
        st.subheader("📊 REAL-TIME INSTITUTIONAL CANDLESTICK GRAPH")
        
        fig = go.Figure(data=[go.Candlestick(
            x=data_stream['date'], open=data_stream['open'], high=data_stream['high'],
            low=data_stream['low'], close=data_stream['close'],
            increasing_line_color='#00ff88', decreasing_line_color='#ff4b4b'
        )])
        
        # Adding predictive lines directly on the candlestick interface
        fig.add_hline(y=aladdin['entry_target'], line_dash="dash", line_color="#00ff88", annotation_text="Predicted Demand Floor")
        fig.add_hline(y=aladdin['exit_target'], line_dash="dash", line_color="#ff4b4b", annotation_text="Predicted Institutional Ceiling")

        fig.update_layout(
            template="plotly_dark", xaxis_rangeslider_visible=False,
            paper_bgcolor='#0d1117', plot_bgcolor='#0d1117',
            margin=dict(l=8, r=8, t=8, b=8), yaxis=dict(gridcolor='#1f242c', side="right")
        )
        st.plotly_chart(fig, use_container_width=True, key="aladdin_prophet_v23")
    else:
        st.error("📡 Core Satellite Connection Mapping Broken.")
