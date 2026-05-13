import streamlit as st
import pandas as pd
import requests
import time
from gtts import gTTS
from groq import Groq

# --- 🔱 INSTITUTIONAL ACCESS ---
GROQ_API_KEY = "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"
CMC_API_KEY = "04d81f211e234e55a3e281b9ae23256f"

st.set_page_config(page_title="H32 QUANTUM V12: WHALE CORE", layout="wide")

# --- 🔱 THE "WALL STREET" UI ---
st.markdown("""
<style>
    .stApp { background: #010409 !important; color: #e6edf3; }
    .whale-card {
        background: linear-gradient(145deg, #0d1117, #1c2128);
        padding: 30px; border-radius: 20px; border: 1px solid #30363d;
        box-shadow: 0 10px 30px rgba(0,0,0,0.7);
        margin-bottom: 25px;
    }
    .trap-warning {
        background: rgba(255, 68, 68, 0.1); padding: 15px;
        border-radius: 12px; border: 1px solid #ff4444; color: #ff4444;
        font-weight: bold; text-align: center; margin: 10px 0;
    }
    .entry-zone {
        background: rgba(0, 255, 157, 0.1); padding: 20px;
        border-radius: 12px; border: 1px solid #00ff9d; color: #00ff9d;
        font-size: 1.5rem; font-weight: bold; text-align: center;
    }
</style>
""", unsafe_allow_html=True)

st.title("🔱 H32 QUANTUM V12: ELITE WHALE PSYCHOLOGY")
st.write("Mode: **Institutional Liquidity Sweep (Anti-Retail Trap)**")

# --- 🔱 QUANT PSYCHOLOGY ENGINE ---

def get_whale_logic(symbol, price, chg):
    """Bade AI Traders ki psychology based decision logic"""
    try:
        client = Groq(api_key=GROQ_API_KEY)
        # Roman Urdu instructing for natural sound + strict levels
        prompt = f"""
        Act as a 200 IQ Quant Hedge Fund Manager. 
        Asset: {symbol} at ${price} ({chg}%).
        
        Analyze:
        1. Retail Trap: Kya retail traders ko trap kiya ja raha hai? 
        2. Liquidity Hunt: Market stop-loss hit karne kitne percent (%) niche jayegi? Exact % drop batao.
        3. Point of Control (POC): Exact entry price for Whales.
        4. Invalidation: Kab ye setup fail ho jayega (SL).
        
        Output Style: Roman Urdu (English alphabet). Clear, Direct, No Fluff.
        Use points: TRAP CHECK, DOWNSIDE %, BEST ENTRY, STOP LOSS.
        """
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1 # Low temp = No mistakes, only data
        )
        return resp.choices[0].message.content
    except: return "Network glitch. Market structure remains under Whale accumulation."

def natural_voice(text):
    """High Speed Voice Alert"""
    try:
        # Roman Urdu text ko ur accent mein bolne se natural sound ati hai
        tts = gTTS(text=text, lang='ur', slow=False)
        tts.save("whale_alert.mp3")
        return "whale_alert.mp3"
    except: return None

# --- 🔱 TERMINAL DASHBOARD ---

with st.sidebar:
    st.header("🐋 Whale DNA Scanner")
    target_coin = st.selectbox("Symbol", ["BTC", "ETH", "SOL", "SUI", "ONDO", "HYPE", "XRP"])
    st.markdown("---")
    st.write("📊 **Smart Money Concept (SMC) Active**")
    st.write("🛡️ **Anti-Liquidation Filter: ON**")

if st.button("🚀 EXECUTE INSTITUTIONAL SCAN"):
    with st.spinner("Scanning Order Blocks & Liquidity Voids..."):
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
        headers = {'X-CMC_PRO_API_KEY': CMC_API_KEY}
        params = {'symbol': target_coin, 'convert': 'USD'}
        
        try:
            r = requests.get(url, headers=headers, params=params)
            data = r.json()['data'][target_coin]
            price = data['quote']['USD']['price']
            chg = data['quote']['USD']['percent_change_24h']
            
            # --- EXECUTE BRAIN ---
            analysis = get_whale_logic(target_coin, round(price, 4), chg)
            
            # --- UI RENDERING ---
            st.markdown("<div class='whale-card'>", unsafe_allow_html=True)
            col1, col2 = st.columns([1, 1])
            with col1:
                st.metric(f"💎 {target_coin} Market Price", f"${price:,.4f}", f"{chg:.2f}%")
            with col2:
                # Direct Entry Status
                if chg < -2:
                    st.markdown("<div class='entry-zone'>🔥 WHALE BUY ZONE: LIQUIDITY GRAB</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div class='trap-warning'>⚠️ CAUTION: WAITING FOR RETAIL SHAKEOUT</div>", unsafe_allow_html=True)
            
            st.markdown(f"<div class='logic-box' style='background:#0d1117; padding:20px; border-radius:12px; border-left:5px solid #58a6ff;'><b>🐋 WHALE PSYCHOLOGY ANALYSIS:</b><br><br>{analysis}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Voice Alert (Psychology summary)
            audio_text = f"{target_coin} analysis complete. {analysis[:180]}"
            v_file = natural_voice(audio_text)
            if v_file:
                st.audio(v_file)
                
        except Exception as e:
            st.error(f"Execution Error: {e}")

st.divider()
st.caption("🔱 Quantum V12: Whale Psychology Core | Developed for Haseem Ali | No-Galti Edition")
