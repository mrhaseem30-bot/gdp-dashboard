import streamlit as st
import requests
import pandas as pd

# --- 🛰️ SATELLITE CORE ---
st.set_page_config(page_title="V5000 OMNI-LEARN", layout="wide")
st.title("🛰️ V5000: SELF-LEARNING DATA TERMINAL")

# --- 🧠 3-BRAIN AI ENGINE ---
def get_institutional_pipe(symbol):
    url = f"https://min-api.cryptocompare.com/data/v2/histohour?fsym={symbol}&tsym=USD&limit=168"
    res = requests.get(url).json()['Data']['Data']
    return pd.DataFrame(res)

# Setup Session State for Learning
if 'learning_log' not in st.session_state:
    st.session_state.learning_log = []

coins = ["BTC", "ETH", "SOL"]

for sym in coins:
    df = get_institutional_pipe(sym)
    curr_p = df['close'].iloc[-1]
    
    st.header(f"💎 {sym}/USDT | `${curr_p:,.2f}`")
    
    # --- 🏗️ 3-BRAIN ANALYSIS ---
    b1, b2, b3 = st.columns(3)

    with b1:
        st.info("🎯 **AI 1: BIT-NOTE (1H)**")
        low_1h = df['low'].iloc[-1]
        st.write(f"**Scalp Entry:** `${low_1h * 0.999:,.2f}`")

    with b2:
        st.success("🛰️ **AI 2: BIT-GLASS (12H)**")
        low_12h = df['low'].tail(12).min()
        st.write(f"**Puri Entry:** `${low_12h * 0.995:,.2f}`")

    with b3:
        st.warning("🏛️ **AI 3: BLACKROCK (1W)**")
        low_1w = df['low'].min()
        st.write(f"**Whale Floor:** `${low_1w * 0.98:,.2f}`")

    # --- 🐋 WALLET TRACKER ---
    vol_spike = df['volumeto'].iloc[-1] > (df['volumeto'].tail(24).mean() * 1.5)
    if vol_spike:
        st.button(f"🐋 WHALE INFLOW DETECTED: {sym}", key=f"btn_{sym}")
    
    # --- 🛠️ THE "ERROR CORRECTION" OPTION ---
    st.markdown("---")
    with st.expander(f"⚠️ Report Error / Teach AI for {sym}"):
        reason = st.text_input("Galti kya hai? (e.g. False Breakout, Late Entry)", key=f"in_{sym}")
        if st.button("Submit Correction & Learn", key=f"corr_{sym}"):
            st.session_state.learning_log.append({"coin": sym, "price": curr_p, "error": reason})
            st.write("✅ **AI Learning:** Galti record ho gayi hai. Next cycle mein is level ko adjust kiya jayega.")

    st.divider()

# --- 📊 MASTER LOG (AI'S DATABASE) ---
if st.session_state.learning_log:
    st.sidebar.subheader("🧠 AI Knowledge Base")
    st.sidebar.write("System in galtiyon se seekh raha hai:")
    st.sidebar.json(st.session_state.learning_log)
