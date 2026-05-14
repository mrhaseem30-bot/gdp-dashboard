import streamlit as st
import pandas as pd
import json
import websocket
import threading
import time
import ssl

# --- 🔱 CORE CONFIG ---
st.set_page_config(page_title="H32 OMNICORE V1.0", layout="wide")

# GLOBAL DATA (Thread isko hamesha dekh sakega)
if 'live_data' not in st.globals:
    st.globals['live_data'] = {
        "BTC": {"price": 0.0, "change": 0.0, "signal": "WAITING..."},
        "ETH": {"price": 0.0, "change": 0.0, "signal": "WAITING..."},
        "SOL": {"price": 0.0, "change": 0.0, "signal": "WAITING..."},
        "SUI": {"price": 0.0, "change": 0.0, "signal": "WAITING..."},
        "XRP": {"price": 0.0, "change": 0.0, "signal": "WAITING..."},
        "DOT": {"price": 0.0, "change": 0.0, "signal": "WAITING..."},
        "LINK": {"price": 0.0, "change": 0.0, "signal": "WAITING..."}
    }

# --- 📡 BACKGROUND ENGINE (FIXED) ---
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

            # GLOBAL dictionary update kar rahe hain (st.session_state use nahi kar rahe)
            st.globals['live_data'][sym] = {"price": price, "change": change, "signal": sig}
    except:
        pass

def start_socket():
    streams = [f"{s.lower()}usdt@ticker" for s in st.globals['live_data'].keys()]
    url = f"wss://stream.binance.com:9443/stream?streams={'/'.join(streams)}"
    ws = websocket.WebSocketApp(url, on_message=on_message)
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

# Thread ko check karna ke wo pehle se chal to nahi raha
if 'bg_thread' not in st.globals:
    st.globals['bg_thread'] = threading.Thread(target=start_socket, daemon=True)
    st.globals['bg_thread'].start()

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
for sym, info in st.globals['live_data'].items():
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

time.sleep(2)
st.rerun()
