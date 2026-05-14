import streamlit as st
import pandas as pd
import json
import websocket
import threading
import time
import ssl  # SSL connection ke liye zaroori hai

# --- 🔱 CORE CONFIG ---
st.set_page_config(page_title="H32 OMNICORE V1.0", layout="wide")

# Session State for Market Data
if 'market_data' not in st.session_state:
    st.session_state.market_data = {
        "BTC": {"price": 0.0, "change": 0.0, "signal": "CONNECTING..."},
        "ETH": {"price": 0.0, "change": 0.0, "signal": "CONNECTING..."},
        "SOL": {"price": 0.0, "change": 0.0, "signal": "CONNECTING..."},
        "SUI": {"price": 0.0, "change": 0.0, "signal": "CONNECTING..."},
        "XRP": {"price": 0.0, "change": 0.0, "signal": "CONNECTING..."},
        "DOT": {"price": 0.0, "change": 0.0, "signal": "CONNECTING..."},
        "LINK": {"price": 0.0, "change": 0.0, "signal": "CONNECTING..."}
    }

# --- 🎨 UI STYLING ---
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
    }
    .price-display { font-family: 'Orbitron', sans-serif; font-size: 2.5rem; font-weight: 900; color: #fff; }
    .neon-green { color: #00ff9d; text-shadow: 0 0 10px #00ff9d66; }
    .neon-red { color: #ff4444; text-shadow: 0 0 10px #ff444466; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #fff; font-family: \"Orbitron\", sans-serif;'>🔱 OMNI-CORE LIVE</h1>", unsafe_allow_html=True)

# --- 📡 IMPROVED WEBSOCKET ENGINE ---
def on_message(ws, message):
    try:
        msg = json.loads(message)
        if 'data' in msg:
            data = msg['data']
            sym = data['s'].replace('USDT', '')
            if sym in st.session_state.market_data:
                price = float(data['c'])
                change = float(data['P'])
                
                # Signal Logic
                if change > 1.5: sig = "🚀 PURI ENTRY (BULLISH)"
                elif change < -1.5: sig = "⚠️ LIQUIDITY SWEEP"
                else: sig = "⚖️ MONITORING"
                
                st.session_state.market_data[sym] = {"price": price, "change": change, "signal": sig}
    except Exception as e:
        pass # Background errors ko silently handle karega

def start_socket():
    streams = [f"{s.lower()}usdt@ticker" for s in st.session_state.market_data.keys()]
    url = f"wss://stream.binance.com:9443/stream?streams={'/'.join(streams)}"
    
    # SSL_NONE setting numbers ko zero se hatane mein madad karegi
    ws = websocket.WebSocketApp(url, on_message=on_message)
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

if 'socket_thread' not in st.session_state:
    st.session_state.socket_thread = threading.Thread(target=start_socket, daemon=True)
    st.session_state.socket_thread.start()

# --- 📱 DASHBOARD ---
for sym, info in st.session_state.market_data.items():
    col_color = "neon-green" if info['change'] >= 0 else "neon-red"
    fmt_p = f"{info['price']:,.2f}" if info['price'] > 1 else f"{info['price']:,.4f}"
    
    st.markdown(f"""
    <div class="hyper-card">
        <div style="display: flex; justify-content: space-between;">
            <b style="color: #fff; font-size: 1.2rem;">{sym}/USDT</b>
            <span class="{col_color}">{info['change']:+.2f}%</span>
        </div>
        <div class="price-display">${fmt_p}</div>
        <div style="color: #58a6ff; font-size: 0.8rem; margin-top: 10px;">
            VERDICT: {info['signal']}
        </div>
    </div>
    """, unsafe_allow_html=True)

# 2-3 seconds ka wait taake connection stable rahe
time.sleep(2)
st.rerun()
