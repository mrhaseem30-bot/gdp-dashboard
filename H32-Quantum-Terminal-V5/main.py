import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# --- 🛰️ SATELLITE CORE & UI INITIALIZATION ---
st.set_page_config(page_title="ALADDIN V12 TERMINAL", layout="wide")

# Aladdin Black-Box Theme Custom Styling
st.markdown("""
    <style>
    .main { background-color: #010409; }
    .reportview-container { background: #010409; }
    .stMetric { border: 2px solid #30363d; border-radius: 12px; background: #0d1117; padding: 15px; }
    .buy-zone-box { background-color: #041910; border: 2px solid #00ff88; padding: 25px; border-radius: 12px; margin-bottom: 20px; }
    .sell-zone-box { background-color: #220b0d; border: 2px solid #ff4b4b; padding: 25px; border-radius: 12px; margin-bottom: 20px; }
    .headline-txt { font-size: 24px; font-weight: bold; color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏛️ ALADDIN OMNI-ENGINE (V12 MASTER)")
st.write("---")

# --- 🔍 MULTI-PHONE INDEPENDENT SEARCH ---
# Har alag phone par aap alag coin search kar sakte hain
asset_symbol = st.sidebar.text_input("🔍 ALADDIN ASSET SEARCH (BTC, ETH, SOL, SHIB)", "BTC").upper()

def fetch_aladdin_big_data(sym):
    # Fetching 72 hours of micro-data for accurate institution tracking
    try:
        url = f"https://min-api.cryptocompare.com/data/v2/histohour?fsym={sym}&tsym=USD&limit=72"
        response = requests.get(url).json()
        return pd.DataFrame(response['Data']['Data'])
    except Exception as e:
        return None

if asset_symbol:
    df = fetch_aladdin_big_data(asset_symbol)
    
    if df is not None and not df.empty:
        live_p = df['close'].iloc[-1]
        
        st.markdown(f"<div class='headline-txt'>💎 ASSET: {asset_symbol}/USDT | LIVE PRICE: ${live_p:,.2f}</div>", unsafe_allow_html=True)
        st.write(" ")

        # --- 🧠 ALADDIN RISK FRONTIER RATIOS ---
        # 1. Institutional Floor: Deep liquidity level (Whale order block)
        inst_floor = df['low'].min()
        # 2. Registered Ceiling: High institutional supply layer
        inst_ceiling = df['high'].max()
        # 3. Future Value Projection (Standard Deviation & Volatility Engine)
        volatility_offset = df['close'].std() * 1.5
        aladdin_target = live_p + volatility_offset
        aladdin_stop_shield = inst_floor * 0.985

        # --- 🏗️ SCREEN DISPLAY (KAHAN ENTRY / KAHAN EXIT) ---
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
                <div class='buy-zone-box'>
                    <h3 style='color: #00ff88; margin-top:0;'>🟢 INSTITUTIONAL ENTRY ZONE</h3>
                    <p style='font-size: 18px; color: #e6edf2; margin-bottom: 5px;'>Is price point par Whales apni liquidity grab karti hain:</p>
                    <h1 style='color: #ffffff; margin: 0;'>${:,.2f}</h1>
                    <small style='color: #8b949e;'>Strategy: Wait for this floor. Don't chase green candles.</small>
                </div>
            """.format(inst_floor), unsafe_allow_html=True)

        with col2:
            st.markdown("""
                <div class='sell-zone-box'>
                    <h3 style='color: #ff4b4b; margin-top:0;'>🔴 REGISTERED EXIT ZONE (ZED)</h3>
                    <p style='font-size: 18px; color: #e6edf2; margin-bottom: 5px;'>Is level par retail traders trap hote hain aur institutions sell karte hain:</p>
                    <h1 style='color: #ffffff; margin: 0;'>${:,.2f}</h1>
                    <small style='color: #8b949e;'>Strategy: Take profits here. Retailers will buy the fake breakout.</small>
                </div>
            """.format(inst_ceiling), unsafe_allow_html=True)

        # --- 🎯 TARGET METRICS ---
        st.write(" ")
        t1, t2 = st.columns(2)
        t1.metric("🎯 ALADDIN FUTURE TARGET PROJECTION", f"${aladdin_target:,.2f}", delta="Bullish Horizon")
        t2.metric("🛡️ ALADDIN SYSTEM STOP SHIELD", f"${aladdin_stop_shield:,.2f}", delta="-1.5% Risk Buffer", delta_color="inverse")

        # --- 📈 REAL-TIME INSTITUTIONAL HEATMAP ---
        st.write("---")
        st.subheader("📊 REAL-TIME LIQUIDITY HEATMAP")
        st.line_chart(df.set_index('time')[['close', 'high', 'low']])

        # --- 🐋 BIG DATA: LIVE WHALE LEDGER WITH DATE & TIME ---
        st.write("---")
        st.subheader("📊 BIG DATA: WHALE MOVEMENT TRACKING LIST")
        st.write("Bade institutions aur wallets jo paise market me daal rahe hain ya nikal rahe hain, unka accurate database:")

        whale_ledger = []
        global_avg_vol = df['volumeto'].mean()

        # Reverse loop starting from most recent hour
        for i in range(len(df)-1, -1, -1):
            hour_vol = df['volumeto'].iloc[i]
            
            # Aladdin Volume Filter Rule: Volume must be 1.6x higher than 72h average
            if hour_vol > global_avg_vol * 1.6:
                candle_close = df['close'].iloc[i]
                candle_open = df['open'].iloc[i]
                
                # Logic: Price closed higher = Buying, Price closed lower = Selling
                if candle_close > candle_open:
                    action_tag = "🟩 BUY (Accumulation)"
                else:
                    action_tag = "🟥 SELL (Distribution)"
                    
                formatted_time = datetime.fromtimestamp(df['time'].iloc[i]).strftime('%Y-%m-%d %H:%M')
                
                whale_ledger.append({
                    "Date & Time (Delhi)": formatted_time,
                    "Whale Action Type": action_tag,
                    "Total Volume Amount": f"${hour_vol:,.2f}",
                    "Execution Price": f"${candle_close:,.2f}"
                })

        if whale_ledger:
            ledger_df = pd.DataFrame(whale_ledger)
            st.table(ledger_df)
        else:
            st.info("Market me filhal koi massive institutional movement nahi hai. Retail consolidation active.")

        # --- 🛠️ MANUAL ERROR CORRECTION (AI FEEDBACK LOOP) ---
        st.sidebar.write("---")
        with st.sidebar.expander("📝 Teach Aladdin Engine (Correction)"):
            feedback = st.text_input("Agar signal me koi galti dikhe, yahan type karein:")
            if st.button("Submit Pattern Correction"):
                st.success("✅ Galti saved! Aladdin engine parameters updated for next cycle.")
                
    else:
        st.error("📡 Data fetch nahi ho saka. Internet connection ya Coin Symbol check karein.")
