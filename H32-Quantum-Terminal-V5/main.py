import streamlit as st
import pandas as pd
import json
import websocket
import threading
import time
import ssl

# --- 🔱 CORE CONFIG ---
st.set_page_config(page_title="H32 OMNICORE V1.0", layout="wide")

# Background thread aur UI ke darmiyan data share karne ke liye
if 'live_cache' not in st.session_state:
    st.session_state.live_cache = {
        "BTC": {"price": 0.0, "change": 0.0, "signal": "CONNECTING..."},
        "ETH": {"price": 0.0, "change": 0.0, "signal": "CONNECTING..."},
        "SOL": {"price": 0.0, "change": 0.0, "signal": "CONNECTING..."},
        "SUI": {"price": 0.0, "change": 0.0, "signal": "CONNECTING..."},
        "XRP": {"price": 0.0, "change": 0.0, "signal": "CONNECTING..."},
        "DOT": {"price": 0.0, "change": 0.0, "signal": "CONNECTING..."},
        "LINK": {"price": 0.0, "change": 0.0, "signal": "CONNECTING..."}
    }

# --- 🎨 SUPREME UI ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;900&display=swap');
    .stApp { background: #010204 !important; }
    .hyper-card {
        background: rgba(10, 15, 25, 0.95);
        border-radius: 18px;
        padding: 20px;
        margin-bottom: 15px;
        border: 1px solid #00f2ff22;
    }
    .price-display { font-family: 'Orbitron', sans-serif; font-size: 2.2rem; font-weight: 900; color: #fff; }
    .neon-green { color: #00ff9d; }
    .neon-red { color: #ff4444; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #fff; font-family: \"Orbitron\", sans-serif;'>🔱 OMNI-CORE LIVE</h1>", unsafe_allow_html=True)

# --- 📡 FIX: BACKGROUND ENGINE ---
def on_message(ws, message):
    try:
        msg = json.loads(message)
        if 'data' in msg:
            d = msg['data']
            sym = d['s'].replace('USDT', '')
            
            price = float(d['c'])
            change = float(d['P'])
            
            if change > 1.5: sig = "🚀 PURI ENTRY (BULLISH)"
            elif change < -1.5: sig = "⚠️ LIQUIDITY SWEEP"
            else: sig = "⚖️ MONITORING"

            # Session state ko thread safe tareeqe se update karna
            st.session_state.live_cache[sym] = {
                "price": price, 
                "change": change, 
                "signal": sig
            }
    except:
        pass

def start_socket():
    streams = [f"{s.lower()}usdt@ticker" for s in st.session_state.live_cache.keys()]
    url = f"wss://stream.binance.com:9443/stream?streams={'/'.join(streams)}"
    ws = websocket.WebSocketApp(url, on_message=on_message)
    # SSL fix for cloud
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

if 'socket_active' not in st.session_state:
    st.session_state.socket_active = True
    threading.Thread(target=start_socket, daemon=True).start()

# --- 📱 LIVE DASHBOARD ---
for sym, info in st.session_state.live_cache.items():
    c_color = "neon-green" if info['change'] >= 0 else "neon-red"
    p_val = f"{info['price']:,.2f}" if info['price'] > 1 else f"{info['price']:,.4f}"
    
    st.markdown(f"""
    <div class="hyper-card">
        <div style="display: flex; justify-content: space-between;">
            <b style="color: #fff; font-size: 1.1rem;">{sym}/USDT</b>
            <span class="{c_color}" style="font-weight: bold;">{info['change']:+.2f}%</span>
        </div>
        <div class="price-display">${p_val}</div>
        <div style="color: #58a6ff; font-size: 0.7rem; margin-top: 5px;">VERDICT: {info['signal']}</div>
    </div>
    """, unsafe_allow_html=True)

# UI Refresh
time.sleep(2)
st.rerun()
