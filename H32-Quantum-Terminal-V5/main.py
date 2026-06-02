import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="H32 Compound Trend Bot", layout="wide")
st.title("⚡ H32 Compound Trend Bot (SuperTrend + EMA)")
st.subheader("Smart Entry + Timing System")

coins = {
    "Bitcoin (BTC)": "BTC-USD",
    "Ethereum (ETH)": "ETH-USD",
    "Solana (SOL)": "SOL-USD",
    "Sui (SUI)": "SUI-USD",
    "Chainlink (LINK)": "LINK-USD"
}

selected_coin = st.selectbox("Select Coin", list(coins.keys()))
ticker = coins[selected_coin]

st.sidebar.header("Strategy Settings")
st_period = st.sidebar.slider("SuperTrend Period", 7, 20, 10)
st_mult = st.sidebar.slider("SuperTrend Multiplier", 1.0, 5.0, 3.0)

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

    # === Indicators ===
    df_1h['EMA20'] = ta.ema(df_1h['Close'], 20)
    df_1h['EMA50'] = ta.ema(df_1h['Close'], 50)

    st_data = ta.supertrend(df_1h['High'], df_1h['Low'], df_1h['Close'], 
                           length=st_period, multiplier=st_mult)
    df_1h['SuperTrend'] = st_data['SUPERT_' + str(st_period) + '_' + str(st_mult)]
    df_1h['ST_Dir'] = st_data['SUPERTd_' + str(st_period) + '_' + str(st_mult)]

    # === Compound Logic ===
    last_row = df_1h.iloc[-1]
    prev_row = df_1h.iloc[-2]

    ema_bull = last_row['EMA20'] > last_row['EMA50']
    super_bull = last_row['ST_Dir'] == 1

    if ema_bull and super_bull and live_price > last_row['SuperTrend']:
        signal = "🟢 STRONG BUY SIGNAL"
        signal_color = "lime"
        entry_note = "Demand Zone + SuperTrend Flip"
    elif not ema_bull and not super_bull and live_price < last_row['SuperTrend']:
        signal = "🔴 STRONG SELL SIGNAL"
        signal_color = "red"
        entry_note = "Supply Zone + SuperTrend Flip"
    else:
        signal = "⭕ WAIT / NO CLEAR SIGNAL"
        signal_color = "orange"
        entry_note = "Trend not confirmed"

    # UI
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(f"{selected_coin} Price", f"${live_price:,.4f}")
    with col2:
        st.markdown(f"**Signal:** <span style='color:{signal_color}; font-size:26px; font-weight:bold;'>{signal}</span>", unsafe_allow_html=True)
    with col3:
        st.metric("Entry Suggestion", entry_note)

    # Chart
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=df_1h.index, open=df_1h['Open'], high=df_1h['High'],
                                 low=df_1h['Low'], close=df_1h['Close']))
    fig.add_trace(go.Scatter(x=df_1h.index, y=df_1h['SuperTrend'], line=dict(color='violet', width=3), name="SuperTrend"))
    fig.add_trace(go.Scatter(x=df_1h.index, y=df_1h['EMA20'], line=dict(color='orange'), name="EMA 20"))
    fig.add_trace(go.Scatter(x=df_1h.index, y=df_1h['EMA50'], line=dict(color='blue'), name="EMA 50"))

    fig.update_layout(height=650, template="plotly_dark", title="Compound Strategy Chart")
    st.plotly_chart(fig, use_container_width=True)

    st.info(f"**Logic:** SuperTrend + EMA20/50 dono agree karein tabhi strong signal. Yeh bot timing ke liye best hai.")

except Exception as e:
    st.error(f"Error: {e}")
