import streamlit as st
import pandas as pd
import json
import websocket
import threading
import time

# --- 🔱 CORE SATELLITE CONFIG ---
st.set_page_config(page_title="H32 OMNICORE V1.0", layout="wide")

# Initialize Session State for Multi-Coin Live Data
if 'market_data' not in st.session_state:
    st.session_state.market_data = {
        "BTC": {"price": 0.0, "change": 0.0, "signal": "INITIALIZING"},
        "ETH": {"price": 0.0, "change": 0.0, "signal": "INITIALIZING"},
        "SOL": {"price": 0.0, "change": 0.0, "signal": "INITIALIZING"},
        "SUI": {"price": 0.0, "change": 0.0, "signal": "INITIALIZING"},
        "XRP": {"price": 0.0, "change": 0.0, "signal": "INITIALIZING"},
        "DOT": {"price": 0.0, "change": 0.0, "signal": "INITIALIZING"},
        "LINK": {"price": 0.0, "change": 0.0, "signal": "INITIALIZING"}
    }

# --- 🎨 SUPREME NEON MOBILE UI ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;900&display=swap');
    .stApp { background: #010204 !important; }
    .hyper-card {
        background: rgba(10, 15, 25, 0.95);
        border-radius: 18px;
        padding: 22px;
        margin-bottom: 20px;
        border: 1px solid #00f2ff22;
        box-shadow: 0 0 25px #00f2ff0a;
    }
    .price-display { font-family: 'Orbitron', sans-serif; font-size: 2.5rem; font-weight: 900; color: #fff; margin: 10px 0; }
    .neon-green { color: #00ff9d; text-shadow: 0 0 10px #00ff9d66; }
    .neon-red { color: #ff4444; text-shadow: 0 0 10px #ff444466; }
    .badge-signal { background: #1e293b; border: 1px solid #334155; padding: 4px 10px; border-radius: 6px; font-size: 0.75rem; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #fff; font-family: \"Orbitron\", sans-serif;'>🔱 OMNI-CORE LIVE Engine</h1>", unsafe_allow_html=True)
st.markdown("<div style='text-align:center; color:#58a6ff; font-size:0.8rem; margin-bottom:20px;'>PHASE 1: LIVE BINANCE WEBSOCKET STREAM</div>", unsafe_allow_html=True)

# --- 📡 WEBSOCKET BACKGROUND ENGINE ---
def on_message(ws, message):
    msg = json.loads(message)
    if 'data' in msg:
        data = msg['data']
        sym = data['s'].replace('USDT', '')
        if sym in st.session_state.market_data:
            price = float(data['c'])
            change = float(data['P'])
            
            # Phase 1: Pure Mathematical Signal
            if change > 1.5: signal = "🚀 PURI ENTRY LENI HAI (BULLISH)"
            elif change < -1.5: signal = "⚠️ WAIT FOR LIQUIDITY SWEEP"
            else: signal = "⚖️ MONITORING POSITION (SIDEWAYS)"
            
            st.session_state.market_data[sym] = {
                "price": price,
                "change": change,
                "signal": signal
            }

def start_socket():
    # Stream for multiple tickers
    streams = [f"{s.lower()}usdt@ticker" for s in st.session_state.market_data.keys()]
    url = f"wss://stream.binance.com:9443/stream?streams={'/'.join(streams)}"
    ws = websocket.WebSocketApp(url, on_message=on_message)
    ws.run_forever()

if 'socket_thread' not in st.session_state:
    st.session_state.socket_thread = threading.Thread(target=start_socket, daemon=True)
    st.session_state.socket_thread.start()

# --- 📱 LIVE MULTI-COIN DASHBOARD SCANNER ---
for sym, info in st.session_state.market_data.items():
    is_bullish = info['change'] >= 0
    change_color = "neon-green" if is_bullish else "neon-red"
    dot_color = "#00ff9d" if is_bullish else "#ff4444"
    
    fmt_p = f"{info['price']:,.2f}" if info['price'] > 1 else f"{info['price']:,.4f}"
    
    st.html(f"""
    <div class="hyper-card">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <div style="height: 10px; width: 10px; background: {dot_color}; border-radius: 50%; box-shadow: 0 0 10px {dot_color};"></div>
                <b style="font-size: 1.4rem; color: #fff;">{sym}/USDT</b>
            </div>
            <span class="{change_color}" style="font-weight: bold; font-size: 1.1rem;">{info['change']:+.2f}%</span>
        </div>
        
        <div class="price-display">${fmt_p}</div>
        
        <div style="margin-top: 15px; padding-top: 10px; border-top: 1px solid #1f2937; display: flex; justify-content: space-between; align-items: center;">
            <span style="color: #8b949e; font-size: 0.75rem;">ENGINE VERDICT:</span>
            <span class="badge-signal" style="color: {'#00ff9d' if 'PURI' in info['signal'] else '#ff4444' if 'WAIT' in info['signal'] else '#58a6ff'};">
                {info['signal']}
            </span>
        </div>
    </div>
    """)

# Auto refresh component to keep UI live
time.sleep(1)
st.rerun()
