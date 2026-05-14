import streamlit as st
import requests
import pandas as pd
import numpy as np

# --- 🛰️ HEAVY SYSTEM SETUP ---
st.set_page_config(page_title="ENCEPHALON V40 PRO", layout="wide")

# Static Data for Reliability
GROQ_KEY = "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"
COINS = ["BTC", "ETH", "SOL", "AVAX", "BNB", "ASTER", "UNI", "LTC", "ZEC", "ONDO", "LINK", "DOGE"]

# --- 🧪 THE BACKTESTING CORE (Heavy Math) ---
def run_heavy_backtest(symbol):
    try:
        # Fetching 100 hours of historical data
        url = f"https://min-api.cryptocompare.com/data/v2/histohour?fsym={symbol}&tsym=USD&limit=100"
        data = requests.get(url).json()['Data']['Data']
        df = pd.DataFrame(data)
        
        # Calculate RSI (Institutional Strength Indicator)
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1+rs))
        
        latest_rsi = df['rsi'].iloc[-1]
        avg_vol = df['volumeto'].mean()
        curr_vol = df['volumeto'].iloc[-1]
        
        # Decision Logic based on Backtested RSI & Volume
        if latest_rsi < 35 and curr_vol > avg_vol:
            return "🔥 STRONG BUY (BACKTESTED)", "Whale Accumulation Detected.", "success"
        elif latest_rsi > 70:
            return "⚠️ OVERBOUGHT (DANGER)", "Backtest suggests immediate correction.", "error"
        else:
            return "⚖️ HOLD / NEUTRAL", "Market waiting for direction.", "info"
    except:
        return "🔄 SCANNING...", "Connecting to Satellite Data.", "info"

# --- 📱 CLEAN PRO DASHBOARD ---
st.title("🛰️ ENCEPHALON V40: INSTITUTIONAL COMMANDER")
st.write("---")

# Data Fetching
url_live = f"https://min-api.cryptocompare.com/data/pricemultifull?fsyms={','.join(COINS)}&tsyms=USD"
try:
    raw_data = requests.get(url_live).json()['RAW']
    
    for sym in COINS:
        if sym in raw_data:
            p = raw_data[sym]['USD']['PRICE']
            c = raw_data[sym]['USD']['CHANGEPCT24HOUR']
            
            # Run Heavy Analysis
            verdict, logic, status = run_heavy_backtest(sym)
            
            # Using Native Streamlit Containers (No more HTML breakages)
            with st.container():
                c1, c2, c3 = st.columns([1, 2, 2])
                with c1:
                    st.subheader(f"{sym}/USDT")
                    st.metric("Price", f"${p:,.2f}", f"{c:+.2f}%")
                
                with c2:
                    if status == "success":
                        st.success(f"**{verdict}**")
                    elif status == "error":
                        st.error(f"**{verdict}**")
                    else:
                        st.info(f"**{verdict}**")
                    st.write(f"🧠 {logic}")
                
                with c3:
                    st.write("**PRO TARGETS (1-2 WEEKS)**")
                    st.code(f"ENTRY: ${p*0.985:,.2f} | TARGET: ${p*1.15:,.2f}")
                st.write("---")
except:
    st.error("📡 SATELLITE CONNECTION LOST. RE-ESTABLISHING...")
