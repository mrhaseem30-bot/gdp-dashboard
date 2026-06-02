import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import talib

st.set_page_config(page_title="H32 Compound Trend Bot", layout="wide")

st.title("⚡ H32 Compound Trend Bot")
st.subheader("SuperTrend + EMA Strategy")

coins = {
    "Bitcoin (BTC)": "BTC-USD",
    "Ethereum (ETH)": "ETH-USD",
    "Solana (SOL)": "SOL-USD",
    "Sui (SUI)": "SUI-USD",
    "Chainlink (LINK)": "LINK-USD"
}

selected_coin = st.selectbox("Select Coin", list(coins.keys()))
ticker = coins[selected_coin]

st.sidebar.header("Settings")
period = st.sidebar.slider("SuperTrend Period", 7, 20, 10)
multiplier = st.sidebar.slider("Multiplier", 1.0, 5.0, 3.0)

@st.cache_data(ttl=60)
def get_data(ticker):
    df_15m = yf.download(ticker, period="3d", interval="15m")
    df_1h = yf.download(ticker, period="15d", interval="1h")
    return df_15m, df_1h

try:
    df_15m, df_1h = get_data(ticker)

    for df in [df_15m, df_1h]:
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

    live_price = float(df_15m['Close'].iloc[-1])

    # EMA
    df_1h['EMA20'] = talib.EMA(df_1h['Close'], timeperiod=20)
    df_1h['EMA50'] = talib.EMA(df_1h['Close'], timeperiod=50)

    # Simple SuperTrend Logic (Manual - kyuki ta-lib mein nahi hai)
    hl2 = (df_1h['High'] + df_1h['Low']) / 2
    atr = talib.ATR(df_1h['High'], df_1h['Low'], df_1h['Close'], timeperiod=period)
    upper = hl2 + (multiplier * atr)
    lower = hl2 - (multiplier * atr)

    df_1h['SuperTrend'] = upper  # Basic version

    # Signal
    last = df_1h.iloc[-1]
    signal = "🟢 STRONG BUY" if (last['EMA20'] > last['EMA50']) else "🔴 STRONG SELL" if (last['EMA20'] < last['EMA50']) else "⭕ WAIT"
    color = "lime" if "BUY" in signal else "red" if "SELL" in signal else "orange"
