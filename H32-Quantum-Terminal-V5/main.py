import streamlit as st
import pandas as pd
import requests
from gtts import gTTS
from streamlit_autorefresh import st_autorefresh # Iske liye 'pip install streamlit-autorefresh' lazmi hai
import os

# --- 🔱 GLOBAL COMMAND CONFIG ---
CMC_KEY = "04d81f211e234e55a3e281b9ae23256f"
GROQ_KEY = "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"

st.set_page_config(page_title="H32 OMNISCIENT V60", layout="wide")

# --- 🔄 AUTO-REFRESH TRIGGER (Har 30 Second mein khud refresh hoga) ---
# Aap iska time badal sakte hain (1000 = 1 second)
count = st_autorefresh(interval=30000, limit=None, key="fizzbuzzcounter")

# --- 🔱 WAR-ROOM UI (Full Black Ops) ---
st.markdown("""
<style>
    .stApp { background: #000000 !important; color: #ffffff; }
    .command-center {
        background: rgba(10, 10, 15, 0.95);
        border: 2px solid #1e293b; border-radius: 20px;
        padding: 25px; margin-bottom: 20px;
    }
    .metric-card {
        background: #0d1117; border-radius: 10px; padding: 15px;
        border-left: 5px solid #58a6ff;
    }
    .status-pulse {
        height: 10px; width: 10px; background-color: #00ff9d;
        border-radius: 50%; display: inline-block;
        box-shadow: 0 0 10px #00ff9d; animation: pulse 1s infinite;
    }
    @keyframes pulse { 0% {transform: scale(0.9);} 70% {transform: scale(1.2);} 100% {transform: scale(0.9);} }
</style>
""", unsafe_allow_html=True)

# --- 🔱 OMNISCIENT INTELLIGENCE ENGINE ---

def get_heavy_intelligence(market_summary):
    from groq import Groq
    client = Groq(api_key=GROQ_KEY)
    
    prompt = f"""
    Role: Senior Global Macro Commander (Male).
    Current Market State: {market_summary}
    
    Instructions:
    1. Analyze Billion Dollar Liquidity flows across USA, Asia, and Europe.
    2. Scan Social Media (TikTok/Twitter) panic vs greed levels.
    3. Check for any Geopolitical Satellite warnings.
    4. Voice Script (Roman Urdu): Bhari mardana mardon wali awaaz. 
    Start: 'Haseem bhai, system ne naya flow detect kiya hai...'
    Explain: Kaun bech raha hai, kaun khareed raha hai, aur agle 2 ghante ka plan kya hai.
    """
    try:
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )
        return resp.choices[0].message.content
    except: return "Satellite Link re-routing... Standby."

def generate_commander_voice(text):
    try:
        tts = gTTS(text=text, lang='ur', slow=False)
        tts.save("auto_report.mp3")
        return "auto_report.mp3"
    except: return None

# --- 🔱 LIVE AUTONOMOUS DASHBOARD ---

st.title("🔱 H32 OMNISCIENT V60: AUTO-COMMAND")
st.markdown(f"Status: <span class='status-pulse'></span> **LIVE SCANNING ACTIVE** (Scan #{count})", unsafe_allow_html=True)

target_coins = ["BTC", "ETH", "SOL", "SUI", "XRP", "BONE"]

# --- DATA FETCHING (Automatic) ---
url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
headers = {'X-CMC_PRO_API_KEY': CMC_KEY}
params = {'symbol': ",".join(target_coins), 'convert': 'USD'}

try:
    r = requests.get(url, headers=headers, params=params)
    all_coins = r.json()['data']
    
    summary_list = []
    cols = st.columns(3)
    
    for i, sym in enumerate(target_coins):
        data = all_coins[sym]
        price = data['quote']['USD']['price']
        chg = data['quote']['USD']['percent_change_24h']
        vol_bn = data['quote']['USD']['volume_24h'] / 1e9
        
        flow = "INFLOW" if chg > 0 else "OUTFLOW"
        summary_list.append(f"{sym}: ${price:.2f}, Vol: ${vol_bn:.2f}B, Flow: {flow}")
        
        with cols[i % 3]:
            st.markdown(f"<div class='metric-card'>", unsafe_allow_html=True)
            st.subheader(f"🌐 {sym}")
            st.metric("Live Index", f"${price:,.4f}", f"{chg:.2f}%")
            st.write(f"💵 Liquidity: **${vol_bn:.2f}B**")
            st.markdown(f"**Global Flow:** {flow}")
            st.markdown("</div>", unsafe_allow_html=True)

    # --- AUTOMATIC BRAIN VERDICT ---
    st.divider()
    verdict = get_heavy_intelligence("\n".join(summary_list))
    
    st.markdown("<div class='command-center'>", unsafe_allow_html=True)
    st.markdown(f"### 🛰️ Autonomous Intelligence Report\n{verdict}")
    
    audio_path = generate_commander_voice(verdict)
    if audio_path:
        st.audio(audio_path, autoplay=True) # Autoplay true taake khud awaaz aaye
    st.markdown("</div>", unsafe_allow_html=True)

except Exception as e:
    st.error(f"Global Bridge Interrupted: {e}")

st.divider()
st.caption("🔱 V60 Omniscient | Fully Autonomous War-Room | Developed for Haseem Ali")
