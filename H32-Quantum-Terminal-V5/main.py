import streamlit as st
import pandas as pd
import json
import websocket
import threading
import time
import ssl

# --- 🔱 CORE CONFIG ---
st.set_page_config(page_title="H32 OMNICORE V1.0", layout="wide")

# --- 🚀 BULLETPROOF DATA CACHE ---
# Yeh function database ki tarah kaam karega jo kabhi crash nahi hoga
@st.cache_resource
def get_market_data():
    return {
        "BTC": {"price": 0.0, "change": 0.0, "signal": "WAITING..."},
        "ETH": {"price": 0.0, "change": 0.0, "signal": "WAITING..."},
        "SOL": {"price": 0.0, "change": 0.0, "signal": "WAITING..."},
        "SUI": {"price": 0.0, "change": 0.0, "signal": "WAITING..."},
        "XRP": {"price": 0.0, "change": 0.0, "signal": "WAITING..."},
        "DOT": {"price": 0.0, "change": 0.0, "signal": "WAITING..."},
        "LINK": {"price": 0.0, "change": 0.0, "signal": "WAITING..."}
    }

# Data ko variable mein load karein
live_data = get_market_data()

# --- 📡 BACKGROUND ENGINE ---
def on_message(ws, message):
    try:
        msg = json.loads(message)
        if 'data' in msg:
            d = msg['data']
            sym = d['s'].replace('USDT', '')
            
            if sym in live_data:
                price = float(d['c'])
                change = float(d['P'])
                
                if change > 1.5: sig = "🚀 PURI ENTRY (BULLISH)"
                elif change < -1.5: sig = "⚠️ LIQUIDITY SWEEP"
                else: sig = "⚖️ MONITORING"

                # Direct cache update (No errors)
                live_data[sym]["price"] = price
                live_data[sym]["change"] = change
                live_data[sym]["signal"] = sig
    except:
        pass

def start_socket():
    streams = [f"{s.lower()}usdt@ticker" for s in live_data.keys()]
    url = f"wss://stream.binance.com:9443/stream?streams={'/'.join(streams)}"
    ws = websocket.WebSocketApp(url, on_message=on_message)
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

# Sirf ek baar thread start karega
@st.cache_resource
def start_background_thread():
    thread = threading.Thread(target=start_socket, daemon=True)
    thread.start()
    return thread

start_background_thread()

# --- 🎨 UI DESIGN ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;900&display=swap');
    .stApp { background: #010204 !important; }
    .card { background: rgba(10, 15, 25, 0.95); border-radius: 15px; padding: 20px; margin-bottom: 15px; border: 1px solid #00f2ff22; }
    .price { font-family: 'Orbitron', sans-serif; font-size: 2rem; color: #fff; font-weight: 900; }
    .green { color: #00ff9d; }
    .red { color: #ff4444; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #fff; font-family: \"Orbitron\", sans-serif;'>🔱 OMNI-CORE LIVE</h1>", unsafe_allow_html=True)

# UI Display Loop
for sym, info in live_data.items():
    color = "green" if info['change'] >= 0 else "red"
    p_format = f"{info['price']:,.2f}" if info['price'] > 1 else f"{info['price']:,.4f}"
    
    st.markdown(f"""
    <div class="card">
        <div style="display: flex; justify-content: space-between;">
            <b style="color: #fff;">{sym}/USDT</b>
            <span class="{color}">{info['change']:+.2f}%</span>
        </div>
        <div class="price">${p_format}</div>
        <div style="color: #58a6ff; font-size: 0.8rem; margin-top: 5px;">{info['signal']}</div>
    </div>
    """, unsafe_allow_html=True)

# 2 second ka wait UI refresh ke liye
time.sleep(2)
st.rerun()
