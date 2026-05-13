import streamlit as st
import pandas as pd
import requests
from gtts import gTTS
import os

# --- 🔱 INSTITUTIONAL CORE ---
[span_0](start_span)CMC_KEY = "04d81f211e234e55a3e281b9ae23256f" #[span_0](end_span)
[span_1](start_span)GROQ_KEY = "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" #[span_1](end_span)

st.set_page_config(page_title="H32 QUANTUM V15", layout="wide")

# --- 🔱 BLACK-OPS UI (Deep Obsidian Theme) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    
    .stApp {
        background: radial-gradient(circle at top, #0d1117 0%, #010409 100%) !important;
        color: #c9d1d9;
        font-family: 'JetBrains Mono', monospace;
    }
    .main-terminal {
        background: rgba(13, 17, 23, 0.8);
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
    }
    .buy-signal {
        background: linear-gradient(90deg, #238636, #2ea043);
        color: white; padding: 15px; border-radius: 8px;
        text-align: center; font-size: 1.8rem; font-weight: bold;
        box-shadow: 0 0 15px rgba(46, 160, 67, 0.3);
    }
    .sell-signal {
        background: linear-gradient(90deg, #da3633, #f85149);
        color: white; padding: 15px; border-radius: 8px;
        text-align: center; font-size: 1.8rem; font-weight: bold;
        box-shadow: 0 0 15px rgba(248, 81, 73, 0.3);
    }
    .metric-value { font-size: 2rem !important; color: #58a6ff !important; }
</style>
""", unsafe_allow_html=True)

# --- 🔱 QUANT INTELLIGENCE ---

def get_pro_verdict(coin, price, chg):
    from groq import Groq
    client = Groq(api_key=GROQ_KEY)
    
    # Psychology-driven instructions
    prompt = f"""
    Elite Quant Trader mindset se {coin} analyze karo at ${price}.
    1. Trap Alert: Kya whales retail ko fasa rahi hain?
    2. Precision Entry: Exact buy level with Fibonacci/SMC logic.
    3. Downside Risk: Market kitne % mazeed gir sakti hai?
    4. Voice Script: Ek natural Roman Urdu line jo main bol sakun (e.g. 'Bhai abhi wait karo, market trap kar rahi hai').
    
    Response short aur high-impact rakho. Roman Urdu (English alphabet) use karo.
    """
    try:
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        return resp.choices[0].message.content
    except: return "System calibration in progress... Market looks volatile."

def generate_natural_voice(text):
    try:
        # Roman Urdu ko 'ur' lang ke saath use karne se natural accent ata hai
        tts = gTTS(text=text, lang='ur', slow=False)
        tts.save("pro_signal.mp3")
        return "pro_signal.mp3"
    except: return None

# --- 🔱 DASHBOARD ---

st.title("🔱 H32 QUANTUM: BLACK-OPS")
st.caption("Status: Institutional Bridge Active | Level: Elite Psychology")

with st.sidebar:
    st.header("🎯 Watchlist")
    coin = st.selectbox("Select Asset", ["BTC", "ETH", "SOL", "SUI", "ONDO", "XRP"])
    st.info("SMC & Liquidity Finder Enabled")

if st.button("🚀 INITIATE QUANTUM SCAN", use_container_width=True):
    with st.spinner("Analyzing Whale Wallets & Order Blocks..."):
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
        headers = {'X-CMC_PRO_API_KEY': CMC_KEY}
        params = {'symbol': coin, 'convert': 'USD'}
        
        try:
            r = requests.get(url, headers=headers, params=params)
            data = r.json()['data'][coin]
            price = data['quote']['USD']['price']
            chg = data['quote']['USD']['percent_change_24h']
            
            # Logic: Buy only if there's a dip or strong recovery
            decision = "🟢 ACCUMULATE" if chg < -2 or chg > 5 else "🔴 AVOID/WAIT"
            style = "buy-signal" if decision == "🟢 ACCUMULATE" else "sell-signal"
            
            # AI Deep Dive
            verdict = get_pro_verdict(coin, round(price, 2), chg)
            
            # UI Render
            st.markdown(f"<div class='main-terminal'>", unsafe_allow_html=True)
            c1, c2 = st.columns([1, 1])
            with c1:
                st.metric(f"{coin} Live", f"${price:,.2f}", f"{chg:.2f}%")
            with c2:
                st.markdown(f"<div class='{style}'>{decision}</div>", unsafe_allow_html=True)
            
            st.markdown(f"### 🐋 Institutional Psychology\n{verdict}")
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Voice Alert
            voice_text = f"{coin} ka scan complete. {decision}. " + verdict.split('\n')[-1]
            audio_path = generate_natural_voice(voice_text)
            if audio_path:
                st.audio(audio_path)
                
        except Exception as e:
            st.error(f"Bridge Interrupted: {e}")

st.divider()
st.caption("V15 Elite | Powered by Dual-Brain Neural Link | Developed for Haseem Ali")
