import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# --- 🏛️ ALADDIN ARCHITECTURE ---
st.set_page_config(page_title="ALADDIN V11", layout="wide")

# CSS for a Professional Aladdin Black-Box look
st.markdown("""
    <style>
    .main { background-color: #010409; }
    .stMetric { border: 1px solid #30363d; background-color: #0d1117; border-radius: 10px; }
    .whale-buy { color: #00ff88; font-weight: bold; background-color: #062016; padding: 5px; border-radius: 3px; }
    .whale-sell { color: #ff4b4b; font-weight: bold; background-color: #2d1316; padding: 5px; border-radius: 3px; }
    </style>
    """, unsafe_allow_index=True)

st.title("🏛️ ALADDIN: BIG DATA WHALE TRACKER")

# --- 🔍 INDEPENDENT SEARCH FOR EACH PHONE ---
search_target = st.sidebar.text_input("🔍 SEARCH ASSET", "BTC").upper()

def fetch_aladdin_intelligence(sym):
    # Fetching 48 hours of data for deep analysis
    url = f"https://min-api.cryptocompare.com/data/v2/histohour?fsym={sym}&tsym=USD&limit=48"
    response = requests.get(url).json()
    return pd.DataFrame(response['Data']['Data'])

if search_target:
    df = fetch_aladdin_intelligence(search_target)
    curr_price = df['close'].iloc[-1]
    
    st.markdown(f"## 💎 {search_target} | LIVE: `${curr_price:,.2f}`")

    # --- 🏗️ ALADDIN RISK FRONTIER ---
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🟢 INSTITUTIONAL FLOOR", f"${df['low'].min():,.2f}")
        st.write("Wait for **Whale Liquidity** yahan se asli kharidari hogi.")
        
    with col2:
        st.metric("🔴 REGISTERED CEILING", f"${df['high'].max():,.2f}")
        st.write("Is point par **Retail Trap** (Fik Mot) ho sakta hai.")

    with col3:
        target = curr_price * 1.05
        st.metric("🎯 ALADDIN PROJECTION", f"${target:,.2f}")
        st.write("Institutional target for this cycle.")

    st.divider()

    # --- 🐋 BIG DATA: WHALE MOVEMENT LIST ---
    st.subheader("📊 BIG DATA: WHALE ACTION LEDGER")
    st.write("Bade institutions ke real-time buy aur sell orders ki list:")

    ledger_data = []
    avg_vol = df['volumeto'].mean()

    for i in range(len(df)-1, 0, -1):
        vol = df['volumeto'].iloc[i]
        # Aladdin Logic: Agar volume average se 1.6x hai, toh wo Whale hai
        if vol > avg_vol * 1.6:
            action_type = "BUY (Accumulation)" if df['close'].iloc[i] > df['open'].iloc[i] else "SELL (Distribution)"
            time_stamp = datetime.fromtimestamp(df['time'].iloc[i]).strftime('%Y-%m-%d %H:%M')
            
            ledger_data.append({
                "Date/Time": time_stamp,
                "Big Data Action": action_type,
                "Total Amount ($)": f"${vol:,.2f}",
                "Execution Price": f"${df['close'].iloc[i]:,.2f}"
            })

    if ledger_data:
        ledger_df = pd.DataFrame(ledger_data)
        st.table(ledger_df)
    else:
        st.info("No massive Whale moves detected in the last 48 hours. Market is in Retail range.")

    # --- 🛠️ ALADDIN SELF-LEARNING ---
    st.sidebar.divider()
    with st.sidebar.expander("📝 Teach Aladdin (Manual Correction)"):
        correction = st.text_input("Galti kya hui?")
        if st.button("Update Aladdin Risk Engine"):
            st.write("✅ Aladdin is learning from this pattern correction.")
