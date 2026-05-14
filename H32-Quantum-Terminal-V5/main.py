import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go   # ← Yeh sahi kiya hai

from data_fetcher import DataFetcher
from smc_engine import SMCEngine
from ai_analyst import AIAnalyst
from risk_manager import RiskManager
import config

st.set_page_config(page_title="GDP Quantum Terminal V5", layout="wide")
st.title("🟢 GDP - H32 Quantum Terminal V5")
st.markdown("**Pura Trading Computer | Smart Money + AI + Global Data**")

# Sidebar Controls
st.sidebar.header("⚙️ Controls")
account_balance = st.sidebar.number_input("Account Balance (USDT)", value=1000.0)
risk_percent = st.sidebar.slider("Risk % per Trade", 0.5, 3.0, config.CONFIG["risk_percent"])
selected_tf = st.sidebar.selectbox("Timeframe", config.CONFIG["timeframes"])

fetcher = DataFetcher()
smc = SMCEngine()
ai = AIAnalyst()

# Live Scanner
st.subheader("📡 Global Market Scanner")
coins = config.CONFIG["watchlist"]
results = []

for coin in coins:
    df = fetcher.get_ohlcv(coin, selected_tf, 200)
    if df is not None:
        df = smc.get_indicators(df)
        obs = smc.detect_order_blocks(df)
        analysis = ai.analyze(df, obs)
        
        results.append({
            "Coin": coin.replace("USDT", ""),
            "Price": f"${df['close'].iloc[-1]:,.4f}",
            "Signal": analysis["signal"],
            "Conf": f"{analysis['confidence']}%",
            "Structure": smc.detect_structure(df)
        })

st.dataframe(pd.DataFrame(results), use_container_width=True, height=500)

# Signals & Psychology
col1, col2 = st.columns(2)
with col1:
    st.subheader("🚨 Active Signals")
    for r in results:
        if "STRONG BUY" in r["Signal"]:
            st.success(f"**{r['Coin']}** → {r['Signal']} | {r['Conf']}")

with col2:
    st.subheader("🧠 Psychology Engine")
    st.metric("Market Sentiment", "Bullish Bias", "FOMO + Liquidity Grab")
    st.metric("AI Overall Confidence", "74%", "↑")

# Chart
st.subheader("📈 BTCUSDT Detailed Chart")
df_btc = fetcher.get_ohlcv("BTCUSDT", selected_tf, 300)
if df_btc is not None:
    df_btc = smc.get_indicators(df_btc)
    fig = go.Figure(data=[go.Candlestick(x=df_btc['time'],
                    open=df_btc['open'], high=df_btc['high'],
                    low=df_btc['low'], close=df_btc['close'])])
    fig.add_trace(go.Scatter(x=df_btc['time'], y=df_btc['EMA21'], name="EMA 21", line=dict(color='orange')))
    st.plotly_chart(fig, use_container_width=True)

st.caption(f"Last Updated: {datetime.now().strftime('%d %b %I:%M %p')} | Risk Mode: {risk_percent}% | Global Data via CCXT")
