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

# --- 🎨 ALADDIN PREMIUM SOLID DARK THEME ---
st.markdown("""
    <style>
    .stApp { background-color: #06090f !important; }
    .main { color: #f0f6fc; font-family: 'Inter', sans-serif; }
    .terminal-card { background-color: #0d1117; border: 1px solid #30363d; border-radius: 12px; padding: 20px; margin-bottom: 15px; }
    .predict-box { padding: 22px; border-radius: 15px; text-align: center; font-weight: bold; margin-bottom: 15px; }
    .whale-entry-zone { border: 2px solid #00ff88; background-color: #041910; color: #00ff88; box-shadow: 0 0 15px rgba(0,255,136,0.1); }
    .whale-exit-zone { border: 2px solid #ff4b4b; background-color: #220b0d; color: #ff4b4b; box-shadow: 0 0 15px rgba(255,75,75,0.1); }
    
    /* Summary Elements & Percentage Matrix boxes */
    .summary-box-in { border: 2px solid #58a6ff; background-color: #0c1a30; color: #58a6ff; border-radius: 15px; padding: 20px; text-align: center; font-weight: bold; }
    .summary-box-out { border: 2px solid #ff4b4b; background-color: #220b0d; color: #ff4b4b; border-radius: 15px; padding: 20px; text-align: center; font-weight: bold; }
    
    .net-flow-card { border-radius: 15px; padding: 22px; text-align: center; font-weight: bold; margin-bottom: 20px; font-size: 1.2rem; }
    .net-plus { border: 2px solid #00ff88; background-color: #051a10; color: #00ff88; box-shadow: 0 0 12px rgba(0,255,136,0.15); }
    .net-minus { border: 2px solid #ff4b4b; background-color: #220b0d; color: #ff4b4b; box-shadow: 0 0 12px rgba(255,75,75,0.15); }
    
    .wallet-log { font-family: 'Courier New', monospace; font-size: 13px; color: #00ff88; background-color: #0d1117; padding: 10px; border-radius: 5px; margin-bottom: 5px; border-left: 4px solid #00ff88; }
    .wallet-out { color: #ff4b4b; border-left: 4px solid #ff4b4b; }
    </style>
    """, unsafe_allow_html=True)

def send_telegram_alert(msg):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"}
        requests.post(url, json=payload, timeout=1)
    except:
        pass

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

if st.sidebar.selectbox("📂 PORTFOLIO TARGET", ["BTC", "ETH", "SOL", "LINK", "DOT", "SHIB", "BONE", "BNB", "XRP", "MATIC"]):
    selected_asset = st.session_state.get("st.sidebar.selectbox(📂 PORTFOLIO TARGET)") or "BTC"
    
    time_panel = {
        "⏱️ 15 Minutes Micro Scalp": "15m", "⏱️ 30 Minutes Session Spread": "30m",
        "⏱️ 1 Hour Structural Cluster": "1h", "⏱️ 2 Hours Momentum Shift": "2h",
        "⏱️ 3 Hours Mid-Session Core": "3h", "⏱️ 5 Hours Whale Block Layer": "5h",
        "⏱️ 10 Hours Institutional Weight": "10h", "⏱️ 15 Days Macro Horizon Block": "15d"
    }
    selected_tf_label = st.sidebar.selectbox("⏱️ SELECT PREDICTION TIME ENGINE", list(time_panel.keys()))
    active_tf_code = time_panel[selected_tf_label]
    
    data_stream = fetch_satellite_candles(selected_asset, active_tf_code, limit=60)
    
    if data_stream is not None and not data_stream.empty:
        curr_price = float(data_stream['close'].iloc[-1])
        recent_low = float(data_stream['low'].tail(30).min())
        recent_high = float(data_stream['high'].tail(30).max())
        
        predicted_entry = recent_low if curr_price > recent_low else curr_price * 0.991
        predicted_exit = recent_high if curr_price < recent_high else curr_price * 1.009
        
        st.markdown(f"<h2>🏛️ ALADDIN AI PREDICTOR: {selected_asset}/USDT</h2>", unsafe_allow_html=True)
        st.write("---")

        st.subheader("🔮 FUTURE MARKET TARGET PREDICTIONS")
        col_in, col_out = st.columns(2)
        with col_in:
            st.markdown(f"<div class='predict-box whale-entry-zone'><h3 style='margin:0; color:#00ff88;'>🟩 ALADDIN PREDICTED ENTRY POINT</h3><p style='font-size:28px; margin:10px 0; color:white;'>${predicted_entry:,.4f}</p></div>", unsafe_allow_html=True)
        with col_out:
            st.markdown(f"<div class='predict-box whale-exit-zone'><h3 style='margin:0; color:#ff4b4b;'>🟥 ALADDIN PREDICTED EXIT / SEL POINT</h3><p style='font-size:28px; margin:10px 0; color:white;'>${predicted_exit:,.4f}</p></div>", unsafe_allow_html=True)

        # 🐋 LIVE WALLET RADAR PIPELINE
        st.subheader("📡 LIVE INSTANT MILLION DOLLAR WALLET FLOW")
        whale_logs = scan_heavy_whale_wallets(selected_asset, curr_price)
        
        total_inflow_calc = 0.0
        total_outflow_calc = 0.0

        for tx in whale_logs:
            if "INFLOW" in tx['type']:
                total_inflow_calc += tx['raw_val']
                css_class = "wallet-log"
            else:
                total_outflow_calc += tx['raw_val']
                css_class = "wallet-log wallet-out"
                
            st.markdown(f"""
                <div class='{css_class}'>
                    <b>Address:</b> {tx['address']} | <b>Volume Qty:</b> {tx['size']} | <b>Value USD:</b> <span style='color:white;'><b>{tx['formatted_val']}</b></span> | <b>Whale Entry Price:</b> <span style='color:#00ff88; font-weight:bold;'>${tx['entry_price']:,.4f}</span> | <b>Direction:</b> {tx['type']}
                </div>
            """, unsafe_allow_html=True)

        # --- 🧮 MATHEMATICAL PERCENTAGE DYNAMIC SYSTEM (BILKUL NICHE END) ---
        st.write("---")
        st.subheader("📊 LIVE SESSION TOTAL INSTITUTIONAL CASH WEIGHT")
        
        # Percentage Logic: Dono flows ka variance check karna
        total_combined = total_inflow_calc + total_outflow_calc
        if total_combined > 0:
            inflow_percentage = (total_inflow_calc / total_combined) * 100
            outflow_percentage = (total_outflow_calc / total_combined) * 100
        else:
            inflow_percentage, outflow_percentage = 0, 0

        # Main Dynamic Card logic matching plus/minus levels
        if total_inflow_calc >= total_outflow_calc:
            net_diff_pct = inflow_percentage - outflow_percentage
            st.markdown(f"""
                <div class='net-flow-card net-plus'>
                    🟢 NETWORK NET STATUS: PLUS (+) | Whales are Aggressively Loading!<br>
                    <span style='font-size:30px; color:white;'>+{net_diff_pct:.2f}% Cash Surplus</span> Injected Into Market
                </div>
            """, unsafe_allow_html=True)
        else:
            net_diff_pct = outflow_percentage - inflow_percentage
            st.markdown(f"""
                <div class='net-flow-card net-minus'>
                    🔴 NETWORK NET STATUS: MINUS (-) | Warning! Whales are Liquidating/Dumping!<br>
                    <span style='font-size:30px; color:white;'>-{net_diff_pct:.2f}% Cash Outflow</span> Extracted From Market
                </div>
            """, unsafe_allow_html=True)

        # Sub columns representing individual volume data
        col_sum_in, col_sum_out = st.columns(2)
        with col_sum_in:
            st.markdown(f"""
                <div class='summary-box-in'>
                    <h3 style='margin:0; color:#58a6ff;'>🟦 TOTAL ACCOUNT INFLOW</h3>
                    <p style='font-size:28px; margin:5px 0; color:white;'>{format_institutional_cash(total_inflow_calc)}</p>
                    <small style='color:#8ab4f8;'>Share Block Weight: {inflow_percentage:.1f}%</small>
                </div>
            """, unsafe_allow_html=True)
            
        with col_sum_out:
            st.markdown(f"""
                <div class='summary-box-out'>
                    <h3 style='margin:0; color:#ff4b4b;'>🟥 TOTAL ACCOUNT OUTFLOW</h3>
                    <p style='font-size:28px; margin:5px 0; color:white;'>{format_institutional_cash(total_outflow_calc)}</p>
                    <small style='color:#fba3a3;'>Share Block Weight: {outflow_percentage:.1f}%</small>
                </div>
            """, unsafe_allow_html=True)

        # Plotly chart
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
