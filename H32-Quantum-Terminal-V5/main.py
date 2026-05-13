import streamlit as st
import pandas as pd
import requests
from gtts import gTTS
import os

# --- 🔱 QUANTUM CORE CONFIG ---
CMC_KEY = "04d81f211e234e55a3e281b9ae23256f"
GROQ_KEY = "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"

st.set_page_config(page_title="H32 NEURAL V18", layout="wide")

# --- 🔱 PREMIUM OBSIDIAN UI ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@500;700&display=swap');
    
    .stApp {
        background: linear-gradient(180deg, #050505 0%, #0a0c12 100%) !important;
        color: #e0e0e0;
        font-family: 'Rajdhani', sans-serif;
    }
    .stButton>button {
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%);
        color: black !important; font-weight: bold; border: none; border-radius: 50px;
        transition: 0.3s all ease;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 20px #4facfe; }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px; padding: 25px; margin: 10px 0;
    }
    .metric-box { text-align: center; border-right: 1px solid #333; }
    .status-active { color: #00ff9d; font-weight: bold; text-shadow: 0 0 10px #00ff9d; }
</style>
""", unsafe_allow_html=True)

# --- 🔱 NEURAL LOGIC ENGINE ---

def get_neural_analysis(coin, price, chg):
    from groq import Groq
    client = Groq(api_key=GROQ_KEY)
    
    # Whale Psychology Prompt
    prompt = f"""
    Elite Whale Trader ki tarah {coin} analyze karo at ${price}.
    1. Trap Alert: Kya retail panic mein hai?
    2. Exact Target: Next 4 hours ka potential target aur % drop risk.
    3. Voice Line: Roman Urdu mein ek choti aur powerfull advice (e.g. 'Abhi sabr karo, whales trap kar rahi hain').
    Output: Points mein do, Roman Urdu script use karo.
    """
    try:
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        return resp.choices[0].message.content
    except: return "Neural link down. Retrying connection..."

def speak_pro(text):
    try:
        # Voice speed thodi fast rakhi hai taake natural lage
        tts = gTTS(text=text, lang='ur', slow=False)
        tts.save("neural_voice.mp3")
        return "neural_voice.mp3"
    except: return None

# --- 🔱 INTERFACE ---

st.title("🔱 H32 NEURAL OBSIDIAN V18")
st.markdown("Status: <span class='status-active'>QUANTUM BRIDGE ACTIVE</span>", unsafe_allow_html=True)

with st.sidebar:
    st.header("🌌 Neural Targets")
    asset = st.selectbox("Asset Select", ["BTC", "ETH", "SOL", "SUI", "ONDO", "XRP"])
    st.markdown("---")
    st.caption("Auto-SMC & Whale Hunt Active")

if st.button("🚀 INITIATE NEURAL SCAN", use_container_width=True):
    with st.spinner("Decoding Whale Flow..."):
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
        headers = {'X-CMC_PRO_API_KEY': CMC_KEY}
        params = {'symbol': asset, 'convert': 'USD'}
        
        try:
            r = requests.get(url, headers=headers, params=params)
            data = r.json()['data'][asset]
            price = data['quote']['USD']['price']
            chg = data['quote']['USD']['percent_change_24h']
            
            analysis = get_neural_analysis(asset, round(price, 2), chg)
            
            # --- UI Display ---
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            col1, col2 = st.columns([1, 1])
            with col1:
                st.metric(f"💎 {asset} Index", f"${price:,.2f}", f"{chg:.2f}%")
            with col2:
                # Dynamic Logic
                if chg < -1:
                    st.success("🟢 ACCUMULATION MODE: WHALES BUYING THE DIP")
                else:
                    st.warning("🟠 WAIT MODE: RETAIL TRAP DETECTED")
            
            st.divider()
            st.markdown(f"### 🧠 Neural Intelligence Analysis\n{analysis}")
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Voice Alert
            voice_line = analysis.split('\n')[-1] # Akhri line uthaye ga advice ke liye
            audio_path = speak_pro(f"{asset} ka analysis ready hai. {voice_line}")
            if audio_path:
                st.audio(audio_path)
                
        except Exception as e:
            st.error(f"Bridge Error: {e}")

st.divider()
st.caption("🔱 Quantum V18 Elite | Developed for Haseem Ali | Obsidian Stable")
