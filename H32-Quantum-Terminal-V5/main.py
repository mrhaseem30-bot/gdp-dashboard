import streamlit as st
from data_fetcher import get_binance_data
from smc_engine import detect_market_structure, calculate_confluence
from ai_analyst import get_ai_verdict
from tts_urdu import speak_urdu

st.set_page_config(page_title="H32 Quantum Terminal V4", layout="wide")
st.title("H32 Quantum Terminal V4 - Urdu Voice")

symbol = st.selectbox("Coin Select", ["BTC/USDT", "ETH/USDT", "SOL/USDT", ...])

if st.button("Analyze Now"):
    with st.spinner("Quantum Analysis chal raha hai..."):
        df = get_binance_data(symbol, "15m")
        price = df['close'].iloc[-1]
        
        structure, _ = detect_market_structure(df)
        score, reasons = calculate_confluence(df, price)
        
        ai_response = get_ai_verdict(symbol, price, structure, score, reasons)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Price", f"${price:,.2f}", delta=None)
            st.subheader("Confluence Score")
            st.progress(score/100)
            st.success(f"{score}%") if score > 70 else st.warning(f"{score}%")
        
        with col2:
            st.subheader("AI Verdict + Reasons")
            st.write(ai_response)
            
            # Urdu Voice
            if st.button("Urdu Mein Suno"):
                audio_file = speak_urdu(ai_response)
                st.audio(audio_file, format="audio/mp3")
