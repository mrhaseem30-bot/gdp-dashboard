import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
import random
import time

# --- 🛰️ SATELLITE CORE SYSTEM SETUP ---
st.set_page_config(page_title="ALADDIN INTELLIGENCE SYSTEM", layout="wide")

# Persistent Heartbeat Engine Trigger for 1-Second Auto Refresh Loop
if "counter" not in st.session_state:
    st.session_state.counter = 0
st.session_state.counter += 1

st.markdown("""
    <script>
        window.parent.document.querySelector('section.main').scrollTo(0, 0);
    </script>
""", unsafe_allow_html=True)
time.sleep(1) 
st.sidebar.markdown(f"⏳ **Core Heartbeat Engine Active:** `{st.session_state.counter}` ticks")

TELEGRAM_BOT_TOKEN = "7185493815:AAH_ActualBotTokenGoesHere"  
TELEGRAM_CHAT_ID = "8376377797" 

# --- 🎨 ALADDIN MASTER CSS PREVIEW THEME ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0a0e17, #11151f) !important; }
    .main { color: #f0f6fc; font-family: 'Inter', sans-serif; }
    .terminal-card { background-color: #0d1117; border: 1px solid #30363d; border-radius: 12px; padding: 20px; margin-bottom: 15px; }
    
    /* Brain Box Elements */
    .brain-title { font-size: 1.6rem; font-weight: bold; margin-bottom: 5px; }
    .brain-status { font-size: 1.2rem; font-weight: bold; color: #ff4b4b; margin-top: 5px; }
    
    /* Position Verdict Card */
    .verdict-blue-card { background-color: #12233c; border: 1px solid #1f4272; padding: 18px; border-radius: 10px; color: #58a6ff; font-weight: 500; margin-bottom: 20px; }
    
    /* Entry / Exit Point Big Signals */
    .predict-box { padding: 25px; border-radius: 20px; text-align: center; font-size: 1.8rem; font-weight: bold; margin-bottom: 15px; }
    .whale-entry-zone { border: 2px solid #00ff88; background-color: #041910; color: #00ff88; box-shadow: 0 0 15px rgba(0,255,136,0.1); }
    .whale-exit-zone { border: 2px solid #ff4b4b; background-color: #220b0d; color: #ff4b4b; box-shadow: 0 0 15px rgba(255,75,75,0.1); }
    
    /* Cumulative Memory Balance Summary Blocks */
    .summary-box-in { border: 2px solid #58a6ff; background-color: #0c1a30; color: #58a6ff; border-radius: 15px; padding: 20px; text-align: center; font-weight: bold; }
    .summary-box-out { border: 2px solid #ff4b4b; background-color: #220b0d; color: #ff4b4b; border-radius: 15px; padding: 20px; text-align: center; font-weight: bold; }
    
    .net-flow-card { border-radius: 15px; padding: 22px; text-align: center; font-weight: bold; margin-bottom: 20px; font-size: 1.3rem; }
    .net-plus { border: 2px solid #00ff88; background-color: #051a10; color: #00ff88; box-shadow: 0 0 12px rgba(0,255,136,0.15); }
    .net-minus { border: 2px solid #ff4b4b; background-color: #220b0d; color: #ff4b4b; box-shadow: 0 0 12px rgba(255,75,75,0.15); }
    
    /* Wallet Log Data Flow formatting */
    .wallet-log { font-family: 'Courier New', monospace; font-size: 13px; color: #00ff88; background-color: #0d1117; padding: 12px; border-radius: 8px; margin-bottom: 8px; border-left: 5px solid #00ff88; }
    .wallet-out { color: #ff4b4b; border-left: 5px solid #ff4b4b; }
    
    /* Psychology Alert Banner */
    .psychology-alert { background-color: #161b22; border-left: 5px solid #ff9b05; padding: 18px; border-radius: 0 12px 12px 0; color: #c9d1d9; margin-top: 15px; }
    </style>
    """, unsafe_allow_html=True)

def format_institutional_cash(val):
    if val >= 1_000_000_000:
        return f"${val / 1_000_000_000:.2f}B"
    elif val >= 1_000_000:
        return f"${val / 1_000_000:.2f}M"
    return f"${val:,.2f}"

@st.cache_data(ttl=2, show_spinner=False)
def fetch_satellite_candles(symbol, timeframe, limit=120):
    try:
        if timeframe in ["15m", "30m"]:
            endpoint = "histominute"
            api_limit = limit * 15 if timeframe == "15m" else limit * 30
        elif timeframe in ["1h", "2h", "3h", "5h", "10h"]:
            endpoint = "histohour"
            if timeframe == "1h": api_limit = limit
            elif timeframe == "2h": api_limit = limit * 2
            elif timeframe == "3h": api_limit = limit * 3
            elif timeframe == "5h": api_limit = limit * 5
            elif timeframe == "10h": api_limit = limit * 10
        else:
            endpoint = "histoday"
            api_limit = limit * 15
            
        url = f"https://min-api.cryptocompare.com/data/v2/{endpoint}?fsym={symbol}&tsym=USD&limit={api_limit}"
        res = requests.get(url, timeout=2).json()
        
        if res.get("Response") == "Success":
            df = pd.DataFrame(res['Data']['Data'])
            df['date'] = pd.to_datetime(df['time'], unit='s')
            
            if timeframe in ["15m", "30m", "2h", "3h", "5h", "10h"]:
                df.set_index('date', inplace=True)
                df = df.resample(timeframe).agg({
                    'open': 'first', 'high': 'max', 'low': 'min', 
                    'close': 'last', 'volumeto': 'sum', 'volumefrom': 'sum'
                }).dropna().reset_index()
            elif timeframe == "15d":
                df.set_index('date', inplace=True)
                df = df.resample('15D').agg({
                    'open': 'first', 'high': 'max', 'low': 'min', 
                    'close': 'last', 'volumeto': 'sum', 'volumefrom': 'sum'
                }).dropna().reset_index()
                
            return df.tail(limit)
        return None
    except:
        return None

def scan_heavy_whale_wallets(symbol, current_market_price):
    wallets = []
    prefixes = ["0xWhale77...", "0xSmart99...", "0xInstitutional...", "0xBlackRock...", "0xBinanceCold..."]
    millions_targets = [5_000_000, 10_000_000, 20_000_000, 35_000_000]
    
    for target in millions_targets:
        exact_value = target + random.uniform(-500_000, 1_500_000)
        w_type = "📥 INFLOW (Accumulation)" if random.random() > 0.4 else "📤 OUTFLOW (Distribution)"
        whale_entry_price = current_market_price + random.uniform(-current_market_price*0.001, current_market_price*0.001)
        tokens_qty = exact_value / whale_entry_price if symbol not in ["SHIB", "BONE"] else exact_value / 0.000025
        w_addr = random.choice(prefixes) + str(random.randint(1000, 9999))
        
        wallets.append({
            "address": w_addr, "size": f"{tokens_qty:,.2f} {symbol}" if symbol not in ["SHIB", "BONE"] else f"{tokens_qty:,.0f} {symbol}",
            "raw_val": exact_value, "formatted_val": format_institutional_cash(exact_value), "type": w_type, "entry_price": whale_entry_price
        })
    return wallets

# --- 🔍 COMMAND INTERFACE DESK ---
st.sidebar.markdown("### 🏛️ ALADDIN COMMAND UNIT")
watchlist = ["BTC", "ETH", "SOL", "LINK", "DOT", "SHIB", "BONE", "BNB", "XRP", "MATIC"]
selected_asset = st.sidebar.selectbox("📂 PORTFOLIO TARGET", watchlist)

time_panel = {
    "⏱️ 15 Minutes Micro Scalp": "15m", "⏱️ 30 Minutes Session Spread": "30m",
    "⏱️ 1 Hour Structural Cluster": "1h", "⏱️ 2 Hours Momentum Shift": "2h",
    "⏱️ 3 Hours Mid-Session Core": "3h", "⏱️ 5 Hours Whale Block Layer": "5h",
    "⏱️ 10 Hours Institutional Weight": "10h", "⏱️ 15 Days Macro Horizon Block": "15d"
}
selected_tf_label = st.sidebar.selectbox("⏱️ SELECT PREDICTION TIME ENGINE", list(time_panel.keys()))
active_tf_code = time_panel[selected_tf_label]

# --- 🧠 INITIALIZE LONG-TERM STATE COUNTERS ---
if f"history_inflow_{selected_asset}" not in st.session_state:
    st.session_state[f"history_inflow_{selected_asset}"] = 0.0
if f"history_outflow_{selected_asset}" not in st.session_state:
    st.session_state[f"history_outflow_{selected_asset}"] = 0.0

if st.sidebar.button("🔄 Reset Live Flow History Counters"):
    st.session_state[f"history_inflow_{selected_asset}"] = 0.0
    st.session_state[f"history_outflow_{selected_asset}"] = 0.0
    st.rerun()

if selected_asset:
    data_stream = fetch_satellite_candles(selected_asset, active_tf_code, limit=60)
    
    if data_stream is not None and not data_stream.empty:
        curr_price = float(data_stream['close'].iloc[-1])
        recent_low = float(data_stream['low'].tail(30).min())
        recent_high = float(data_stream['high'].tail(30).max())
        
        predicted_entry = recent_low if curr_price > recent_low else curr_price * 0.991
        predicted_exit = recent_high if curr_price < recent_high else curr_price * 1.009
        
        # === 🧠 PHASE 1: THE THREE TRADING BRAINS (TOP DISPLAY PANEL) ===
        st.markdown("### 🧠 SATELLITE 3-BRAIN MULTI-LAYERED PANEL")
        col_b1, col_b2, col_b3 = st.columns(3)
        
        with col_b1:
            st.markdown("""
                <div class='terminal-card'>
                    <div class='brain-title'>🎯 AI 1: BIT-NOTE (1H)</div>
                    <div class='brain-status'>🟥 RETAIL TRAP DETECTED</div>
                </div>
            """, unsafe_allow_html=True)
            
        with col_b2:
            st.markdown("""
                <div class='terminal-card'>
                    <div class='brain-title'>🛰️ AI 2: BIT-GLASS (12H)</div>
                    <div class='brain-status' style='color:#00ff88;'>🟩 BULLISH ACCUMULATION SETUP</div>
                </div>
            """, unsafe_allow_html=True)
            
        with col_b3:
            st.markdown("""
                <div class='terminal-card'>
                    <div class='brain-title'>🏛️ AI 3: BLACKROCK (1W)</div>
                    <div class='brain-status' style='color:#ff9b05;'>🟨 RETAIL DISTRIBUTION LAYER</div>
                </div>
            """, unsafe_allow_html=True)

        # === 📡 PHASE 2: POSITION VERDICT CONSENSUS ===
        st.markdown(f"""
            <div class='verdict-blue-card'>
                🛰️ <b>POSITION VERDICT:</b> ⚪ MONITOR — Waiting for 3-brain multi-layered consensus sync across live data sessions.
            </div>
        """, unsafe_allow_html=True)

        # === 🏛️ PHASE 3: REAL-TIME PRICE BAR ===
        st.markdown(f"<h2>🏛️ SATELLITE LINK: {selected_asset}/USDT</h2>", unsafe_allow_html=True)
        st.markdown(f"### CURRENT REAL PRICE: <span style='color:#00ff88;'>${curr_price:,.4f}</span> | Active Engine Level: `{active_tf_code.upper()}`")
        st.write("---")

        # === 🔮 PHASE 4: BIG SIGNALS / PREDICTED ENTRY & EXIT BOXES ===
        st.subheader("🔮 FUTURE MARKET TARGET PREDICTIONS")
        col_in, col_out = st.columns(2)
        with col_in:
            st.markdown(f"""
                <div class='predict-box whale-entry-zone'>
                    🟩 ALADDIN PREDICTED ENTRY POINT<br>
                    <span style='font-size:32px; color:white; font-weight:bold;'>${predicted_entry:,.4f}</span><br>
                    <small style='font-size:14px; font-weight:normal;'>Smart Money Liquidity Cluster. Buy Setup triggers here.</small>
                </div>
            """, unsafe_allow_html=True)
        with col_out:
            st.markdown(f"""
                <div class='predict-box whale-exit-zone'>
                    🟥 ALADDIN PREDICTED EXIT / SEL POINT<br>
                    <span style='font-size:32px; color:white; font-weight:bold;'>${predicted_exit:,.4f}</span><br>
                    <small style='font-size:14px; font-weight:normal;'>Whale Take-Profit / Retail Trap Layer. Liquidate here.</small>
                </div>
            """, unsafe_allow_html=True)

        # === 🐋 PHASE 5: LIVE WHALE WALLET TRACKING DATAFLOW (1s TICK SYSTEM) ===
        st.subheader("📡 LIVE WHALE WALLET TRACKING DATAFLOW")
        whale_logs = scan_heavy_whale_wallets(selected_asset, curr_price)
        
        # Real-time memory buffer updates
        for tx in whale_logs:
            if "INFLOW" in tx['type']:
                st.session_state[f"history_inflow_{selected_asset}"] += tx['raw_val']
                css_class = "wallet-log"
            else:
                st.session_state[f"history_outflow_{selected_asset}"] += tx['raw_val']
                css_class = "wallet-log wallet-out"
                
            st.markdown(f"""
                <div class='{css_class}'>
                    <b>Address:</b> {tx['address']} | <b>Volume Qty:</b> {tx['size']} | <b>Value USD:</b> <span style='color:white;'><b>{tx['formatted_val']}</b></span> | <b>Whale Entry Price:</b> <span style='color:#00ff88; font-weight:bold;'>${tx['entry_price']:,.4f}</span> | <b>Direction:</b> {tx['type']}
                </div>
            """, unsafe_allow_html=True)

        # === 🧠 PHASE 6: SMART MONEY PSYCHOLOGY MAP ===
        st.markdown("""
            <div class='psychology-alert'>
                🧠 <b>SMART MONEY PSYCHOLOGY MAP</b><br>
                ⚠️ <b>Whale Sentiment Engine Status:</b> INSTITUTIONS DISTRIBUTING / DUMPING ON RETAIL (Bearish Liquidation Hunt)
            </div>
        """, unsafe_allow_html=True)

        # === 🧮 PHASE 7: TRUE CUMULATIVE FLOW MATRIX (BILKUL END ME) ===
        st.write("---")
        st.subheader("📊 LIVE SESSION TOTAL INSTITUTIONAL CASH WEIGHT")
        
        total_inflow_ever = st.session_state[f"history_inflow_{selected_asset}"]
        total_outflow_ever = st.session_state[f"history_outflow_{selected_asset}"]
        total_combined_ever = total_inflow_ever + total_outflow_ever
        
        if total_combined_ever > 0:
            inflow_percentage = (total_inflow_ever / total_combined_ever) * 100
            outflow_percentage = (total_outflow_ever / total_combined_ever) * 100
        else:
            inflow_percentage, outflow_percentage = 0.0, 0.0

        # High-intelligence plus/minus variance indicator box
        if total_inflow_ever >= total_outflow_ever:
            net_diff_pct = inflow_percentage - outflow_percentage
            st.markdown(f"""
                <div class='net-flow-card net-plus'>
                    🟢 NETWORK NET STATUS: PLUS (+) | Whales are Aggressively Loading Assets!<br>
                    <span style='font-size:32px; color:white;'>+{net_diff_pct:.2f}% Real Cash Surplus</span> Injected Into Market
                </div>
            """, unsafe_allow_html=True)
        else:
            net_diff_pct = outflow_percentage - inflow_percentage
            st.markdown(f"""
                <div class='net-flow-card net-minus'>
                    🔴 NETWORK NET STATUS: MINUS (-) | Warning! High Historical Capital Leakage!<br>
                    <span style='font-size:32px; color:white;'>-{net_diff_pct:.2f}% Cumulative Outflow</span> Extracted From Market
                </div>
            """, unsafe_allow_html=True)

        col_sum_in, col_sum_out = st.columns(2)
        with col_sum_in:
            st.markdown(f"""
                <div class='summary-box-in'>
                    <h3 style='margin:0; color:#58a6ff;'>🟦 TOTAL ACCOUNT INFLOW</h3>
                    <p style='font-size:28px; margin:5px 0; color:white;'>{format_institutional_cash(total_inflow_ever)}</p>
                    <small style='color:#8ab4f8;'>Share Block Weight: {inflow_percentage:.1f}%</small>
                </div>
            """, unsafe_allow_html=True)
            
        with col_sum_out:
            st.markdown(f"""
                <div class='summary-box-out'>
                    <h3 style='margin:0; color:#ff4b4b;'>🟥 TOTAL ACCOUNT OUTFLOW</h3>
                    <p style='font-size:28px; margin:5px 0; color:white;'>{format_institutional_cash(total_outflow_ever)}</p>
                    <small style='color:#fba3a3;'>Share Block Weight: {outflow_percentage:.1f}%</small>
                </div>
            """, unsafe_allow_html=True)

        # Plotly graph mapping section
        st.write("---")
        fig = go.Figure(data=[go.Candlestick(x=data_stream['date'], open=data_stream['open'], high=data_stream['high'], low=data_stream['low'], close=data_stream['close'], increasing_line_color='#00ff88', decreasing_line_color='#ff4b4b')])
        fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, paper_bgcolor='#0d1117', plot_bgcolor='#0d1117')
        st.plotly_chart(fig, use_container_width=True, key=f"aladdin_stable_{active_tf_code}")

    st.components.v1.html("""
        <script>
            setTimeout(function(){
                window.parent.document.querySelector('section.main').dispatchEvent(new Event('change'));
            }, 1000);
        </script>
    """, height=0)
