import streamlit as st
import requests
import time
from datetime import datetime

st.set_page_config(page_title="SATELLITE-PRO V900", layout="wide")

st.markdown("""
<style>
    .main {background-color: #000000; color: #00f2ff;}
    .card {background: #0a1428; border: 2px solid #00f2ff; border-radius: 18px; padding: 20px; margin: 12px 0;}
    .entry {background: #00ff9d; color: black; padding: 12px; border-radius: 30px; text-align: center; font-weight: bold;}
    .wait {background: #ffaa00; color: black; padding: 12px; border-radius: 30px; text-align: center; font-weight: bold;}
    .sell {background: #ff3366; color: white; padding: 12px; border-radius: 30px; text-align: center; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

st.title("🔱 SATELLITE-PRO V900")
st.success("🛰️ FULL PSYCHOLOGY + SMART MONEY + MANIPULATION DETECTOR ACTIVE")

coins = ["BTC","ETH","SOL","SUI","XRP","BNB","AVAX","ONDO","HYPE","DOT","LINK"]

@st.cache_data(ttl=5)
def get_data():
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/24hr", timeout=6)
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
                    
                    # Psychology + Manipulation Logic
                    if chg <= -7 and vol > 250000000:
                        verdict = "🔴 HEAVY DISTRIBUTION / MANIPULATION"
                        suggestion = "Smart Money Exit Kar Raha Hai"
                        status = "sell"
                    elif chg > 5 and vol > 300000000:
                        verdict = "🟢 STRONG SMART MONEY ACCUMULATION"
                        suggestion = "Entry Leni Chahiye"
                        status = "entry"
                    elif chg > 3 and vol > 150000000:
                        verdict = "🟢 GOOD ENTRY ZONE"
                        suggestion = "Momentum Build Ho Raha Hai"
                        status = "entry"
                    else:
                        verdict = "🟡 WAIT - SIDEWAYS / TRAP POSSIBLE"
                        suggestion = "Abhi Entry Mat Lo"
                        status = "wait"
                    
                    target = price * 1.23 if chg > 0 else price * 0.88
                    
                    st.html(f"""
                    <div class="card">
                        <div style="display:flex; justify-content:space-between;">
                            <h2>{sym}/USDT</h2>
                            <h3 style="color:{'#00ff9d' if chg>0 else '#ff3366'}">{chg:+.2f}%</h3>
                        </div>
                        <h1 style="font-size:2.5rem;">${price:,.4f if price<1000 else :,.2f}</h1>
                        <div class="{status}">{verdict}</div>
                        <div style="margin-top:12px;">
                            <b>Suggestion:</b> {suggestion}<br>
                            <b>Target:</b> ${target:,.4f}
                        </div>
                    </div>
                    """)
        else:
            st.warning("Satellite Data Loading...")
        
        st.success(f"Live Update: {datetime.now().strftime('%H:%M:%S')}")
    
    time.sleep(6)
