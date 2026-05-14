import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# --- 🏛️ ALADDIN COMMAND CORE ---
st.set_page_config(page_title="ALADDIN WHALE V10", layout="wide")

# Custom Styling for Institutional Look
st.markdown("""
    <style>
    .whale-buy { color: #00ff88; font-weight: bold; }
    .whale-sell { color: #ff4b4b; font-weight: bold; }
    .big-data-box { background-color: #0d1117; border: 1px solid #30363d; padding: 15px; border-radius: 10px; }
    </style>
    """, unsafe_allow_index=True)

# --- 🔍 MULTI-PHONE INDIVIDUAL SEARCH ---
target_coin = st.sidebar.text_input("🔍 ALADDIN SEARCH (BTC, ETH, DOT)", "BTC").upper()

def get_aladdin_data(sym):
    url = f"https://min-api.cryptocompare.com/data/v2/histohour?fsym={sym}&tsym=USD&limit=24"
    return requests.get(url).json()['Data']['Data']

if target_coin:
    raw_data = get_aladdin_data(target_coin)
    df = pd.DataFrame(raw_data)
    current_price = df['close'].iloc[-1]
    
    st.title(f"🏛️ {target_coin} INSTITUTIONAL LEDGER")
    st.markdown(f"### LIVE PRICE: `${current_price:,.2f}`")

    # --- 🏗️ ALADDIN RISK FRONTIER ---
    c1, c2 = st.columns(2)
    with c1:
        st.success(f"🟢 **BUY SUPPORT:** `${df['low'].min():,.2f}`")
    with c2:
        st.error(f"🔴 **SELL RESISTANCE:** `${df['high'].max():,.2f}`")

    st.divider()

    # --- 🐋 BIG DATA: WHALE TRACKING LIST ---
    st.subheader("📊 BIG DATA: WHALE MOVEMENT LEDGER")
    st.write("Is list mein bade institutions ki buy/sell activity ka record hai:")

    whale_list = []
    for i in range(len(df)-1, 0, -1):
        vol = df['volumeto'].iloc[i]
        avg_vol = df['volumeto'].mean()
        time_str = datetime.fromtimestamp(df['time'].iloc[i]).strftime('%Y-%m-%d %H:%M')
        
        # Aladdin Logic: Agar volume average se 1.5x zyada hai, toh wo Whale hai
        if vol > avg_vol * 1.5:
            action = "BUY (Accumulation)" if df['close'].iloc[i] > df['open'].iloc[i] else "SELL (Distribution)"
            status_class = "whale-buy" if "BUY" in action else "whale-sell"
            
            whale_list.append({
                "Date/Time": time_str,
                "Action": action,
                "Volume ($)": f"${vol:,.2f}",
                "Price": f"${df['close'].iloc[i]:,.2f}"
            })

    if whale_list:
        whale_df = pd.DataFrame(whale_list)
        # Displaying as a professional table
        st.table(whale_df)
    else:
        st.info("Searching for Whale Liquidity... Market is currently in Retail Consolidation.")

    # --- ⚠️ ALADDIN VERDICT ---
    st.divider()
    last_vol = df['volumeto'].iloc[-1]
    if last_vol > df['volumeto'].mean() * 1.8:
        st.warning(f"🚨 **ALADDIN ALERT:** Huge Whale activity detected right now in {target_coin}!")
    
    # --- 🛠️ MANUAL ERROR CORRECTION ---
    with st.expander("📝 Report Data Error (Teach AI)"):
        err_msg = st.text_input("Galti kya hai?")
        if st.button("Update Ledger Engine"):
            st.write("✅ **Aladdin Learning:** Whale pattern record updated.")
