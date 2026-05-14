import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go

from data_fetcher import DataFetcher
from smc_engine import SMCEngine
from ai_analyst import AIAnalyst

st.set_page_config(page_title="GDP Quantum Terminal V5", layout="wide")
st.title("🟢 GDP - H32 Quantum Terminal V5")
st.markdown("**Smart Money + Liquidity + AI Trading System**")

# Risk Tracker
st.sidebar.header("⚙️ Risk & Budget Tracker")
account_balance = st.sidebar.number_input("Total Balance (USDT)", value=1000.0, step=50.0)
risk_percent = st.sidebar.slider("Risk % Per Trade", 0.5, 3.0, 1.0, 0.1)
used_risk = 0.0  # Placeholder

st.sidebar.metric("Available Risk", f"${(account_balance * risk_percent/100):.2f}")

fetcher = DataFetcher()
smc = SMCEngine()
ai = AIAnalyst()

# Scanner
st.subheader("📡 Live Market Scanner")
coins = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT"]
results = []

for coin in coins:
    df = fetcher.get_ohlcv(coin, "4h", 200)
    if df is not None:
        df = smc.get_indicators(df)
        signal, reason = smc.get_signal(df)
        analysis = ai.analyze(df, [])
        
        results.append({
            "Coin": coin.replace("USDT", ""),
            "Price": f"${df['close'].iloc[-1]:,.2f}",
            "Signal": signal,
            "Reason": reason,
            "Confidence": f"{analysis['confidence']}%"
        })

st.dataframe(pd.DataFrame(results), use_container_width=True, height=500)

# Best Signal Highlight
st.subheader("🚨 Best Entry Signals")
for r in results:
    if "STRONG BUY" in r["Signal"]:
        st.success(f"**{r['Coin']}** → {r['Signal']}\n{r['Reason']}")

# Chart
st.subheader("📈 BTCUSDT Live Chart")
df_btc = fetcher.get_ohlcv("BTCUSDT", "4h", 300)
if df_btc is not None:
    df_btc = smc.get_indicators(df_btc)
    fig = go.Figure(data=[go.Candlestick(x=df_btc['time'],
                    open=df_btc['open'], high=df_btc['high'],
                    low=df_btc['low'], close=df_btc['close'])])
    fig.add_trace(go.Scatter(x=df_btc['time'], y=df_btc['EMA21'], name="EMA 21"))
    st.plotly_chart(fig, use_container_width=True)

st.caption(f"Last Updated: {datetime.now().strftime('%I:%M %p')} | Risk Mode: {risk_percent}%")
