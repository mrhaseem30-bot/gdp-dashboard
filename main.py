import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go

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

# Sidebar Settings
st.sidebar.header("Strategy Settings")
st_period = st.sidebar.slider("SuperTrend Period", min_value=7, max_value=20, value=10)
st_mult = st.sidebar.slider("SuperTrend Multiplier", min_value=1.0, max_value=5.0, value=3.0)

@st.cache_data(ttl=60)
def get_data(ticker):
    df_15m = yf.download(ticker, period="3d", interval="15m")
    df_1h = yf.download(ticker, period="15d", interval="1h")
    return df_15m, df_1h

try:
    df_15m, df_1h = get_data(ticker)

    # Column cleaning
    for df in [df_15m, df_1h]:
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

    live_price = float(df_15m['Close'].iloc[-1])

    # Indicators
    df_1h['EMA20'] = ta.ema(df_1h['Close'], length=20)
    df_1h['EMA50'] = ta.ema(df_1h['Close'], length=50)

    supertrend = ta.supertrend(high=df_1h['High'], 
                               low=df_1h['Low'], 
                               close=df_1h['Close'], 
                               length=st_period, 
                               multiplier=st_mult)

    df_1h['SuperTrend'] = supertrend[f'SUPERT_{st_period}_{st_mult}']
    df_1h['ST_Dir'] = supertrend[f'SUPERTd_{st_period}_{st_mult}']

    # Signal Logic
    last = df_1h.iloc[-1]
    trend = "🟢 STRONG BUY" if (last['ST_Dir'] == 1 and last['EMA20'] > last['EMA50']) else \
            "🔴 STRONG SELL" if (last['ST_Dir'] == -1 and last['EMA20'] < last['EMA50']) else \
            "⭕ WAIT"

    color = "lime" if "BUY" in trend else "red" if "SELL" in trend else "orange"

    # Display
    col1, col2 = st.columns(2)
    with col1:
        st.metric(f"{selected_coin} Live Price", f"${live_price:,.4f}")
    with col2:
        st.markdown(f"**Signal:** <span style='color:{color}; font-size:28px; font-weight:bold;'>{trend}</span>", unsafe_allow_html=True)

    # Chart
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=df_1h.index, open=df_1h['Open'], high=df_1h['High'],
                                 low=df_1h['Low'], close=df_1h['Close'], name="OHLC"))
    fig.add_trace(go.Scatter(x=df_1h.index, y=df_1h['SuperTrend'], 
                           line=dict(color='violet', width=3), name="SuperTrend"))
    fig.add_trace(go.Scatter(x=df_1h.index, y=df_1h['EMA20'], line=dict(color='orange'), name="EMA 20"))
    fig.add_trace(go.Scatter(x=df_1h.index, y=df_1h['EMA50'], line=dict(color='blue'), name="EMA 50"))

    fig.update_layout(height=650, template="plotly_dark", xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Error: {str(e)}")
