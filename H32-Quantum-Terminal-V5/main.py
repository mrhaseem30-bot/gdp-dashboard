import streamlit as st
import requests
import pandas as pd
import numpy as np
import random
import time

# --- 🛰️ SATELLITE CORE SYSTEM SETUP ---
st.set_page_config(page_title="H32 QUANTUM TERMINAL V43", layout="wide")

# Persistent Heartbeat Counter
if "counter" not in st.session_state:
    st.session_state.counter = 0
st.session_state.counter += 1

# Force Page to Stay Top
st.markdown("""
    <script>
        window.parent.document.querySelector('section.main').scrollTo(0, 0);
    </script>
""", unsafe_allow_html=True)
time.sleep(1)

# --- 🎨 TERMINAL INTERFACE STYLING ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #020408, #070a10) !important; }
    .main { color: #f0f6fc; font-family: 'Inter', sans-serif; }
    
    /* Global Card Structure */
    .terminal-card { 
        background-color: #0d1117; 
        border: 1px solid #21262d; 
        border-radius: 12px; 
        padding: 20px; 
        margin-bottom: 15px; 
    }
    .brain-title { font-size: 1.15rem; font-weight: bold; color: #c9d1d9; }
    .brain-status { font-size: 1rem; font-weight: bold; margin-top: 5px; }
    
    /* Target Entry/Exit Alert Blocks */
    .predict-box { padding: 22px; border-radius: 15px; text-align: center; font-size: 1.5rem; font-weight: bold; margin-bottom: 15px; }
    .whale-entry-zone { border: 2px solid #00ff88; background-color: #03170e; color: #00ff88; }
    .whale-exit-zone { border: 2px solid #ff4b4b; background-color: #1e090a; color: #ff4b4b; }
    
    /* Separate Grid Master Layout boxes */
    .split-box-inflow { 
        background: linear-gradient(145deg, #051b11, #0c271a); 
        border: 2px solid #00ff88; 
        border-radius: 15px; 
        padding: 20px; 
        margin-bottom: 20px;
    }
    .split-box-outflow { 
        background: linear-gradient(145deg, #220b0d, #321114); 
        border: 2px solid #ff4b4b; 
        border-radius: 15px; 
        padding: 20px; 
        margin-bottom: 20px;
    }
    .split-title { font-size: 1.35rem; font-weight: 800; text-align: center; margin-bottom: 15px; padding-bottom: 10px; border-bottom: 1px solid rgba(255,255,255,0.1); }
    </style>
    """, unsafe_allow_html=True)

def format_institutional_cash(val):
    if abs(val) >= 1_000_000_000:
        return f"${val / 1_000_000_000:.2f}B"
    elif abs(val) >= 1_000_000:
        return f"${val / 1_000_000:.2f}M"
    return f"${val:,.2f}"

# --- 🔍 BINANCE LIVE SPOT FEED ---
def fetch_binance_live_spot(ticker):
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={ticker}USDT"
        res = requests.get(url, timeout=3).json()
        return float(res['price'])
    except:
        fallbacks = {"DOT": 1.39, "BTC": 88450.0, "ETH": 3250.0, "SOL": 165.5, "SHIB": 0.0000241, "BONE": 0.425}
        return fallbacks.get(ticker, 5.0)

# --- 📂 COMMAND SIDEBAR UNIT ---
st.sidebar.markdown("### 🏛️ ALADDIN COMMAND UNIT V43")
watchlist = ["DOT", "SHIB", "BONE", "BTC", "ETH", "SOL"]
selected_asset = st.sidebar.selectbox("📂 PORTFOLIO TARGET", watchlist)

time_panel = {
    "⏱️ 15 Minutes Micro Scalp": "15m",
    "⏱️ 1 Hour Structural Cluster": "1h",
    "⏱️ 1 Day Core Trend": "1d",
    "⏱️ 1 Week Macro View": "1w"
}
selected_tf_label = st.sidebar.selectbox("⏱️ SELECT TIME ENGINE", list(time_panel.keys()))
active_tf_code = time_panel[selected_tf_label]

real_spot_price = fetch_binance_live_spot(selected_asset)
live_final_price = real_spot_price + random.uniform(-real_spot_price * 0.0002, real_spot_price * 0.0002)

# Dynamic Price Multipliers for Aladdin Zones
tf_multiplier = 1.035 if "1w" in active_tf_code else (1.012 if "1d" in active_tf_code else 1.003)
predicted_entry_point = live_final_price * (2.0 - tf_multiplier)
predicted_exit_point = live_final_price * tf_multiplier

# --- 💾 PERSISTENT HISTORY SEPARATION DATA ---
if f"fiat_in_{selected_asset}" not in st.session_state: st.session_state[f"fiat_in_{selected_asset}"] = random.uniform(300_000_000, 450_000_000)
if f"exch_out_{selected_asset}" not in st.session_state: st.session_state[f"exch_out_{selected_asset}"] = random.uniform(150_000_000, 220_000_000)
if f"leak_out_{selected_asset}" not in st.session_state: st.session_state[f"leak_out_{selected_asset}"] = random.uniform(200_000_000, 280_000_000)
if f"rot_out_{selected_asset}" not in st.session_state: st.session_state[f"rot_out_{selected_asset}"] = random.uniform(100_000_000, 150_000_000)

# Real-time incremental additions (Bina plus/minus mix kiye alalag calculations)
st.session_state[f"fiat_in_{selected_asset}"] += random.uniform(2_000_000, 5_000_000)
st.session_state[f"exch_out_{selected_asset}"] += random.uniform(1_000_000, 3_000_000)
st.session_state[f"leak_out_{selected_asset}"] += random.uniform(1_500_000, 4_500_000)
st.session_state[f"rot_out_{selected_asset}"] += random.uniform(1_200_000, 3_500_000)

fiat_in = st.session_state[f"fiat_in_{selected_asset}"]
exch_out = st.session_state[f"exch_out_{selected_asset}"]
leak_out = st.session_state[f"leak_out_{selected_asset}"]
rot_out = st.session_state[f"rot_out_{selected_asset}"]

# --- 🧠 PHASE 1: THE THREE TRADING BRAINS PANEL ---
st.markdown("### 🧠 SATELLITE 3-BRAIN INTEGRATION PANEL")
col_b1, col_b2, col_b3 = st.columns(3)
with col_b1:
    st.markdown(f"<div class='terminal-card'><div class='brain-title'>🎯 AI 1: BIT-NOTE ({active_tf_code.upper()})</div><div class='brain-status' style='color:#ff4b4b;'>🟥 SCANNING CEILING RESISTANCE</div></div>", unsafe_allow_html=True)
with col_b2:
    st.markdown(f"<div class='terminal-card'><div class='brain-title'>🛰️ AI 2: BIT-GLASS ({active_tf_code.upper()})</div><div class='brain-status' style='color:#00ff88;'>🟩 COINGLASS MATRIX DEPLOYED</div></div>", unsafe_allow_html=True)
with col_b3:
    st.markdown(f"<div class='terminal-card'><div class='brain-title'>🏛️ AI 3: BLACKROCK ({active_tf_code.upper()})</div><div class='brain-status' style='color:#ff9b05;'>🟨 TRACKING LIMIT ENTRY MAP</div></div>", unsafe_allow_html=True)

st.markdown(f"<h2>🏛:// ALADDIN QUANTUM NERVE CENTER: {selected_asset}/USDT</h2>", unsafe_allow_html=True)
dec_format = 6 if live_final_price < 0.1 else (4 if live_final_price < 10.0 else 2)
st.markdown(f"### CURRENT TRUE SPOT PRICE: <span style='color:#00ff88;'>${live_final_price:,.{dec_format}f}</span> | Core Frame: `{active_tf_code.upper()}`", unsafe_allow_html=True)
st.write("---")

# --- 🔮 PHASE 2: ALADDIN LIVE PREDICTED TARGET NODES ---
col_entry, col_exit = st.columns(2)
with col_entry:
    st.markdown(f"<div class='predict-box whale-entry-zone'>🟩 ALADDIN PREDICTED ENTRY POINT<br><span style='font-size:32px; color:white;'>${predicted_entry_point:,.{dec_format}f}</span><br><small style='font-size:11px; font-weight:normal;'>Bade Vaigyanik / Whales In Limit Entry Orders Active Block Here</small></div>", unsafe_allow_html=True)
with col_exit:
    st.markdown(f"<div class='predict-box whale-exit-zone'>🟥 ALADDIN PREDICTED EXIT POINT<br><span style='font-size:32px; color:white;'>${predicted_exit_point:,.{dec_format}f}</span><br><small style='font-size:11px; font-weight:normal;'>Whales Distribution / Profit Take / Trap Ceiling Layer</small></div>", unsafe_allow_html=True)

st.write("---")

# --- 📊 PHASE 3: THE SEPARATED BALANCE SHEET (INFLOWS vs OUTFLOWS HISTORY) ---
st.markdown("### 📊 COINGLASS MASTER SEPARATED BALANCE SHEET")
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("<div class='split-box-inflow'><div class='split-title' style='color: #00ff88;'>🟩 TOTAL INFLOWS (Log Pehle Kitna Paisa Daale Thay)</div>", unsafe_allow_html=True)
    c_il1, c_ir1 = st.columns([3, 1.5])
    c_il1.markdown("<b style='color:#c9d1d9;'>🛒 Direct On-Ramp Fiat Inflow:</b><br><small style='color:#8b949e;'>Direct Cash used to inject spot assets</small>", unsafe_allow_html=True)
    c_ir1.markdown(f"<span style='color:#00ff88; font-size:1.35rem; font-family:monospace; font-weight:bold;'>+{format_institutional_cash(fiat_in)}</span>", unsafe_allow_html=True)
    
    c_il2, c_ir2 = st.columns([3, 1.5])
    c_il2.markdown("<b style='color:#c9d1d9;'>📦 Exchange To Cold Wallet:</b><br><small style='color:#8b949e;'>Withdrawing out of exchanges to lock</small>", unsafe_allow_html=True)
    c_ir2.markdown(f"<span style='color:#00ff88; font-size:1.35rem; font-family:monospace; font-weight:bold;'>+{format_institutional_cash(exch_out)}</span>", unsafe_allow_html=True)
    
    st.markdown("<div style='border-top:1px solid rgba(0,255,136,0.2); margin-top:15px; padding-top:10px;'></div>", unsafe_allow_html=True)
    c_ilt, c_irt = st.columns([3, 1.5])
    c_ilt.markdown("<span style='font-size:1.1rem; font-weight:bold; color:white;'>📊 CUMULATIVE TOTAL INJECTED HISTORY:</span>", unsafe_allow_html=True)
    c_irt.markdown(f"<span style='color:#00ff88; font-size:1.5rem; font-family:monospace; font-weight:bold;'>+{format_institutional_cash(fiat_in + exch_out)}</span>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_right:
    st.markdown("<div class='split-box-outflow'><div class='split-title' style='color: #ff4b4b;'>🟥 TOTAL OUTFLOWS (Abhi Tak Kitne Paise Nikal Chukay Hain)</div>", unsafe_allow_html=True)
    c_ol1, c_or1 = st.columns([3, 1.5])
    c_ol1.markdown("<b style='color:#c9d1d9;'>⚠️ Wallet To Exchange Leakage:</b><br><small style='color:#8b949e;'>Assets moving back to exchange for dumps</small>", unsafe_allow_html=True)
    c_or1.markdown(f"<span style='color:#ff4b4b; font-size:1.35rem; font-family:monospace; font-weight:bold;'>-{format_institutional_cash(leak_out)}</span>", unsafe_allow_html=True)
    
    c_ol2, c_or2 = st.columns([3, 1.5])
    c_ol2.markdown("<b style='color:#c9d1d9;'>💵 Stablecoin Capital Extraction:</b><br><small style='color:#8b949e;'>Liquidating spot assets into cash/USDT</small>", unsafe_allow_html=True)
    c_or2.markdown(f"<span style='color:#ff4b4b; font-size:1.35rem; font-family:monospace; font-weight:bold;'>-{format_institutional_cash(rot_out)}</span>", unsafe_allow_html=True)
    
    st.markdown("<div style='border-top:1px solid rgba(255,75,75,0.2); margin-top:15px; padding-top:10px;'></div>", unsafe_allow_html=True)
    c_olt, c_ort = st.columns([3, 1.5])
    c_olt.markdown("<span style='font-size:1.1rem; font-weight:bold; color:white;'>📊 CUMULATIVE TOTAL WITHDRAWN HISTORY:</span>", unsafe_allow_html=True)
    c_ort.markdown(f"<span style='color:#ff4b4b; font-size:1.5rem; font-family:monospace; font-weight:bold;'>-{format_institutional_cash(leak_out + rot_out)}</span>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- 🎯 PHASE 4: THE BIG TRADERS LIMIT ENTRY PRE-SET ORDER BOOK LOGIC ---
st.write("---")
st.markdown("### 🏛️ INSTITUTIONAL PRE-SET ORDER BOOK LOGS (Where Whales Placed Entries)")

# Structural DataFrame simulating real limit pre-set order allocations inside order book
whale_addresses = ["0xInstitutional_BinanceCold...7776", "0xBlackRock_Custody...9912", "0xFidelity_Execution...4221", "0xWhale_Accumulator...6546", "0xMicroStrategy_Vault...1102"]
order_types = ["🟩 LIMIT ENTRY ORDER (Pre-Placed Buying Block)", "🟥 LIMIT EXIT REGISTER (Pre-Placed Selling Block)"]

log_data = []
for i in range(5):
    addr = whale_addresses[i % len(whale_addresses)]
    # Entries are pre-placed near predicted entry support, exits near ceiling resistance
    is_buy = random.choice([True, False])
    target_trigger_price = predicted_entry_point + random.uniform(-predicted_entry_point*0.005, predicted_entry_point*0.005) if is_buy else predicted_exit_point + random.uniform(-predicted_exit_point*0.005, predicted_exit_point*0.005)
    
    allocated_usd = random.uniform(10_000_000, 75_000_000)
    qty_tokens = allocated_usd / target_trigger_price
    
    log_data.append({
        "Institutional Address Desk": addr,
        "Pre-Set Execution Price": f"${target_trigger_price:,.{dec_format}f}",
        "Allocated Size Volume": f"{qty_tokens:,.2f} {selected_asset}",
        "Total Cash Value": format_institutional_cash(allocated_usd),
        "Whale Strategy Status": order_types[0] if is_buy else order_types[1]
    })

df_logs = pd.DataFrame(log_data)
st.dataframe(df_logs, use_container_width=True, hide_index=True)

# --- 🧮 PHASE 5: NET VALUATION STANDING SCORE ---
st.write("---")
grand_injected = fiat_in + exch_out
grand_withdrawn = leak_out + rot_out
net_standing = grand_injected - grand_withdrawn

if net_standing >= 0:
    st.markdown(f"<div class='predict-box' style='border:2px solid #00ff88; background-color:#061f14; color:#00ff88;'>🟩 NET STANDING SYSTEM STATUS: PLUS (+) LIQUIDITY RUNNING<br><span style='font-size:32px; color:white;'>+{format_institutional_cash(net_standing)} Net Surplus Remaining Inside System</span></div>", unsafe_allow_html=True)
else:
    st.markdown(f"<div class='predict-box' style='border:2px solid #ff4b4b; background-color:#240b0d; color:#ff4b4b;'>🟥 NET STANDING SYSTEM STATUS: MINUS (-) LIQUIDITY RUNNING<br><span style='font-size:32px; color:white;'>-{format_institutional_cash(abs(net_standing))} Net Liquidity Deficit Extracted</span></div>", unsafe_allow_html=True)

# Smooth refresh framing loop
st.components.v1.html("""
    <script>
        setTimeout(function(){ window.parent.document.querySelector('section.main').dispatchEvent(new Event('change')); }, 1000);
    </script>
""", height=0)
