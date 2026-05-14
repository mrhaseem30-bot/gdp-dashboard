import streamlit as st
import requests
import time
from datetime import datetime
import random

st.set_page_config(page_title="H32 SATELLITE-PRO V900", layout="wide")

st.markdown("""
<style>
    .main {background-color: #000000; color: #00f2ff; font-family: 'Courier New', monospace;}
    .card {background: #0a1428; border: 2px solid #00f2ff; border-radius: 18px; padding: 22px; margin: 14px 0;}
    .entry {background: #00ff9d; color: black; padding: 12px; border-radius: 30px; text-align: center; font-weight: bold;}
    .wait {background: #ffaa00; color: black; padding: 12px; border-radius: 30px; text-align: center; font-weight: bold;}
    .sell {background: #ff3366; color: white; padding: 12px; border-radius: 30px; text-align: center; font-weight: bold;}
    .header {font-size: 2.6rem; font-weight: 900; text-align: center; margin-bottom: 8px;}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='header'>🔱 SATELLITE-PRO V900</h1>", unsafe_allow_html=True)
st.success("🛰️ FULL PSYCHOLOGY + SMART MONEY + MANIPULATION DETECTOR ACTIVE")

coins = ["BTC","ETH","SOL","SUI","XRP","BNB","AVAX","ONDO","HYPE","DOT","LINK"]

@st.cache_data(ttl=5)
def get_data():
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/24hr", timeout=5)
        if r.status_code == 200:
            return {item['symbol'].replace('USDT',''): item for item in r.json() if item['symbol'].endswith('USDT')}
    except:
        pass
    return {}

data = get_data()

placeholder = st.empty()

while True:
    with placeholder.container():
        if data:
            for sym in coins:
                if sym in data:
                    d = data[sym]
                    price = float(d['lastPrice'])
                    chg = float(d['priceChangePercent'])
                    vol = float(d['quoteVolume'])
                    
                    liq = min(98, int(vol / 8000000))
                    momentum = chg * (vol / 100000000)
                    
                    # Advanced Psychology Engine
                    if chg <= -7 and vol > 280000000:
                        verdict = "🔴 HEAVY DISTRIBUTION / MANIPULATION"
                        suggestion = "Smart Money Selling - Urgent Exit"
                        status = "sell"
                    elif chg > 4.5 and vol > 350000000 and liq > 78:
                        verdict = "🟢 INSTITUTIONAL ACCUMULATION"
                        suggestion = "Entry Leni Chahiye - Big Players Buying"
                        status = "entry"
                    elif momentum > 22 and chg > 3:
                        verdict = "🟢 HIGH PROBABILITY MOMENTUM"
                        suggestion = "Strong Retail + Smart Money Flow"
                        status = "entry"
                    elif chg < -4 and vol > 250000000:
                        verdict = "🟡 POSSIBLE FAKE DUMP / TRAP"
                        suggestion = "Abhi Mat Enter Karo - Manipulation Ho Sakta Hai"
                        status = "wait"
                    else:
                        verdict = "🟡 NEUTRAL - ACCUMULATION PHASE"
                        suggestion = "Clear Signal Nahi - Wait Karo"
                        status = "wait"
                    
                    target = price * 1.24 if chg > 0 else price * 0.87
                    
                    st.html(f"""
                    <div class="card">
                        <div style="display:flex; justify-content:space-between;">
                            <h2>{sym}/USDT</h2>
                            <h3 style="color:{'#00ff9d' if chg>0 else '#ff3366'}">{chg:+.2f}%</h3>
                        </div>
                        <h1 style="font-size:2.5rem; margin:8px 0;">${price:,.4f if price<1000 else :,.2f}</h1>
                        
                        <div class="{status}">{verdict}</div>
                        
                        <div style="margin-top:15px; background:#112233; padding:15px; border-radius:12px;">
                            <b>Suggestion:</b> {suggestion}<br><br>
                            <b>Target:</b> ${target:,.4f} | Confidence: {min(97, int(48 + abs(chg)*3.5 + vol/12000000))}%
                        </div>
                    </div>
                    """)
        
        st.success(f"✅ Live Psychology Update: {datetime.now().strftime('%H:%M:%S')}")
    
    time.sleep(6)
