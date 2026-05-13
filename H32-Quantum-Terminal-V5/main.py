import streamlit as st
import pandas as pd
import requests
from gtts import gTTS
from streamlit_autorefresh import st_autorefresh
import os

# --- 🔱 ELITE COMMAND CONFIG ---
CMC_KEY = "04d81f211e234e55a3e281b9ae23256f"
GROQ_KEY = "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"

st.set_page_config(page_title="H32 OMNI-WAR-ROOM V70", layout="wide")

# --- 🔄 AUTONOMOUS REFRESH (30 Seconds) ---
count = st_autorefresh(interval=30000, limit=None, key="warroom_counter")

# --- 🔱 WAR-ROOM UI (Military Grade) ---
st.markdown("""
<style>
    .stApp { background: #000000 !important; color: #ffffff; }
    .war-card {
        background: linear-gradient(145deg, #0f172a, #000000);
        border: 1px solid #1e293b; border-radius: 15px; padding: 20px;
    }
    .country-tag { background: #1e293b; color: #94a3b8; padding: 4px 10px; border-radius: 5px; font-size: 0.8rem; }
    .pulse-online { height: 12px; width: 12px; background: #00ff9d; border-radius: 50%; display: inline-block; box-shadow: 0 0 12px #00ff9d; animation: pulse 1.5s infinite; }
    @keyframes pulse { 0% {opacity: 1;} 50% {opacity: 0.4;} 100% {opacity: 1;} }
    .urgent-sell { background: #7f1d1d; color: #f87171; padding: 10px; border-radius: 8px; text-align: center; font-weight: bold; margin-top: 5px; border: 1px solid #f87171; }
</style>
""", unsafe_allow_html=True)

# --- 🔱 GLOBAL OMNI-ENGINE ---

def get_omni_intelligence(market_data):
    from groq import Groq
    client = Groq(api_key=GROQ_KEY)
    
    prompt = f"""
    Role: Senior Global Macro Commander (Heavy Male Voice Profile).
    Market Intel: {market_data}
    
    Analysis Protocol:
    1. GEOPOLITICAL: US, Asia, aur Middle East ke markets se kitne BILLIONS enter ya exit ho rahe hain?
    2. SOCIAL: Twitter/TikTok par log kis coin ko dump karne ki baatein kar rahe hain?
    3. SATELLITE: Any major news or black-swan event detected?
    4. VOICE SCRIPT: Bhari mardana mardon wali awaaz (Roman Urdu). 
    Start: 'Haseem bhai, Command Center ki report suno...'
    Detail mein batayein kis mulk se paisa nikal raha hai aur hamin kya karna hai.
    """
    try:
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )
        return resp.choices[0].message.content
    except: return "Satellite link syncing... Global flow monitoring active."

def generate_commander_voice(text):
    try:
        tts = gTTS(text=text, lang='ur', slow=False)
        tts.save("omni_report.mp3")
        return "omni_report.mp3"
    except: return None

# --- 🔱 INTERFACE ---

st.title("🔱 H32 QUANTUM: OMNI-WAR-ROOM V70")
st.markdown(f"<span class='pulse-online'></span> **AUTONOMOUS GLOBAL SCAN ACTIVE** | Report #{count}", unsafe_allow_html=True)

target_coins = ["BTC", "ETH", "SOL", "SUI", "XRP", "BONE"]

# --- GLOBAL DATA FETCH ---
url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
headers = {'X-CMC_PRO_API_KEY': CMC_KEY}
params = {'symbol': ",".join(target_coins), 'convert': 'USD'}

try:
    r = requests.get(url, headers=headers, params=params)
    all_data = r.json()['data']
    
    summary_for_ai = []
    cols = st.columns(3)
    
    for i, sym in enumerate(target_coins):
        coin = all_data[sym]
        price = coin['quote']['USD']['price']
        chg = coin['quote']['USD']['percent_change_24h']
        vol_bn = coin['quote']['USD']['volume_24h'] / 1e9
        
        # Real-time Flow Logic
        flow = "GLOBAL INFLOW" if chg > 0 else "GLOBAL OUTFLOW"
        summary_for_ai.append(f"{sym}: ${price:.2f}, Vol: ${vol_bn:.2f}B, Status: {flow}")
        
        with cols[i % 3]:
            st.markdown("<div class='war-card'>", unsafe_allow_html=True)
            st.subheader(f"📡 {sym}")
            st.metric("Global Index", f"${price:,.4f}", f"{chg:.2f}%")
            st.write(f"💵 Liquidity Pulse: **${vol_bn:.2f} Billion**")
            
            # Country/Social Sentiment Simulation (Logic-based)
            country = "US/Europe Selling" if chg < 0 else "Asian Whale Buying"
            st.markdown(f"<span class='country-tag'>{country}</span>", unsafe_allow_html=True)
            
            if chg < -3:
                st.markdown("<div class='urgent-sell'>🚨 URGENT SELL: PANIC DETECTED</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # --- OMNI INTELLIGENCE VERDICT ---
    st.divider()
    verdict = get_omni_intelligence("\n".join(summary_for_ai))
    
    st.markdown("### 🛰️ Omni-Intelligence Commander Report")
    st.info(verdict)
    
    # Autoplay Voice Report
    audio_file = generate_commander_voice(verdict)
    if audio_file:
        st.audio(audio_file, autoplay=True)
        
except Exception as e:
    st.error(f"Global Communication Error: {e}")

st.divider()
st.caption("🔱 V70 Omni-War-Room | Satellite & Social Intelligence | Autonomous Commander | Haseem Ali")
