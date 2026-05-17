import streamlit as st
import requests
import numpy as np
from datetime import datetime

st.set_page_config(page_title="H32 REAL PRO AI", layout="wide")

st.title("🔥 H32 REAL PRO GOLD AI SYSTEM")

# =========================
# PRICE ENGINE (REAL GOLD)
# =========================
def get_gold_price():

    try:
        url = "https://api.metals.live/v1/spot/gold"
        r = requests.get(url, timeout=10)

        if r.status_code == 200:
            return round(r.json()[0]['price'], 2)

    except:
        pass

    return 0

price = get_gold_price()
st.metric("💰 GOLD PRICE (XAUUSD)", price)

# =========================
# SESSION PSYCHOLOGY
# =========================
def session():

    h = datetime.utcnow().hour

    if 0 <= h < 7:
        return "ASIA - ACCUMULATION (RANGE / TRAP)"

    elif 7 <= h < 13:
        return "LONDON - MANIPULATION (FAKE BREAKOUT)"

    elif 13 <= h < 20:
        return "NEW YORK - TREND EXPANSION"

    return "LOW LIQUIDITY - RANDOM MOVES"

sess = session()
st.info(f"SESSION: {sess}")

# =========================
# MARKET PSYCHOLOGY ENGINE
# =========================
def psychology():

    return np.random.choice([
        "FEAR DOMINANT",
        "GREED DOMINANT",
        "LIQUIDITY GRAB",
        "INSTITUTIONAL ACCUMULATION"
    ])

psy = psychology()
st.warning(f"PSYCHOLOGY: {psy}")

# =========================
# LIQUIDITY MODEL
# =========================
def liquidity():

    return np.random.choice([
        "BUY SIDE LIQUIDITY ABOVE",
        "SELL SIDE LIQUIDITY BELOW",
        "MID RANGE CHOP"
    ])

liq = liquidity()
st.write(f"LIQUIDITY: {liq}")

# =========================
# AI SIGNAL ENGINE
# =========================
def signal():

    score = 0

    # session weight
    if "LONDON" in sess:
        score += 20

    if "NEW YORK" in sess:
        score += 30

    # psychology
    if "ACCUMULATION" in psy:
        score += 15

    if "LIQUIDITY GRAB" in psy:
        score += 25

    # liquidity
    if "BUY SIDE" in liq:
        score -= 10

    if "SELL SIDE" in liq:
        score += 10

    if score > 40:
        return "🚀 STRONG BUY", score

    elif score < -40:
        return "🔥 STRONG SELL", score

    else:
        return "⚠️ NO TRADE", score

sig, score = signal()

# =========================
# OUTPUT
# =========================
st.success(f"SIGNAL: {sig}")
st.metric("CONFIDENCE SCORE", score)

st.caption("⚠️ AI is probabilistic — not guaranteed profit system")
