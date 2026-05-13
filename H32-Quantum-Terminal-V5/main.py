import streamlit as st
import pand
import requests
from gtts import gTTS
import os

# --- 🔄 SAFE AUTO-REFRESH IMPORT ---
try:
    from streamlit_autorefresh import st_autorefresh
    AUTO_REFRESH_AVAILABLE = True
except ImportError:
    AUTO_REFRESH_AVAILABLE = False

# --- 🔱 CONFIG & CORE ---
CMC_KEY = "04d81f211e234e55a3e281b9ae23256f"
GROQ_KEY = "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"

st.set_page_config(page_title="H32 OMNI-CORE V80", layout="wide")

# CSS Integration from your uploaded style.css
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #0a0e17, #11151f) !important; color: white; }
    .heavy-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid #1f2937; border-radius: 15px; padding: 20px;
    }
    .big-signal { padding: 25px; border-radius: 20px; text-align: center; font-size: 1.8rem; font-weight: bold; animation: pulse 2s infinite; }
    @keyframes pulse { 0% {opacity: 1;} 50% {opacity: 0.7;} 100% {opacity: 1;} }
</style>
""", unsafe_allow_html=True)

# --- 🔄 AUTO-START ENGINE ---
if AUTO_REFRESH_AVAILABLE:
    st_autorefresh(interval=30000, key="omnicore_v80")
else:
    st.warning("⚠️ Module 'streamlit-autorefresh' missing. Please run: pip install streamlit-autorefresh")

# --- 🔱 TRIPLE AI BRAIN ---

def get_global_intelligence(data):
    from groq import Groq
    client = Groq(api_key=GROQ_KEY)
    prompt = f"""
    Role: Senior Global Macro Commander (Heavy Male Voice).
    Data: {data}
    Analyze:
    1. Geopolitical Flow: Kis country se paisa nikal raha hai?
    2. Social Sentiment: TikTok/Twitter trends.
    3. Liquidity: Billion dollar whale movements.
    Voice Report: Roman Urdu. Start with 'Haseem bhai, Global Intelligence scan mukammal hai...'
    """
    try:
        resp = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}], temperature=0.1)
        return resp.choices[0].message.content
    except: return "Neural Link offline. Manual monitoring required."

# --- 🔱 DASHBOARD ---

st.title("🔱 H32 QUANTUM: OMNI-CORE V80")
st.write("Status: **Autonomous Global Surveillance Active**")

target_coins = ["BTC", "ETH", "SOL", "SUI", "XRP", "BONE"]

try:
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    headers = {'X-CMC_PRO_API_KEY': CMC_KEY}
    params = {'symbol': ",".join(target_coins), 'convert': 'USD'}
    
    r = requests.get(url, headers=headers, params=params)
    all_data = r.json()['data']
    
    intel_summary = []
    cols = st.columns(3)
    
    for i, sym in enumerate(target_coins):
        coin = all_data[sym]
        price, chg, vol = coin['quote']['USD']['price'], coin['quote']['USD']['percent_change_24h'], coin['quote']['USD']['volume_24h']/1e9
        
        intel_summary.append(f"{sym}: ${price:.2f}, Vol: ${vol:.2f}B, Chg: {chg:.2f}%")
        
        with cols[i % 3]:
            st.markdown("<div class='heavy-card'>", unsafe_allow_html=True)
            st.subheader(f"📡 {sym}")
            st.metric("Price", f"${price:,.4f}", f"{chg:.2f}%")
            st.write(f"💵 Liquidity: **${vol:.2f} Billion**")
            
            if chg < -1.5:
                st.markdown("<div style='color: #ff4444; font-weight: bold;'>🚨 LIQUIDITY DUMP DETECTED</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # Brain Execution
    st.divider()
    verdict = get_global_intelligence("\n".join(intel_summary))
    st.markdown("### 🧠 Commander Intelligence Report")
    st.info(verdict)
    
    # Voice Autoplay
    tts = gTTS(text=verdict, lang='ur', slow=False)
    tts.save("v80_report.mp3")
    st.audio("v80_report.mp3", autoplay=True)

except Exception as e:
    st.error(f"System Error: {e}")

st.divider()
st.caption("🔱 V80 Omni-Core | Triple AI Intelligence | Developed for Haseem Ali")
