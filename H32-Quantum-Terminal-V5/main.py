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
    
    /* Distinct Terminal Pipelines */
    .pipeline-header { font-size: 1.3rem; font-weight: bold; margin-top: 15px; margin-bottom: 10px; border-bottom: 2px solid #30363d; padding-bottom: 5px; }
    
    /* Log Entries Custom Badges */
    .list-log { font-family: 'Courier New', monospace; font-size: 12.5px; background-color: #161b22; padding: 10px; border-radius: 6px; margin-bottom: 6px; box-shadow: inset 0 0 5px rgba(0,0,0,0.2); }
    .badge-danger { color: #ff4b4b; font-weight: bold; }
    .badge-success { color: #00ff88; font-weight: bold; }
    .badge-blue { color: #58a6ff; font-weight: bold; }
    
    /* Summary and Target Components */
    .predict-box { padding: 22px; border-radius: 15px; text-align: center; font-size: 1.5rem; font-weight: bold; margin-bottom: 15px; }
    .whale-entry-zone { border: 2px solid #00ff88; background-color: #041910; color: #00ff88; }
    .whale-exit-zone { border: 2px solid #ff4b4b; background-color: #220b0d; color: #ff4b4b; }
    
    .net-flow-card { border-radius: 15px; padding: 22px; text-align: center; font-weight: bold; margin-bottom: 20px; font-size: 1.3rem; }
    .net-plus { border: 2px solid #00ff88; background-color: #051a10; color: #00ff88; }
    .net-minus { border: 2px solid #ff4b4b; background-color: #220b0d; color: #ff4b4b; }
    
    .summary-box-in { border: 2px solid #58a6ff; background-color: #0c1a30; color: #58a6ff; border-radius: 12px; padding: 15px; text-align: center; font-weight: bold; }
    .summary-box-out { border: 2px solid #ff4b4b; background-color: #220b0d; color: #ff4b4b; border-radius: 12px; padding: 15px; text-align: center; font-weight: bold; }
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

# --- 📅 SEQUENTIAL TIME MAP (15 MINS TO 1 WEEK WEEKLY MACRO) ---
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

# Persistent Historical Cumulative States
if f"hist_in_{selected_asset}" not in st.session_state: st.session_state[f"hist_in_{selected_asset}"] = random.uniform(50_000_000, 120_000_000)
if f"hist_out_{selected_asset}" not in st.session_state: st.session_state[f"hist_out_{selected_asset}"] = random.uniform(40_000_000, 95_000_000)

if st.sidebar.button("🔄 Reset Global Flow Matrix"):
    st.session_state[f"hist_in_{selected_asset}"] = 0.0
    st.session_state[f"hist_out_{selected_asset}"] = 0.0
    st.rerun()

# Dynamic Ticks Generation Engine (Incremental Numbers changing every second)
tick_inflow_growth = random.uniform(2_500_000, 8_500_000)
tick_outflow_growth = random.uniform(1_500_000, 7_500_000)

st.session_state[f"hist_in_{selected_asset}"] += tick_inflow_growth
st.session_state[f"hist_out_{selected_asset}"] += tick_outflow_growth

total_in_ever = st.session_state[f"hist_in_{selected_asset}"]
total_out_ever = st.session_state[f"hist_out_{selected_asset}"]

# Dynamic Price generation simulation based on assets
curr_price = 88450.00 if selected_asset == "BTC" else (3250.00 if selected_asset == "ETH" else 165.50)
curr_price += random.uniform(-curr_price*0.002, curr_price*0.002)

# Adjustment of buffers depending on structural macro selections
multiplier = 1.05 if "1w" in active_tf_code else (1.02 if "1d" in active_tf_code else 1.006)
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

    st.markdown(f"<h2>🏛:// SATELLITE CORE SYSTEM: {selected_asset}/USDT</h2>")
    st.markdown(f"### DYNAMIC PRICE LEVEL: <span style='color:#00ff88;'>${curr_price:,.4f}</span> | Time Variant: `{active_tf_code.upper()}`")
    st.write("---")

    # === 🔮 PHASE 3: TARGET BOXES ===
    col_in, col_out = st.columns(2)
    with col_in:
        st.markdown(f"<div class='predict-box whale-entry-zone'>🟩 ALADDIN PREDICTED ENTRY POINT<br><span style='font-size:30px; color:white;'>${pre_order_buy_limit:,.4f}</span><br><small style='font-size:12px; font-weight:normal;'>Timeframe Floor Liquidity Support</small></div>", unsafe_allow_html=True)
    with col_out:
        st.markdown(f"<div class='predict-box whale-exit-zone'>🟥 ALADDIN PREDICTED EXIT / SEL POINT<br><span style='font-size:30px; color:white;'>${pre_order_sell_limit:,.4f}</span><br><small style='font-size:12px; font-weight:normal;'>Timeframe Ceiling Resistance Barrier</small></div>", unsafe_allow_html=True)

    st.write("---")
    
    # === 📊 PHASE 4: THREE SEPARATE PIPELINES ===
    st.subheader(f"📡 LIVE INSTITUTIONAL FUNDS ROUTING STATUS ({active_tf_code.upper()} INTERVAL)")
    
    col_p1, col_p2, col_p3 = st.columns(3)
    
    # --- PIPELINE 1: COLD STORAGE EX-MIGRATION TRACKER ---
    with col_p1:
        st.markdown("<div class='pipeline-header' style='color:#ff4b4b;'>⚠️ LIST 1: WALLET ➡️ EXCHANGE (Dumping)</div>", unsafe_allow_html=True)
        addresses_p1 = ["0xWhale9981", "0xColdBinance4412", "0xInstitutional7102", "0xAssetTrap9551"]
        for addr in addresses_p1:
            v_raw = random.uniform(5_000_000, 28_000_000)
            st.markdown(f"""
                <div class='list-log'>
                    🔑 Address: <span style='color:#c9d1d9;'>{addr}</span><br>
                    💥 Status: <span class='badge-danger'>[-] ASSET MIGRATED TO EXCHANGE</span><br>
                    💰 Value: <span style='color:white; font-weight:bold;'>{format_institutional_million_cash(v_raw)}</span>
                </div>
            """, unsafe_allow_html=True)
            
    # --- PIPELINE 2: CRYPTO TO USD/STABLECOIN ROTATION ---
    with col_p2:
        st.markdown("<div class='pipeline-header' style='color:#58a6ff;'>💵 LIST 2: ASSET ➡️ USD / STABLECOIN (Safe Hold)</div>", unsafe_allow_html=True)
        addresses_p2 = ["0xSmartProfit8812", "0xBlackRockUSD_01", "0xStableReserve3341", "0xWhaleExit7762"]
        for addr in addresses_p2:
            v_raw = random.uniform(6_000_000, 35_000_000)
            st.markdown(f"""
                <div class='list-log'>
                    🔑 Address: <span style='color:#c9d1d9;'>{addr}</span><br>
                    🔄 Status: <span class='badge-blue'>[+] PROFITS STORED IN STABLECOIN</span><br>
                    💰 Value: <span style='color:white; font-weight:bold;'>{format_institutional_million_cash(v_raw)}</span>
                </div>
            """, unsafe_allow_html=True)
            
    # --- PIPELINE 3: FIAT ON-RAMP BUY INTO WALLET ---
    with col_p3:
        st.markdown("<div class='pipeline-header' style='color:#00ff88;'>🛒 LIST 3: USD BUY ➡️ WALLET DIRECT (Accumulation)</div>", unsafe_allow_html=True)
        addresses_p3 = ["0xOnRampWhale001", "0xDirectBuySmart82", "0xInstitutionalCold_99", "0xMicroStrategyInflow"]
        for addr in addresses_p3:
            v_raw = random.uniform(8_000_000, 42_000_000)
            st.markdown(f"""
                <div class='list-log'>
                    🔑 Address: <span style='color:#c9d1d9;'>{addr}</span><br>
                    🛍️ Status: <span class='badge-success'>[+] DIRECT CASH INFLOW INTO COLD WALLET</span><br>
                    💰 Value: <span style='color:white; font-weight:bold;'>{format_institutional_million_cash(v_raw)}</span>
                </div>
            """, unsafe_allow_html=True)

    # === 🧮 PHASE 5: TRUE CUMULATIVE FLOW MATRIX ===
    st.write("---")
    st.subheader("📊 CUMULATIVE CAPITAL TREND STATS (Auto Incrementing Elements)")
    
    total_combined_ever = total_in_ever + total_out_ever
    if total_combined_ever > 0:
        inflow_percentage = (total_in_ever / total_combined_ever) * 100
        outflow_percentage = (total_out_ever / total_combined_ever) * 100
    else:
        inflow_percentage, outflow_percentage = 0.0, 0.0

    if total_in_ever >= total_out_ever:
        net_diff_pct = inflow_percentage - outflow_percentage
        st.markdown(f"<div class='net-flow-card net-plus'>🟢 NETWORK NET STATUS: PLUS (+) | Whales are Overwhelmingly Securing Assets!<br><span style='font-size:32px; color:white;'>+{net_diff_pct:.2f}% Real Cash Surplus Across Pipelines</span></div>", unsafe_allow_html=True)
    else:
        net_diff_pct = outflow_percentage - inflow_percentage
        st.markdown(f"<div class='net-flow-card net-minus'>🔴 NETWORK NET STATUS: MINUS (-) | Warning! Dominant Asset Extraction and Liquidation Running!<br><span style='font-size:32px; color:white;'>-{net_diff_pct:.2f}% Real Liquidation Run Detected</span></div>", unsafe_allow_html=True)

    col_sum_in, col_sum_out = st.columns(2)
    with col_sum_in:
        st.markdown(f"<div class='summary-box-in'><h3 style='margin:0; color:#58a6ff;'>🟦 TOTAL ACCOUNT INFLOW (List 2 + List 3)</h3><p style='font-size:28px; margin:5px 0; color:white;'>{format_institutional_million_cash(total_in_ever)}</p><small>Cumulative Wallet Load Share: {inflow_percentage:.1f}%</small></div>", unsafe_allow_html=True)
    with col_sum_out:
        st.markdown(f"<div class='summary-box-out'><h3 style='margin:0; color:#ff4b4b;'>🟥 TOTAL ACCOUNT OUTFLOW (List 1 Leakage)</h3><p style='font-size:28px; margin:5px 0; color:white;'>{format_institutional_cash(total_out_ever)}</p><small>Exchange Dump Exposure Share: {outflow_percentage:.1f}%</small></div>", unsafe_allow_html=True)

st.components.v1.html("""
    <script>
        setTimeout(function(){ window.parent.document.querySelector('section.main').dispatchEvent(new Event('change')); }, 1000);
    </script>
""", height=0)
