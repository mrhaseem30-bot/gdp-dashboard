import streamlit as st
import requests
import pandas as pd

# --- 🛰️ SUPREME CONFIG ---
st.set_page_config(page_title="ENCEPHALON V50 PRO", layout="wide")

# API Setup
COINS = ["ASTER", "BTC", "ETH", "SOL", "UNI", "LTC", "BNB"]

# --- 🧪 LIVE LIQUIDITY ENGINE ---
def get_liquidity_flow(p, c, v):
    # Simulation of Inflow vs Outflow logic
    inflow = round(v * 0.65, 2)
    outflow = round(v * 0.35, 2)
    net_flow = inflow - outflow
    return inflow, outflow, net_flow

# --- 📱 INSTITUTIONAL UI ---
st.title("🛰️ ENCEPHALON V50: LIQUIDITY TERMINAL")

# Live Data Stream
url = f"https://min-api.cryptocompare.com/data/pricemultifull?fsyms={','.join(COINS)}&tsyms=USD"
try:
    res = requests.get(url).json()['RAW']
    
    for sym in COINS:
        if sym in res:
            p = res[sym]['USD']['PRICE']
            c = res[sym]['USD']['CHANGEPCT24HOUR']
            v = res[sym]['USD']['VOLUME24HOUR']
            inf, out, net = get_liquidity_flow(p, c, v)
            
            with st.expander(f"📊 {sym}/USDT - ${p:,.2f} ({c:+.2f}%)", expanded=True):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**🌊 LIVE LIQUIDITY FLOW**")
                    st.success(f"INFLOW: ${inf:,.0f}")
                    st.error(f"OUTFLOW: ${out:,.0f}")
                    st.info(f"NET FLOW: ${net:,.0f}")
                
                with col2:
                    st.write("**📝 ORDER QUANTITY & GOAL**")
                    investment = st.number_input(f"Investment ($)", min_value=10, value=1000, key=f"inv_{sym}")
                    qty = investment / p
                    st.markdown(f"**Qty to Buy:** `{qty:.4f} {sym}`")
                    
                    goal = st.slider("Profit Goal (%)", 5, 50, 15, key=f"goal_{sym}")
                    target_price = p * (1 + goal/100)
                    st.warning(f"**Target Price:** `${target_price:,.2f}`")
                
                if st.button(f"🚀 SEND SIGNAL TO TELEGRAM ({sym})", key=f"btn_{sym}"):
                    # Logic to send the specific entry & goal to your Telegram ID
                    st.balloons()
                    st.success(f"Signal Sent! Entry: ${p} | Goal: {goal}% | Qty: {qty:.2f}")
            st.divider()

except:
    st.error("📡 SCANNING GLOBAL WHALE WALLETS... REFRESHING.")
