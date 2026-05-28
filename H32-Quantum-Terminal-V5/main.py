import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from gtts import gTTS
import io

st.set_page_config(page_title="H32 LIVE TRADING FLOOR", layout="wide")

st.title("📈 H32 LIVE TRADING FLOOR - PROFESSIONAL DATA")

# Tab Selection
tab1, tab2 = st.tabs(["📊 LIVE CHART & PRICE", "🧠 AI INSTITUTIONAL INSIGHT"])

# 1. Fetch Real Candle Data (Gold/Bitcoin)
@st.cache_data(ttl=60) # Data har 60 second mein update hoga
def get_candle_data(ticker="GC=F"):
    data = yf.download(ticker, period="1d", interval="5m")
    return data

# TAB 1: Real TradingView Style Candles
with tab1:
    ticker_symbol = st.selectbox("Select Asset:", ["GC=F", "BTC-USD", "ETH-USD"])
    df = get_candle_data(ticker_symbol)
    
    fig = go.Figure(data=[go.Candlestick(x=df.index,
                    open=df['Open'], high=df['High'],
                    low=df['Low'], close=df['Close'])])
    
    fig.update_layout(xaxis_rangeslider_visible=False, template="plotly_dark", height=500)
    st.plotly_chart(fig, use_container_width=True)

# TAB 2: AI Voice Analysis
with tab2:
    st.subheader("🔊 AI Voice Trading Analysis")
    if st.button("Generate Institutional Voice Analysis"):
        # Yahan hum aapki DeepSeek/Groq key use karke AI analysis banayenge
        analysis_text = f"Bhai, {ticker_symbol} is waqt major support level par hai. Volume spikes indicate kar rahe hain ke smart money entry le raha hai. Bullish setup ke chances zyada hain."
        
        st.info(analysis_text)
        
        # Urdu Voice
        tts = gTTS(text=analysis_text, lang='ur', slow=False)
        audio_buf = io.BytesIO()
        tts.write_to_fp(audio_buf)
        audio_buf.seek(0)
        st.audio(audio_buf, format="audio/mp3")

st.sidebar.success("Floor Status: ACTIVE")
