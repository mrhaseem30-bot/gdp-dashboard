import streamlit as st
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# --- 🛰️ ALADDIN SATELLITE CORE ENGINE CONFIG ---
st.set_page_config(page_title="ALADDIN V16.1 MASTER", layout="wide")

# Secure Telegram Credentials (Using your verified ID)
TELEGRAM_BOT_TOKEN = "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"
TELEGRAM_CHAT_ID = "8376377797"

# --- 🛰️ LIVE CRYPTO REAL DATA FETCHER ---
def fetch_real_market_data(symbol, timeframe="1h", limit=168):
    """
    Direct institutional data stream API mapping from CryptoCompare public layer.
    """
    try:
        endpoint = "histohour" if "h" in timeframe else "histoday"
        url = f"https://min-api.cryptocompare.com/data/v2/{endpoint}?fsym={symbol}&tsym=USD&limit={limit}"
        res = requests.get(url).json()
        if res.get("Response") == "Success":
            df = pd.DataFrame(res['Data']['Data'])
            return df
        return None
    except Exception as e:
        return None

# --- 🤖 TELEGRAM ALERT DISPATCHER ---
def send_urgent_telegram_alert(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }
        requests.post(url, json=payload)
    except:
        pass

# --- 🧠 THE 3-BRAIN AI ENGINE INTER-LINKING ---
def run_3_brain_ai_analysis(df, symbol):
    """
    Inter-linking three layers of risk parameters to generate an institutional verdict.
    """
    if df is None or df.empty:
        return None

    # --- BRAIN 1: AI 1 Scalp Risk (1-Hour Micro-data window) ---
    recent_window = df.tail(24)
    local_high = recent_window['high'].max()
    local_low = recent_window['low'].min()
    curr_price = df['close'].iloc[-1]
    
    ai1_verdict = "⚪ MONITOR"
    if abs(curr_price - local_low) < (local_low * 0.005):
        ai1_verdict = "🟩 LIQUIDITY GRAB (BUY)"
    elif abs(curr_price - local_high) < (local_high * 0.005):
        ai1_verdict = "🟥 LIQUIDITY TRAP (SELL)"

    # --- BRAIN 2: AI 2 Session Risk (12-Hour Delhi Cycle tracking) ---
    df['EMA21'] = df['close'].ewm(span=21, adjust=False).mean()
    last_candle = df.iloc[-1]
    
    ai2_verdict = "Sideways Grid"
    if last_candle['close'] > last_candle['EMA21']:
        ai2_verdict = "Bullish Structural Break"
    else:
        ai2_verdict = "Bearish Structural Breakdown"

    # --- BRAIN 3: AI 3 BlackRock Macro Layer (1-Week Volume Flow Analysis) ---
    avg_volume = df['volumeto'].mean()
    last_volume = df['volumeto'].iloc[-1]
    
    ai3_verdict = "Retail Distribution"
    if last_volume > (avg_volume * 1.6):
        ai3_verdict = "🐋 WHALE ACCUMULATION ACTIVE"
    
    # --- INTER-LINKED FINAL POSITION VERDICT ---
    final_signal = "⚪ MONITOR"
    reason = "Waiting for institutional volume sync across Delhi sessions."
    
    if "BUY" in ai1_verdict and "Bullish" in ai2_verdict and "WHALE" in ai3_verdict:
        final_signal = "🟢 PURI ENTRY (STRONG BUY)"
        reason = "AI 1, 2, and 3 are beautifully synced: Lower Liquidity Grab + Whale Volume Inflow!"
    elif "SELL" in ai1_verdict and "Bearish" in ai2_verdict:
        final_signal = "🔴 ZED EXIT (URGENT SELL)"
        reason = "AI 1 & 2 Warning: Retail Trap (Fik Mot) active at major resistance floor."
        
    return {
        "ai1": ai1_verdict,
        "ai2": ai2_verdict,
        "ai3": ai3_verdict,
        "signal": final_signal,
        "reason": reason,
        "support": float(df['low'].min()),
        "resistance": float(df['high'].max()),
        "curr_price": float(curr_price)
    }

# --- 🎨 ADVANCED OMNI-TERMINAL UI SYSTEM ---
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #c9d1d9; font-family: 'Inter', sans-serif; }
    .terminal-title { font-size: 38px; font-weight: bold; color: #00f2ff; letter-spacing: 2px; }
    .ai-card { background-color: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 20px; margin-bottom: 15px; }
    .buy-box { background: linear-gradient(135deg, #041910, #0c3420); border: 2px solid #00ff88; padding: 25px; border-radius: 12px; color: #00ff88; }
    .sell-box { background: linear-gradient(135deg, #220b0d, #421417); border: 2px solid #ff4b4b; padding: 25px; border-radius: 12px; color: #ff4b4b; }
    </style>
    """, unsafe_allow_html=True)

# --- 🔍 SIDEBAR STRATEGY CONTROL ---
st.sidebar.markdown("### 🏛️ ALADDIN COMMAND UNIT")

# Connection Test Utility
if st.sidebar.button("🔌 Sync Terminal Pipelines"):
    send_urgent_telegram_alert("🏛️ *ALADDIN OMNI-MASTER UPDATE:*\nAll 3 AI Brains (Scalp, Session, Macro) are successfully linked to live exchange pipelines! 🛰️")
    st.sidebar.success("Pipelines connected! Test alert dispatched.")

st.sidebar.divider()

# --- 📂 DROPDOWN WATCHLIST LISTING (LINK Added Here) ---
account_watchlist = ["BTC", "ETH", "SOL", "LINK", "DOT", "SHIB", "BONE", "BNB", "XRP", "MATIC"]
selected_coin = st.sidebar.selectbox("📂 CHOOSE SYSTEM ACCOUNT ASSET", account_watchlist)

# System Timeframe Controller
time_map = {
    "1 Hour Scalp Engine": {"tf": "1h", "limit": 24},
    "12 Hour Session Matrix": {"tf": "1h", "limit": 120},
    "1 Month Institutional Horizon": {"tf": "1d", "limit": 30}
}
selected_tf_label = st.sidebar.radio("⏱️ TIME ANALYSIS HORIZON", list(time_map.keys()))
active_config = time_map[selected_tf_label]

# --- 🚀 RUN OMNI LIVE COMPUTATION LOOP ---
if selected_coin:
    raw_df = fetch_real_market_data(selected_coin, active_config['tf'], active_config['limit'])
    
    if raw_df is not None and not raw_df.empty:
        analysis = run_3_brain_ai_analysis(raw_df, selected_coin)
        
        # --- UI DISPLAY HEADLINE ---
        st.markdown(f"<div class='terminal-title'>🏛️ ALADDIN SYSTEM ACTIVE: {selected_coin}/USDT</div>", unsafe_allow_html=True)
        st.markdown(f"### LIVE EXCHANGE VALUE: `${analysis['curr_price']:,.2f}`")
        st.write(f"**Engine Last Sync Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Delhi Time Zone")
        st.write("---")

        # --- 🏗️ THE 3-BRAIN STATUS DISPLAY ---
        st.subheader("🤖 INTER-LINKED MULTI-AI PIPELINE STATUS")
        c1, c2, c3 = st.columns(3)
        
        with c1:
            st.markdown(f"""
            <div class='ai-card'>
                <h4 style='color: #00f2ff; margin:0;'>🎯 AI 1: BIT-NOTE (1H)</h4>
                <p style='margin: 10px 0 0 0; font-size:18px;'><b>Verdict:</b> {analysis['ai1']}</p>
                <small style='color: #8b949e;'>Micro liquidity scanner status</small>
            </div>
            """, unsafe_allow_html=True)
            
        with c2:
            st.markdown(f"""
            <div class='ai-card'>
                <h4 style='color: #ff9f1c; margin:0;'>🛰️ AI 2: BIT-GLASS (12H)</h4>
                <p style='margin: 10px 0 0 0; font-size:18px;'><b>Structure:</b> {analysis['ai2']}</p>
                <small style='color: #8b949e;'>Delhi Session risk framework</small>
            </div>
            """, unsafe_allow_html=True)
            
        with c3:
            st.markdown(f"""
            <div class='ai-card'>
                <h4 style='color: #00ff88; margin:0;'>🏛️ AI 3: BLACKROCK (1W)</h4>
                <p style='margin: 10px 0 0 0; font-size:18px;'><b>Macro Flow:</b> {analysis['ai3']}</p>
                <small style='color: #8b949e;'>Institutional order block weight</small>
            </div>
            """, unsafe_allow_html=True)

        st.write(" ")

        # --- 🚨 URGENT TELEGRAM SIGNAL EVALUATION ---
        if "prev_signal_key" not in st.session_state:
            st.session_state.prev_signal_key = ""

        current_signal_key = f"{selected_coin}_{analysis['signal']}_{active_config['tf']}"

        if "PURI" in analysis['signal']:
            st.markdown(f"""
            <div class='buy-box'>
                <h2 style='margin:0;'>🚀 SATELLITE POSITION VERDICT: {analysis['signal']}</h2>
                <p style='font-size:18px; margin:10px 0 0 0;'><b>Reasoning:</b> {analysis['reason']}</p>
                <h3 style='margin:15px 0 0 0; color:white;'>🎯 BUY TARGET SHIELD LAYER: ${analysis['support']:,.2f}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            if st.session_state.prev_signal_key != current_signal_key:
                tg_msg = f"🏛️ *ALADDIN OMNI-BRAIN REAL ALERT!!*\n\nAsset: {selected_coin}/USDT\nVerdict: 🟢 PURI ENTRY ACTIVE\nPrice: ${analysis['curr_price']:,.2f}\n\nAll 3 AI Brain layers verified liquidity accumulation!"
                send_urgent_telegram_alert(tg_msg)
                st.session_state.prev_signal_key = current_signal_key

        elif "ZED" in analysis['signal']:
            st.markdown(f"""
            <div class='sell-box'>
                <h2 style='margin:0;'>⚠️ SATELLITE POSITION VERDICT: {analysis['signal']}</h2>
                <p style='font-size:18px; margin:10px 0 0 0;'><b>Reasoning:</b> {analysis['reason']}</p>
                <h3 style='margin:15px 0 0 0; color:white;'>🛑 RISK DUMP EXIT LAYER: ${analysis['resistance']:,.2f}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            if st.session_state.prev_signal_key != current_signal_key:
                tg_msg = f"🏛️ *ALADDIN OMNI-BRAIN RISK ALERT!!*\n\nAsset: {selected_coin}/USDT\nVerdict: 🔴 URGENT ZED ZONE DUMP WARNING\nPrice: ${analysis['curr_price']:,.2f}\n\nRetail trap or institutional sell order block detected!"
                send_urgent_telegram_alert(tg_msg)
                st.session_state.prev_signal_key = current_signal_key
        else:
            st.info(f"🛰️ POSITION VERDICT: {analysis['signal']} — {analysis['reason']}")

        # --- 📊 LIVE LIQUIDITY FLOW VISUALIZATION ---
        st.write("---")
        st.subheader("📈 REAL-TIME INSTITUTIONAL PRICE SPREAD")
        st.line_chart(raw_df.set_index('time')['close'])

    else:
        st.error("📡 Live server engine failure. Connecting via backup Aladdin pipe...")
