import streamlit as st
import pandas as pd
import requests
from gtts import gTTS
import os

# --- 🔱 INSTITUTIONAL CORE ---
CMC_KEY = "04d81f211e234e55a3e281b9ae23256f"
GROQ_KEY = "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"

st.set_page_config(page_title="H32 NEURAL V25", layout="wide")

# --- 🔱 ULTIMATE DARK UI ---
st.markdown("""
<style>
    .stApp { background: #010204 !important; color: #ffffff; }
    .history-card {
        background: rgba(30, 30, 40, 0.4);
        border: 1px solid #30363d;
        border-radius: 12px; padding: 20px; margin-top: 10px;
    }
    .voice-btn { border-radius: 50px; background: #58a6ff; color: white; }
</style>
""", unsafe_allow_html=True)

st.title("🔱 H32 QUANTUM: NEURAL HISTORIAN V25")
st.caption("Brain Mode: Autonomous History Analysis + Global Macro")

# --- 🔱 SELF-ANALYSIS & HISTORY ENGINE ---

def get_autonomous_analysis(asset, price, chg):
    from groq import Groq
    client = Groq(api_key=GROQ_KEY)
    
    # AI ko autonomous banaya gaya hai
    prompt = f"""
    Tum ek Autonomous AI Trader ho. Asset: {asset} at ${price} ({chg}%).
    
    Task:
    1. HISTORY ANALYSIS: Is asset ki purani bari moves aur traps ki history nikalo (e.g. 'Last time jab aisa hua tha to market ne dump kiya tha').
    2. GLOBAL REASON: Dunya ke halaat (Fed, CPI, Wars) kyon is asset ko hila rahe hain?
    3. WHALE PSYCHOLOGY: Baray traders ka agla step kya hoga?
    4. VOICE SCRIPT: Ek natural Roman Urdu (WhatsApp style) advice jo 1 minute tak chalay (Detail mein samjhao).
    
    Style: Roman Urdu (English letters). Bilkul bhaiyon wali baat jo detail mein ho.
    """
    try:
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        return resp.choices[0].message.content
    except: return "Neural connection re-establishing... Scaning price action history."

def generate_pro_voice(text):
    try:
        # Voice ko natural speed aur pause ke sath set kiya
        tts = gTTS(text=text, lang='ur', slow=False)
        tts.save("neural_final.mp3")
        return "neural_final.mp3"
    except: return None

# --- 🔱 TERMINAL DASHBOARD ---

with st.sidebar:
    st.header("🧬 Neural DNA")
    coin = st.selectbox("Asset Select", ["BTC", "ETH", "SOL", "SUI", "ONDO", "XRP", "BONE"])
    st.write("---")
    st.info("Autonomous Brain: ACTIVE")

if st.button("🚀 EXECUTE NEURAL HISTORY SCAN", use_container_width=True):
    with st.spinner("Purani history aur global trends scan ho rahe hain..."):
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
        headers = {'X-CMC_PRO_API_KEY': CMC_KEY}
        params = {'symbol': coin, 'convert': 'USD'}
        
        try:
            r = requests.get(url, headers=headers, params=params)
            data = r.json()['data'][coin]
            price = data['quote']['USD']['price']
            chg = data['quote']['USD']['percent_change_24h']
            
            # Autonomous AI Logic
            analysis = get_autonomous_analysis(coin, round(price, 4), chg)
            
            # UI Render
            st.markdown("<div class='history-card'>", unsafe_allow_html=True)
            c1, c2 = st.columns([1, 1])
            with c1:
                st.metric(f"💎 {coin} Current", f"${price:,.4f}", f"{chg:.2f}%")
            with c2:
                status = "🟢 SMART ACCUMULATION" if chg < 0 else "🔴 RETAIL FOMO / TRAP"
                st.subheader(status)
            
            st.divider()
            st.markdown(f"### 🧠 Neural History & Global Analysis\n{analysis}")
            
            # Voice Generation
            audio_path = generate_pro_voice(analysis)
            if audio_path:
                st.audio(audio_path)
            st.markdown("</div>", unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"Neural Bridge Error: {e}")

st.divider()
st.caption("🔱 Quantum V25 | Autonomous Neural Historian | Developed for Haseem Ali")
