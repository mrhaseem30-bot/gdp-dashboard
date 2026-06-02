import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import talib

st.set_page_config(page_title="H32 Compound Trend Bot", layout="wide")

# Custom CSS for glowing effect
st.markdown("""
<style>
    .big-signal {
        font-size: 32px !important;
        font-weight: bold;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 0 15px;
    }
    .buy { color: #00ff00; text-shadow: 0 0 10px #00ff00; }
    .sell { color: #ff0000; text-shadow: 0 0 10px #ff0000; }
    .wait { color: #ffa500; text-shadow: 0 0 8px #ffa500; }
</style>
""", unsafe_allow_html=True)

st.title("⚡ H32 Compound Trend Bot")
st.subheader("SuperTrend + EMA Smart Strategy")

# Coin Selector
coins = {
    "Bitcoin (BTC)": "BTC-USD",
    "Ethereum (ETH)": "ETH-USD",
    "Solana (SOL)": "SOL-USD",
    "Sui (SUI)": "SUI-USD",
    "Chainlink (LINK)": "LINK-USD"
}

selected_coin = st.selectbox("**Select Coin**", list(coins.keys()))
ticker = coins[selected_coin]

# Timeframe Selector (Bahut options)
timeframe = st.selectbox("**Select Timeframe**", 
    ["15 Minutes", "1 Hour", "4 Hours", "Daily"], index=1)

# Settings according to timeframe
if timeframe == "15 Minutes":
    period, multiplier, data_period, interval = 10, 2.5, "2d", "15m"
elif timeframe == "1 Hour":
    period, multiplier, data_period, interval = 10, 3.0, "15d", "1h"
elif timeframe == "4 Hours":
    period, multiplier, data_period, interval = 11, 3.0, "30d", "4h"
else:  # Daily
    period, multiplier, data_period, interval = 10, 3.0, "90d", "1d"

@st.cache_data(ttl=60)
def get_data(ticker, data_period, interval):
    return yf.download(ticker, period=data_period, interval=interval)

try:
    df = get_data(ticker, data_period, interval)

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    live_price = float(df['Close'].iloc[-1])

    # Indicators
    df['EMA20'] = talib.EMA(df['Close'], timeperiod=20)
    df['EMA50'] = talib.EMA(df['Close'], timeperiod=50)

    hl2 = (df['High'] + df['Low']) / 2
    atr = talib.ATR(df['High'], df['Low'], df['Close'], timeperiod=period)
    df['SuperTrend'] = hl2 + (multiplier * atr)

    # Signal Logic
    last = df.iloc[-1]
    ema_bull = last['EMA20'] > last['EMA50']
    price_above_st = live_price > last['SuperTrend']

    if ema_bull and price_above_st:
        signal = "🟢 STRONG BUY"
        css_class = "buy"
        reason = "EMA Bullish + Price above SuperTrend = Strong Uptrend"
        entry = f"Entry Zone: ${live_price:,.4f} - ${live_price*1.008:,.4f}"
    elif not ema_bull and not price_above_st:
        signal = "🔴 STRONG SELL"
