import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# --- 🛰️ ALADDIN CORE SETUP ---
st.set_page_config(page_title="ALADDIN V14 MASTER", layout="wide")

# Institutional Black-Box Theme
st.markdown("""
    <style>
    .main { background-color: #010409; color: #f0f6fc; }
    .stMetric { border: 1px solid #30363d; background-color: #0d1117; border-radius: 12px; padding: 20px; }
    .buy-zone { background-color: #041910; border: 2px solid #00ff88; padding: 25px; border-radius: 12px; color: #00ff88; }
    .sell-zone { background-color: #220b0d; border: 2px solid #ff4b4b; padding: 25px; border-radius: 12px; color: #ff4b4b; }
    </style>
    """, unsafe_allow_html=True)

# --- 🧠 ALADDIN FORMATTING ENGINE ---
def format_big_number(num):
    if num >= 1_000_000_000:
        return f"{num / 1_000_000_000:.2f} B"
    elif num >= 1_000_000:
        return f"{num / 1_000_000:.2f} M"
    else:
        return f"{num:,.2f}"

def fetch_aladdin_data(symbol, timeframe, limit):
    try:
        endpoint = "histohour" if "h" in timeframe else "histoday"
        url = f"https://min-api.cryptocompare.com/data/v2/{endpoint}?fsym={symbol}&tsym=USD&limit={limit}"
        res = requests.get(url).json()
        return pd.DataFrame(res['Data']['Data'])
    except:
        return None

# --- 🔍 SIDEBAR: ACCOUNT LIST & TIMEFRAME ---
st.sidebar.title("🏛️ ALADDIN COMMAND")

asset_list = ["BTC", "ETH", "SOL", "SHIB", "BONE", "BNB", "XRP", "ADA", "DOT", "MATIC"]
selected_asset = st.sidebar.selectbox("📂 SELECT ASSET (Account List)", asset_list)

time_options = {
    "1 Hour (Scalp)": {"tf": "1h", "limit": 24},
    "12 Hours (Session)": {"tf": "1h", "limit": 120},
    "1 Day (Trend)": {"tf": "1d", "limit": 30},
    "1 Week (Whale Cycle)": {"tf": "1d", "limit": 90},
    "1 Month (Institutional)": {"tf": "1d", "limit": 365}
}
selected_tf_label = st.sidebar.radio("⏱️ SELECT TIMEFRAME", list(time_options.keys()))
config = time_options[selected_tf_label]

if selected_asset:
    df = fetch_aladdin_data(selected_asset, config['tf'], config['limit'])
    
    if df is not None:
        curr_price = df['close'].iloc[-1]
        
        st.title(f"🏛️ {selected_asset} RISK FRONTIER ({selected_tf_label})")
        st.markdown(f"### LIVE PRICE: `${format_big_number(curr_price)}`")
        st.write("---")

        # --- 🏗️ ALADDIN ANALYSIS (BUY/SELL/TARGET) ---
        support = df['low'].min()
        resistance = df['high'].max()
        target_proj = curr_price + (df['close'].std() * 1.5)

        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
                <div class='buy-zone'>
                    <h3 style='margin:0;'>🟢 WHALE BUY ENTRY</h3>
                    <h1 style='color:white; margin:10px 0;'>${format_big_number(support)}</h1>
                    <p style='color:#daffde; font-size:14px;'>Institutional Liquidity Point.</p>
                </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
                <div class='sell-zone'>
                    <h3 style='margin:0;'>🔴 ZED EXIT ZONE</h3>
                    <h1 style='color:white; margin:10px 0;'>${format_big_number(resistance)}</h1>
                    <p style='color:#ffdadb; font-size:14px;'>Retail Trap / Resistance Layer.</p>
                </div>
            """, unsafe_allow_html=True)

        # --- 📈 BIG DATA: WHALE LEDGER (Formatted) ---
        st.write("---")
        st.subheader("📊 BIG DATA: WHALE LEDGER (History)")
        
        whale_data = []
        avg_vol = df['volumeto'].mean()

        for i in range(len(df)-1, -1, -1):
            vol = df['volumeto'].iloc[i]
            if vol > avg_vol * 1.6:
                is_buy = df['close'].iloc[i] > df['open'].iloc[i]
                action = "🟩 BUY" if is_buy else "🟥 SELL"
                dt = datetime.fromtimestamp(df['time'].iloc[i]).strftime('%Y-%m-%d %H:%M')
                
                whale_data.append({
                    "Date & Time": dt,
                    "Action": action,
                    "Volume Amount": format_big_number(vol),
                    "Price ($)": format_big_number(df['close'].iloc[i])
                })

        if whale_data:
            st.table(pd.DataFrame(whale_data))
        else:
            st.info("Market is currently in low liquidity consolidation.")

    else:
        st.error("Aladdin Satellite connection failed.")
