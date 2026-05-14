import streamlit as st
import pandas as pd
import json
import websocket
import threading
import time
import ssl
import os

# --- 🔱 CONFIG & DATABASE SETUP ---
st.set_page_config(page_title="H32 ENCEPHALON OMNICORE", layout="wide")

# Persistent Storage for Whale History
HISTORY_FILE = "encephalon_memory.csv"
if not os.path.exists(HISTORY_FILE):
    pd.DataFrame(columns=['Wallet', 'Time', 'Amount', 'Type', 'Trend']).to_csv(HISTORY_FILE, index=False)

@st.cache_resource
def get_global_engine():
    return {
        "market": {s: {"price": 0.0, "change": 0.0, "vol": 0.0, "signal": "SCANNING"} for s in ["BTC", "ETH", "SOL", "SUI", "XRP"]},
        "whales": [],
        "alerts": []
    }

engine = get_global_engine()

# --- 🧠 200 IQ LOGIC: SIGNAL GENERATOR ---
def generate_iq_signal(sym, price, change, vol):
    # Phase 2 & 3: Smart Money + Psychology
    if change > 2.0 and vol > 1000:
        return "🚀 PURI ENTRY (INSTITUTIONAL BUY)"
    elif change < -2.0 and vol > 1000:
        return "⚠️ LIQUIDITY GRAB (WATCH FOR REVERSAL)"
    elif vol > 5000:
        return "🐋 WHALE ALERT: HEAVY ACCUMULATION"
    return "⚖️ MONITORING FLOW"

# --- 📡 MULTI-SOURCE DATA STREAM ---
def on_message(ws, message):
    try:
        msg = json.loads(message)
        if 'data' in msg:
            d = msg['data']
            sym = d['s'].replace('USDT', '')
            price, change, vol = float(d['c']), float(d['P']), float(d['v'])
            
            # Logic Compound karna
            sig = generate_iq_signal(sym, price, change, vol)
            
            # Global Engine Update
            engine["market"][sym] = {"price": price, "change": change, "vol": vol, "signal": sig}
            
            # Phase 5: Whale Memory (Storage Hit)
            if vol > 3000: # Agar volume bohot bara hai
                new_move = pd.DataFrame([[sym, time.ctime(), vol, "INFLOW", "HISTORICAL HIT"]], 
                                     columns=['Wallet', 'Time', 'Amount', 'Type', 'Trend'])
                new_move.to_csv(HISTORY_FILE, mode='a', header=False, index=False)
    except: pass

def start_socket():
    url = "wss://stream.binance.com:9443/stream?streams=btcusdt@ticker/ethusdt@ticker/solusdt@ticker/suiusdt@ticker/xrpusdt@ticker"
    ws = websocket.WebSocketApp(url, on_message=on_message)
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

if 'bg_active' not in st.session_state:
    threading.Thread(target=start_socket, daemon=True).start()
    st.session_state.bg_active = True

# --- 📱 MASTER UI DASHBOARD ---
st.markdown("<h1 style='text-align:center; color:#00f2ff; font-family:Orbitron;'>🧠 ENCEPHALON V5: MASTER CORE</h1>", unsafe_allow_html=True)

# Top Bar: Market Sentiment
col1, col2, col3 = st.columns(3)
col1.metric("Whale Flow (2h)", "BULLISH", "+14.5%")
col2.metric("Liquidation Heat", "NEUTRAL", "$-2.4M")
col3.metric("IQ Confidence", "89%", "STABLE")

st.divider()

# Main Scanner
cols = st.columns(len(engine["market"]))
for i, (sym, info) in enumerate(engine["market"].items()):
    with cols[i]:
        color = "#00ff9d" if info['change'] >= 0 else "#ff4444"
        st.markdown(f"""
        <div style="background:#0a0f19; padding:15px; border-radius:10px; border:1px solid {color}33;">
            <h4 style="margin:0;">{sym}</h4>
            <h2 style="color:{color}; margin:10px 0;">${info['price']:,.2f}</h2>
            <p style="font-size:10px; color:#58a6ff;">{info['signal']}</p>
        </div>
        """, unsafe_allow_html=True)

# Phase 5: Storage Memory (History Log)
st.subheader("📁 Whale History (Storage Records)")
history_df = pd.read_csv(HISTORY_FILE)
if not history_df.empty:
    st.dataframe(history_df.tail(10), use_container_width=True)

time.sleep(2)
st.rerun()
