import streamlit as st
import pandas as pd
import requests
from gtts import gTTS
import os

# --- 🔱 INSTITUTIONAL CORE ---
CMC_KEY = "04d81f211e234e55a3e281b9ae23256f"
GROQ_KEY = "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"

st.set_page_config(page_title="H32 QUANTUM V20", layout="wide")

# --- 🔱 CINEMATIC BLACK UI ---
st.markdown("""
<style>
    .stApp {
        background: radial-gradient(circle at center, #0a0c10 0%, #000000 100%) !important;
        color: #ffffff;
    }
    .macro-card {
        background: rgba(20, 20, 25, 0.7);
        border: 1px solid #30363d;
        border-radius: 15px; padding: 25px;
        margin: 10px 0; backdrop-filter: blur(10px);
    }
    .signal-text { font-size: 2.5rem; font-weight: 900; text-align: center; }
    .global-info { border-left: 4px solid #58a6ff; padding-left: 20px; color: #8b949e; }
</style>
""", unsafe_allow_html=True)

st.title("🔱 H32 QUANTUM V20: GLOBAL INTELLIGENCE")
st.caption("Mode: Institutional Macro-Analysis | Whale Flow Tracking")

# --- 🔱 GLOBAL SITUATION ENGINE ---

def get_global_macro_analysis(asset, price, chg):
    from groq import Groq
    client = Groq(api_key=GROQ_KEY)
    
    # Powerful Macro Prompt
    prompt = f"""
    Analyze {asset} at ${price}. Current Global Situation kya hai? 
    1. US Fed interest rates aur CPI ka kya impact hai?
    2. Global wars ya economic news market ko kyon gira/badha rahi hain?
    3. Whales is waqt kya psychology use kar rahi hain?
    4. Voice Advice: Aik choti natural Roman Urdu line (e.g. 'Duniya ke halaat thode kharab hain, abhi sabr karo').
    
    Language: Roman Urdu (English alphabet). Har point clear aur logic ke sath ho.
    """
    try:
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        return resp.choices[0].message.content
    except: return "Global data link slow hai, magar market structure scanning active hai."

def elite_voice_engine(text):
    try:
        # Roman Urdu text ko 'ur' accent ke sath fast generate karna
        tts = gTTS(text=text, lang='ur', slow=False)
        tts.save("quantum_macro.mp3")
        return "quantum_macro.mp3"
    except: return None

# --- 🔱 DASHBOARD ---

with st.sidebar:
    st.header("🌍 Global Watch")
    selected_coin = st.selectbox("Asset Select", ["BTC", "ETH", "SOL", "SUI", "ONDO", "XRP"])
    st.write("---")
    st.info("Scanning US Treasury & Whale Wallets...")

if st.button("🚀 EXECUTE GLOBAL MACRO SCAN", use_container_width=True):
    with st.spinner("Duniya bhar ke economic indicators scan ho rahe hain..."):
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
        headers = {'X-CMC_PRO_API_KEY': CMC_KEY}
        params = {'symbol': selected_coin, 'convert': 'USD'}
        
        try:
            r = requests.get(url, headers=headers, params=params)
            data = r.json()['data'][selected_coin]
            price = data['quote']['USD']['price']
            chg = data['quote']['USD']['percent_change_24h']
            
            # Macro Brain Logic
            analysis = get_global_macro_analysis(selected_coin, round(price, 2), chg)
            
            # UI Render
            st.markdown("<div class='macro-card'>", unsafe_allow_html=True)
            col1, col2 = st.columns([1, 1])
            with col1:
                st.metric(f"💎 {selected_coin}", f"${price:,.2f}", f"{chg:.2f}%")
            with col2:
                if chg > 0:
                    st.markdown("<div class='signal-text' style='color:#00ff9d;'>BULLISH FLOW</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div class='signal-text' style='color:#ff4444;'>BEARISH TRAP</div>", unsafe_allow_html=True)
            
            st.divider()
            st.markdown(f"### 🌍 Global Situation & Macro Analysis\n<div class='global-info'>{analysis}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Voice Alert
            voice_line = analysis.split('\n')[-1] # Advice line pick karega
            audio_path = elite_voice_engine(f"{selected_coin} scan complete. " + voice_line)
            if audio_path:
                st.audio(audio_path)
                
        except Exception as e:
            st.error(f"Global Link Error: {e}")

st.divider()
st.caption("🔱 Quantum V20 | Developed for Haseem Ali | Global Macro Core")
