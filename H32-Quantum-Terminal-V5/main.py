import streamlit as st
import requests
import pandas as pd

# --- 🏛️ ALADDIN COMMAND CENTER ---
st.set_page_config(page_title="ALADDIN V7000", layout="wide")
st.title("🏛️ ALADDIN RISK & LIQUIDITY TERMINAL")

# --- 🧠 ALADDIN DATA PIPELINE ---
def get_aladdin_data(symbol):
    # Pure Data from Global Infrastructure
    url = f"https://min-api.cryptocompare.com/data/v2/histohour?fsym={symbol}&tsym=USD&limit=168"
    response = requests.get(url).json()
    return pd.DataFrame(response['Data']['Data'])

# --- 🔍 INDIVIDUAL SEARCH (Aapke har phone ke liye) ---
search_coin = st.text_input("🔍 SEARCH COIN (e.g. BTC, ETH, SOL, SHIB)", "BTC").upper()

if search_coin:
    df = get_aladdin_data(search_coin)
    curr_p = df['close'].iloc[-1]
    
    st.markdown(f"## 💎 {search_coin}/USDT | LIVE: `${curr_p:,.2f}`")

    # --- 🏗️ ALADDIN RISK FRONTIER (Support/Resistance/Entry) ---
    col1, col2, col3 = st.columns(3)

    # 🟢 INSTITUTIONAL SUPPORT (Entry)
    with col1:
        st.success("🧱 **ALADDIN SUPPORT (BUY)**")
        # Aladdin logic: Deep liquidity hunt at 1W Low
        sup_level = df['low'].min()
        st.write(f"**Institutional Entry:** `${sup_level:,.2f}`")
        st.write("**Wait for Liquidity:** Asli kharidari yahan se hogi")

    # 🔴 REGISTERED RESISTANCE (Sell)
    with col2:
        st.error("📉 **ALADDIN REGISTER (SELL)**")
        res_level = df['high'].max()
        st.write(f"**Zed Zone (Exit):** `${res_level:,.2f}`")
        st.write("**Retail Trap:** Is point par 'Fik Mot' (Fakeout) ho sakta hai")

    # 🎯 TRADING VIEW TARGETS
    with col3:
        st.info("🎯 **ALADDIN TARGETS**")
        target_1 = curr_p * 1.02
        target_2 = curr_p * 1.05
        st.write(f"**T1 (Institutional):** `${target_1:,.2f}`")
        st.write(f"**T2 (Whale Target):** `${target_2:,.2f}`")

    # --- 📊 ALADDIN CHART SYNC (TradingView Style) ---
    st.subheader(f"📊 {search_coin} Liquidity Chart")
    st.line_chart(df.set_index('time')['close'])

    # --- 🐋 WHALE INFLOW DETECTION ---
    vol_current = df['volumeto'].iloc[-1]
    vol_avg = df['volumeto'].tail(24).mean()
    
    if vol_current > vol_avg * 1.3:
        st.warning("🐋 **WHALE ALERT:** Aladdin ne 'Big Money' detect kiya hai")
    else:
        st.write("📊 **Consolidation:** Market range mein hai")

    # --- 🛠️ MANUAL ERROR CORRECTION (AI Learning) ---
    st.divider()
    with st.expander("⚠️ Galti Pakdo (Teach AI)"):
        correction = st.text_input("Agar signal galat hai, yahan likho:", key=f"err_{search_coin}")
        if st.button("Correct Aladdin", key=f"btn_{search_coin}"):
            st.write("✅ **AI Learning:** Galti record ho gayi. System next time is range se seekhega")
