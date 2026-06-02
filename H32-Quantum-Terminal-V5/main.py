import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import talib

st.set_page_config(page_title="H32 Compound Trend Bot", layout="wide")

st.title("⚡ H32 Compound Trend Bot")
st.subheader("SuperTrend + EMA Combined Strategy")

# Coin Selector
coins = {
    "Bitcoin (BTC)": "BTC-USD",
    "Ethereum (ETH)": "ETH-USD",
    "Solana (SOL)": "SOL-USD",
    "Sui (SUI)": "SUI-USD",
    "Chainlink (LINK)": "LINK-USD"
}

selected_coin = st.selectbox("Select Coin", list(coins.keys()))
ticker = coins[selected_coin]

# Sidebar
st.sidebar.header("Strategy Settings")
period = st.sidebar.slider("SuperTrend Period", 7, 20, 10)
multiplier = st.sidebar.slider("SuperTrend Multiplier", 1.0, 5.0, 3.0)

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

    # EMA Calculation
    df_1h['EMA20'] = talib.EMA(df_1h['Close'], timeperiod=20)
    df_1h['EMA50'] = talib.EMA(df_1h['Close'], timeperiod=50)

    # Simple SuperTrend (Manual)
    hl2 = (df_1h['High'] + df_1h['Low']) / 2
    atr = talib.ATR(df_1h['High'], df_1h['Low'], df_1h['Close'], timeperiod=period)
    upper_band = hl2 + (multiplier * atr)
    df_1h['SuperTrend'] = upper_band

    # Signal Logic
    last = df_1h.iloc[-1]
    
    if last['EMA20'] > last['EMA50']:
        signal = "🟢 STRONG BUY"
        color = "lime"
    elif last['EMA20'] < last['EMA50']:
        signal = "🔴 STRONG SELL"
        color = "red"
    else:
        signal = "⭕ WAIT"
        color = "orange"

    # UI
    col1, col2 = st.columns(2)
    with col1:
        st.metric(f"{selected_coin} Price", f"${live_price:,.4f}")
    with col2:
        st.markdown(f"**Signal:** <span style='color:{color}; font-size:28px; font-weight:bold;'>{signal}</span>", unsafe_allow_html=True)

    # Chart
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=df_1h.index,
                                 open=df_1h['Open'],
                                 high=df_1h['High'],
                                 low=df_1h['Low'],
                                 close=df_1h['Close'],
                                 name="Candlestick"))
    
    fig.add_trace(go.Scatter(x=df_1h.index, y=df_1h['EMA20'], 
                           line=dict(color='orange', width=2), name="EMA 20"))
    fig.add_trace(go.Scatter(x=df_1h.index, y=df_1h['EMA50'], 
                           line=dict(color='blue', width=2), name="EMA 50"))
    fig.add_trace(go.Scatter(x=df_1h.index, y=df_1h['SuperTrend'], 
                           line=dict(color='violet', width=3), name="SuperTrend"))

    fig.update_layout(height=650, template="plotly_dark", xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Error: {str(e)}")
