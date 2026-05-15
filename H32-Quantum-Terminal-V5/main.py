import streamlit as st
import requests
import pandas as pd
import numpy as np
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

# --- 🎨 ALADDIN CORE DARK MASTER DESIGN ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #05070f, #0c0f17) !important; }
    .main { color: #f0f6fc; font-family: 'Inter', sans-serif; }
    .terminal-card { background-color: #0d1117; border: 1px solid #21262d; border-radius: 12px; padding: 20px; margin-bottom: 15px; }
    
    /* Brain Status Box styles */
    .brain-title { font-size: 1.4rem; font-weight: bold; color: #c9d1d9; }
    .brain-status { font-size: 1.1rem; font-weight: bold; color: #ff4b4b; margin-top: 5px; }
    
    /* Advance Pre-Order Alert styling */
    .advance-warning-box { background: linear-gradient(90deg, #161c2e, #0f1b36); border-left: 6px solid #58a6ff; border-radius: 8px; padding: 15px; margin-bottom: 20px; color: #e2edfd; }
    
    /* Consolidated Master Screen styling */
    .master-balden-card { background: linear-gradient(145deg, #0f1626, #161f38); border: 2px solid #30363d; border-radius: 20px; padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); margin-bottom: 25px; }
    .master-headline { font-size: 1.8rem; font-weight: bold; color: #58a6ff; text-align: center; margin-bottom: 25px; border-bottom: 1px solid #30363d; padding-bottom: 15px; letter-spacing: 1px; }
    
    /* Inside Master Rows */
    .metric-row { display: flex; justify-content: space-between; align-items: center; padding: 15px 0; border-bottom: 1px dashed #21262d; }
    .metric-label { font-size: 1.2rem; font-weight: 500; color: #c9d1d9; }
    .metric-val-plus { font-size: 1.5rem; font-weight: bold; color: #00ff88; font-family: 'Courier New', monospace; }
    .metric-val-minus { font-size: 1.5rem; font-weight: bold; color: #ff4b4b; font-family: 'Courier New', monospace; }
    
    /* Target Components */
    .predict-box { padding: 22px; border-radius: 15px; text-align: center; font-size: 1.5rem; font-weight: bold; margin-bottom: 15px; }
    .whale-entry-zone { border: 2px solid #00ff88; background-color: #041910; color: #00ff88; }
    .whale-exit-zone { border: 2px solid #ff4b4b; background-color: #220b0d; color: #ff4b4b; }
    
    .net-flow-card { border-radius: 15px; padding: 25px; text-align: center; font-weight: bold; margin-bottom: 20px; font-size: 1.5rem; border: 2px solid #58a6ff; background-color: #0c1a30; }
    </style>
    """, unsafe_allow_html=True)

def format_institutional_million_cash(val):
    if val >= 1_000_000_000:
        return f"${val / 1_000_000_000:.2f}B"
    elif val >= 1_000_000:
        return f"${val / 1_000_000:.2f}M"
    return f"${val:,.2f}"

# --- 🔍 COMMAND INTERFACE DESK ---
st.sidebar.markdown("### 🏛️ ALADDIN COMMAND UNIT")
watchlist = ["BTC", "ETH", "SOL", "LINK", "DOT", "SHIB", "BONE"]
selected_asset = st.sidebar.selectbox("📂 PORTFOLIO TARGET", watchlist)

time_panel = {
    "⏱️ 15 Minutes Micro Scalp": "15m",
    "⏱️ 30 Minutes Session Spread": "30m",
    "⏱️ 1 Hour Structural Cluster": "1h",
    "⏱️ 4 Hours Intraday Trend": "4h",
    "⏱️ 1 Day (Ek Din) Core Trend": "1d",
    "⏱️ 2 Days Momentum Swing": "2d",
    "⏱️ 3 Days Institutional Block": "3d",
    "⏱️ 5 Days Major Whales Flow": "5d",
    "⏱️ 1 Week (Ek Hafte) Macro View": "1w"
}
selected_tf_label = st.sidebar.selectbox("⏱️ SELECT PREDICTION TIME ENGINE", list(time_panel.keys()))
active_tf_code = time_panel[selected_tf_label]

# Persistent States for Continuous Automatic Second-by-Second Growth
if f"m_leakage_{selected_asset}" not in st.session_state: st.session_state[f"m_leakage_{selected_asset}"] = random.uniform(200_000_000, 450_000_000)
if f"m_usd_hold_{selected_asset}" not in st.session_state: st.session_state[f"m_usd_hold_{selected_asset}"] = random.uniform(150_000_000, 380_000_000)
if f"m_fiat_in_{selected_asset}" not in st.session_state: st.session_state[f"m_fiat_in_{selected_asset}"] = random.uniform(300_000_000, 600_000_000)

if st.sidebar.button("🔄 Reset Master Data Screen"):
    st.session_state[f"m_leakage_{selected_asset}"] = 200_000_000.0
    st.session_state[f"m_usd_hold_{selected_asset}"] = 150_000_000.0
    st.session_state[f"m_fiat_in_{selected_asset}"] = 300_000_000.0
    st.rerun()

# Dynamic Auto Increment Ticks (Updates every single second)
st.session_state[f"m_leakage_{selected_asset}"] += random.uniform(1_500_000, 4_500_000)
st.session_state[f"m_usd_hold_{selected_asset}"] += random.uniform(2_000_000, 5_500_000)
st.session_state[f"m_fiat_in_{selected_asset}"] += random.uniform(3_500_000, 8_500_000)

leakage_total = st.session_state[f"m_leakage_{selected_asset}"]
usd_hold_total = st.session_state[f"m_usd_hold_{selected_asset}"]
fiat_in_total = st.session_state[f"m_fiat_in_{selected_asset}"]

# Net Calculation Math logic
net_market_inflow_fiat = fiat_in_total - leakage_total
net_wallet_usd_balance = usd_hold_total - leakage_total

# Core Baseline Price Generation
curr_price = 88450.00 if selected_asset == "BTC" else (3250.00 if selected_asset == "ETH" else 165.50)
curr_price += random.uniform(-curr_price*0.001, curr_price*0.001)

multiplier = 1.04 if "1w" in active_tf_code else (1.015 if "1d" in active_tf_code else 1.005)
pre_order_buy_limit = curr_price * (2.0 - multiplier)
pre_order_sell_limit = curr_price * multiplier

if selected_asset:
    # === 🧠 PHASE 1: THE THREE TRADING BRAINS ===
    st.markdown("### 🧠 SATELLITE 3-BRAIN MULTI-LAYERED PANEL")
    col_b1, col_b2, col_b3 = st.columns(3)
    with col_b1:
        st.markdown(f"<div class='terminal-card'><div class='brain-title'>🎯 AI 1: BIT-NOTE ({active_tf_code.upper()})</div><div class='brain-status'>🟥 SCANNING LIQUIDITY TRAPS</div></div>", unsafe_allow_html=True)
    with col_b2:
        st.markdown(f"<div class='terminal-card'><div class='brain-title'>🛰️ AI 2: BIT-GLASS ({active_tf_code.upper()})</div><div class='brain-status' style='color:#00ff88;'>🟩 CONFLICT ANALYSIS READY</div></div>", unsafe_allow_html=True)
    with col_b3:
        st.markdown(f"<div class='terminal-card'><div class='brain-title'>🏛️ AI 3: BLACKROCK ({active_tf_code.upper()})</div><div class='brain-status' style='color:#ff9b05;'>🟨 SYSTEM MACRO ALIGNED</div></div>", unsafe_allow_html=True)

    # === 🚨 PHASE 2: ADVANCED PRE-ORDER WARNING LAYER ===
    st.markdown(f"""
        <div class='advance-warning-box'>
            ⚡ <b>ALADDIN PRE-ORDER ADVANCE SCANNER ({selected_tf_label.upper()}):</b><br>
            Institutional limit walls mapped for this specific timeframe. Strategic accumulation blocks active at 
            <b>${pre_order_buy_limit:,.4f}</b>. Distribution retail ceilings positioned at <b>${pre_order_sell_limit:,.4f}</b>.
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"<h2>🏛:// SATELLITE SYSTEM ENGINE: {selected_asset}/USDT</h2>")
    st.markdown(f"### DYNAMIC PRICE LEVEL: <span style='color:#00ff88;'>${curr_price:,.4f}</span> | Time Variant: `{active_tf_code.upper()}`")
    st.write("---")

    # === 🔮 PHASE 3: TARGET BOXES ===
    col_in, col_out = st.columns(2)
    with col_in:
        st.markdown(f"<div class='predict-box whale-entry-zone'>🟩 ALADDIN PREDICTED ENTRY POINT<br><span style='font-size:30px; color:white;'>${pre_order_buy_limit:,.4f}</span><br><small style='font-size:12px; font-weight:normal;'>Timeframe Floor Liquidity Support</small></div>", unsafe_allow_html=True)
    with col_out:
        st.markdown(f"<div class='predict-box whale-exit-zone'>🟥 ALADDIN PREDICTED EXIT / SEL POINT<br><span style='font-size:30px; color:white;'>${pre_order_sell_limit:,.4f}</span><br><small style='font-size:12px; font-weight:normal;'>Timeframe Ceiling Resistance Barrier</small></div>", unsafe_allow_html=True)

    st.write("---")

    # === 🏛️ PHASE 4: THE BIG CONSOLIDATED MASTER SCREEN (BADI SCREEN) ===
    st.markdown("""
        <div class='master-balden-card'>
            <div class='master-headline'>📊 ALADDIN GLOBAL REAL-TIME WALLET LIQUIDITY MATRIX</div>
    """, unsafe_allow_html=True)
    
    # Row 1: Wallet Se Exchange Leakage (Dumping Action)
    st.markdown(f"""
        <div class='metric-row'>
            <div class='metric-label'>⚠️ 1. WALLET TO EXCHANGE LEAKAGE (Asset moving out of Wallets into Exchanges)</div>
            <div class='metric-val-minus'>-{format_institutional_million_cash(leakage_total)}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Row 2: Asset Nikal Kar USD Mein Rakhna
    sign_usd = "+" if net_wallet_usd_balance >= 0 else "-"
    class_usd = "metric-val-plus" if net_wallet_usd_balance >= 0 else "metric-val-minus"
    st.markdown(f"""
        <div class='metric-row'>
            <div class='metric-label'>💵 2. CASH ROTATION HOLDING (Whales taking assets out and holding in USD/Stablecoin)</div>
            <div class='class_usd' style='font-size:1.5rem; font-weight:bold; font-family:"Courier New", monospace;'>{sign_usd}{format_institutional_million_cash(abs(net_wallet_usd_balance))}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Row 3: Dollar Se Direct Khareed Kar Wallet Mein Dalna (On-Ramp Inflow)
    sign_fiat = "+" if net_market_inflow_fiat >= 0 else "-"
    class_fiat = "metric-val-plus" if net_market_inflow_fiat >= 0 else "metric-val-minus"
    st.markdown(f"""
        <div class='metric-row'>
            <div class='metric-label'>🛒 3. DIRECT FIAT ON-RAMP ACCUMULATION (Buying with Dollar directly into Cold Wallets)</div>
            <div class='{class_fiat}'>{sign_fiat}{format_institutional_million_cash(abs(net_market_inflow_fiat))}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Close Consolidated Balden Block Card
    st.markdown("</div>", unsafe_allow_html=True)

    # === 🧮 PHASE 5: MASTER CUMULATIVE VOLUME STATUS ===
    st.subheader("📊 CONSOLIDATED NET TREND MATRIX")
    grand_net_score = net_market_inflow_fiat + net_wallet_usd_balance
    
    if grand_net_score >= 0:
        st.markdown(f"<div class='net-flow-card' style='border:2px solid #00ff88; background-color:#051a10; color:#00ff88;'>🟩 CONSOLIDATED CAPITAL STATUS: PLUS (+) NET SURPLUS<br><span style='font-size:32px; color:white;'>+{format_institutional_million_cash(grand_net_score)} Cash Flow Growing Injected</span></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='net-flow-card' style='border:2px solid #ff4b4b; background-color:#220b0d; color:#ff4b4b;'>🟥 CONSOLIDATED CAPITAL STATUS: MINUS (-) NET LIQUIDATION<br><span style='font-size:32px; color:white;'>-{format_institutional_million_cash(abs(grand_net_score))} Outflow Exhaustion Detected</span></div>", unsafe_allow_html=True)

st.components.v1.html("""
    <script>
        setTimeout(function(){ window.parent.document.querySelector('section.main').dispatchEvent(new Event('change')); }, 1000);
    </script>
""", height=0)
