import streamlit as st
import pandas as pd
import requests
from gtts import gTTS
from streamlit_autorefresh import st_autorefresh
import os

# --- 🔱 TRIPLE AI CORE CONFIG ---
CMC_KEY = "04d81f211e234e55a3e281b9ae23256f"
GROQ_KEY = "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"

st.set_page_config(page_title="H32 OMNI-HEAVY V75", layout="wide")

# --- 🔄 AUTO-COMMAND (Har 30 Sec) ---
count = st_autorefresh(interval=30000, key="omnicore_counter")

# --- 🔱 WAR-ROOM UI (Military Grade) ---
st.markdown("""
<style>
    .stApp { background: #000000 !important; color: #ffffff; }
    .heavy-card {
        background: linear-gradient(135deg, #0f172a 0%, #000000 100%);
        border: 2px solid #1e293b; border-radius: 15px; padding: 25px; margin-bottom: 20px;
    }
    .flow-in { color: #00ff9d; font-weight: bold; text-shadow: 0 0 10px #00ff9d; }
    .flow-out { color: #ff4444; font-weight: bold; text-shadow: 0 0 10px #ff4444; }
    .status-pulse { height: 12px; width: 12px; background: #00ff9d; border-radius: 50%; display: inline-block; animation: pulse 1s infinite; }
    @keyframes pulse { 0% {transform: scale(0.9);} 70% {transform: scale(1.2);} 100% {transform: scale(0.9);} }
</style>
""", unsafe_allow_html=True)

# --- 🔱 TRIPLE AI INTELLIGENCE ---

def get_triple_core_analysis(market_data):
    from groq import Groq
    client = Groq(api_key=GROQ_KEY)
    
    prompt = f"""
    Role: Heavy Macro Commander (Bhari Male Voice).
    Current Intel: {market_data}
    
    Analyze:
    1. LIQUIDITY: US, China, aur Asia se kitne billions enter/exit ho rahe hain?
    2. WHALE PSYCHOLOGY: Ye retail shakeout hai ya real pump?
    3. SOCIAL: TikTok/Twitter par log kis direction mein panic kar rahe hain?
    4. SATELLITE: Global geopolitical risks scan karein.
    
    Voice Advice (Roman Urdu): Bhari mardana mardon wali awaaz.
    Start with: 'Haseem bhai, Triple AI scan mukammal hai...'
    """
    try:
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )
        return resp.choices[0].message.content
    except: return "Global Neural Link Syncing..."

def generate_commander_voice(text):
    try:
        tts = gTTS(text=text, lang='ur', slow=False)
        tts.save("heavy_omni.mp3")
        return "heavy_omni.mp3"
    except: return None

# --- 🔱 DASHBOARD EXECUTION ---

st.title("🔱 H32 QUANTUM: OMNI-HEAVY V75")
st.markdown(f"<span class='status-pulse'></span> **TRIPLE AI CORE: ACTIVE** | Refresh Count: {count}", unsafe_allow_html=True)

target_coins = ["BTC", "ETH", "SOL", "SUI", "XRP", "BONE"]

# --- GLOBAL SCAN ---
url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
headers = {'X-CMC_PRO_API_KEY': CMC_KEY}
params = {'symbol': ",".join(target_coins), 'convert': 'USD'}

try:
    r = requests.get(url, headers=headers, params=params)
    data_all = r.json()['data']
    
    summary_for_ai = []
    cols = st.columns(3)
    
    for i, sym in enumerate(target_coins):
        coin = data_all[sym]
        price = coin['quote']['USD']['price']
        chg = coin['quote']['USD']['percent_change_24h']
        vol_bn = coin['quote']['USD']['volume_24h'] / 1e9
        
        status = "BULLISH INFLOW" if chg > 0 else "BEARISH OUTFLOW"
        s_class = "flow-in" if chg > 0 else "flow-out"
        
        summary_for_ai.append(f"{sym}: ${price:.2f}, Vol: ${vol_bn:.2f}B, Status: {status}")
        
        with cols[i % 3]:
            st.markdown("<div class='heavy-card'>", unsafe_allow_html=True)
            st.subheader(f"🌐 {sym}")
            st.metric("Global Price", f"${price:,.4f}", f"{chg:.2f}%")
            st.write(f"📊 Global Liquidity: **${vol_bn:.2f} Billion**")
            st.markdown(f"**Flow:** <span class='{s_class}'>{status}</span>", unsafe_allow_html=True)
            
            # Urgent Sell Protocol based on your screenshot
            if chg < -1.5:
                st.error("🚨 CAUTION: RETAIL SHAKEOUT DETECTED")
            st.markdown("</div>", unsafe_allow_html=True)

    # --- BRAIN VERDICT ---
    st.divider()
    verdict = get_triple_core_analysis("\n".join(summary_for_ai))
    
    st.markdown("### 🛰️ Triple AI Commander Report")
    st.success(verdict)
    
    # Auto-Voice
    audio = generate_commander_voice(verdict)
    if audio:
        st.audio(audio, autoplay=True)
        
except Exception as e:
    st.error(f"Command Center Bridge Interrupted: {e}")

st.divider()
st.caption("🔱 V75 Omni-Heavy | Triple AI Core | Developed for Haseem Ali")
