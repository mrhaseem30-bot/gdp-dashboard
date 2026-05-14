import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go

from data_fetcher import DataFetcher
from smc_engine import SMCEngine
from ai_analyst import AIAnalyst

st.set_page_config(page_title="GDP Quantum Terminal V5", layout="wide")
st.title("🟢 GDP - H32 Quantum Terminal V5")
st.markdown("**Smart Money + AI Trading System**")

# Sidebar
st.sidebar.header("⚙️ Controls")
risk_percent = st.sidebar.slider("Risk % per Trade", 0.5, 3.0, 1.0)
selected_tf = st.sidebar.selectbox("Timeframe", ["15m", "1h", "4h", "1d"])

fetcher = DataFetcher()
smc = SMCEngine()
ai = AIAnalyst()

# Scanner
st.subheader("📡 Live Market Scanner")
coins = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT"]
results = []

for coin in coins:
    df = fetcher.get_ohlcv(coin, selected_tf, 150)
    if df is not None:
        df = smc.get_indicators(df)          # yahan pandas_ta nahi use hoga
        analysis = ai.analyze(df, [])
        
        results.append({
            "Coin": coin.replace("USDT", ""),
            "Price": f"${df['close'].iloc[-1]:,.2f}",
            "Signal": analysis["signal"],
            "Confidence": f"{analysis['confidence']}%"
        })

st.dataframe(pd.DataFrame(results), use_container_width=True)

# Chart
st.subheader("📈 BTCUSDT Live Chart")
df_btc = fetcher.get_ohlcv("BTCUSDT", selected_tf, 300)
if df_btc is not None:
    fig = go.Figure(data=[go.Candlestick(x=df_btc['time'],
                    open=df_btc['open'], high=df_btc['high'],
                    low=df_btc['low'], close=df_btc['close'])])
    st.plotly_chart(fig, use_container_width=True)

st.caption(f"Last Updated: {datetime.now().strftime('%I:%M %p')}")
