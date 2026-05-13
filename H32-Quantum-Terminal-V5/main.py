import streamlit as st
import pandas as pd
import requests
from gtts import gTTS
import os

# --- 🔱 ELITE CORE ---
CMC_KEY = "04d81f211e234e55a3e281b9ae23256f"
GROQ_KEY = "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"

st.set_page_config(page_title="H32 NEURAL V30", layout="wide")

# --- 🔱 DARK-OPS PREMIUM UI ---
st.markdown("""
<style>
    .stApp { background: #000000 !important; color: #ffffff; }
    .card {
        background: #0d1117; border: 1px solid #30363d;
        border-radius: 10px; padding: 20px;
    }
    .stButton>button { width: 100%; border-radius: 8px; background: #238636; color: white; }
</style>
""", unsafe_allow_html=True)

st.title("🔱 H32 QUANTUM: NEURAL V30")
st.caption("Brain: Autonomous History + Pro Male Voice Engine")

# --- 🔱 THE BRAIN ENGINE ---

def get_pro_analysis(coin, price, chg):
    from groq import Groq
    client = Groq(api_key=GROQ_KEY)
    
    # AI ko mardana lehjay aur history ke liye sakht hidayat
    prompt = f"""
    Tum aik professional mard trader ho. Mere bhai Haseem ko samjhao.
    Asset: {coin} Price: ${price} ({chg}%).
    
    Analysis Steps:
    1. HISTORY: Purani history dekh kar batao ke ye trap hai ya real?
    2. GLOBAL: US Fed aur dunya ke halaat kyon market gira/badha rahe hain?
    3. WHALE MOVE: Baray traders agla jhatka kahan denge?
    4. VOICE SCRIPT: Roman Urdu (WhatsApp style) mein mardana aur bhari lehjay wali advice.
    
    Advice aise do: 'Suno Haseem bhai, market is waqt...' (Be a man, be direct).
    """
    try:
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        return resp.choices[0].message.content
    except: return "Neural link down. Price action scanning manually."

def generate_male_voice(text):
    try:
        # 'ur' lang aur thoda fast pitch natural male flow deti hai
        tts = gTTS(text=text, lang='ur', slow=False)
        tts.save("male_advice.mp3")
        return "male_advice.mp3"
    except: return None

# --- 🔱 DASHBOARD ---

with st.sidebar:
    st.header("⚙️ System Control")
    asset = st.selectbox("Choose Coin", ["BTC", "ETH", "SOL", "SUI", "XRP", "BONE"])
    st.success("Male Neural Engine: ACTIVE")

if st.button("🚀 EXECUTE FULL HISTORY SCAN"):
    with st.spinner("History aur Global trends scan ho rahe hain..."):
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
        headers = {'X-CMC_PRO_API_KEY': CMC_KEY}
        params = {'symbol': asset, 'convert': 'USD'}
        
        try:
            r = requests.get(url, headers=headers, params=params)
            data = r.json()['data'][asset]
            price = data['quote']['USD']['price']
            chg = data['quote']['USD']['percent_change_24h']
            
            # Get Deep Logic
            verdict = get_pro_analysis(asset, round(price, 4), chg)
            
            # Display
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            col1, col2 = st.columns([1,1])
            with col1:
                st.metric(f"💎 {asset}", f"${price:,.4f}", f"{chg:.2f}%")
            with col2:
                status = "✅ SMART ENTRY" if chg < 0 else "⚠️ RISK / TRAP"
                st.subheader(status)
            
            st.divider()
            st.markdown(f"### 🧠 Neural History Analysis\n{verdict}")
            
            # Voice Alert (Male Accent)
            audio_path = generate_male_voice(verdict)
            if audio_path:
                st.audio(audio_path)
            st.markdown("</div>", unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"System Error: {e}")

st.divider()
st.caption("🔱 Quantum V30 | Brother-Voice Edition | Only for Haseem Ali")
