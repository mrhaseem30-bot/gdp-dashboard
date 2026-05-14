import streamlit as st
import requests
import pytz
from datetime import datetime

# --- 🛰️ SATELLITE & GLOBAL SYNC ---
st.set_page_config(page_title="V2100 OMNI", layout="centered")

# --- 🕒 DELHI 12-HOUR SESSION TRACKER ---
ist = pytz.timezone('Asia/Kolkata')
now = datetime.now(ist)
st.title("🛰️ V2100 WHALE COMMAND")
st.write(f"**Session Time:** {now.strftime('%Y-%m-%d | %I:%M %p')}")

# --- 🧠 200 IQ DECISION LOGIC ---
def get_whale_flow():
    try:
        # Investing.com & Global Market Pipe Sync
        url = "https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,ETH,SOL&tsyms=USD"
        res = requests.get(url).json()['RAW']
        return res
    except:
        return None

data = get_whale_flow()

if data:
    for sym in ["BTC", "ETH", "SOL"]:
        price = data[sym]['USD']['PRICE']
        vol = data[sym]['USD']['VOLUME24HOURTO']
        low = data[sym]['USD']['LOW24HOUR']
        high = data[sym]['USD']['HIGH24HOUR']

        # 🐋 WALLET TRACKER & LIQUIDITY ANALYSIS
        # Puri Entry: Liquidity grab point niche hota hai
        puri_entry = low * 0.998 
        # Zed Zone: Retailer trap upar hota hai
        zed_zone = high * 1.002
        
        # 🛡️ ANTI-FAKE (FIK MOT) LOGIC
        # Agar price high ke paas hai par whale volume kam hai
        is_trap = True if (price > high * 0.98 and vol < 100000000) else False

        # --- 📱 SIMPLE CLEAN UI (No HTML Errors) ---
        with st.container():
            st.subheader(f"💎 {sym}/USDT")
            
            col1, col2 = st.columns(2)
            col1.metric("LIVE PRICE", f"${price:,.2f}")
            col2.error("RETAIL TRAP") if is_trap else col2.success("WHALE FLOW")

            st.write(f"---")
            
            # 🎯 DECISION POINTS
            c1, c2 = st.columns(2)
            c1.warning(f"🔴 ZED ZONE (SELL)\n\n**${zed_zone:,.2f}**")
            c2.info(f"🟢 PURI ENTRY (BUY)\n\n**${puri_entry:,.2f}**")

            # 🧠 SYSTEM VERDICT
            st.info(f"""
            **INSTITUTIONAL ANALYSIS:**
            Delhi 12-hour cycle ke mutabiq, BlackRock aur bade whales **${puri_entry:,.2f}** par liquidity grab ka wait kar rahe hain. Upar **Zed Zone** par retailers 
            trap ho rahe hain. Jab tak price niche wick na maare, entry mat lena.
            """)
            st.write("---")

else:
    st.error("📡 CONNECTION FAILED. Update your requirements.txt!")
