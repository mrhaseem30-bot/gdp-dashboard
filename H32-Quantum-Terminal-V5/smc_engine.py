import pandas as pd
import numpy as np

def detect_market_structure(df):
    df = df.copy()
    df['ema9'] = df['close'].ewm(span=9).mean()
    df['ema21'] = df['close'].ewm(span=21).mean()
    df['ema50'] = df['close'].ewm(span=50).mean()
    df['ema200'] = df['close'].ewm(span=200).mean()
    
    latest = df.iloc[-1]
    price = latest['close']
    
    if price > latest['ema9'] > latest['ema21'] > latest['ema50'] > latest['ema200']:
        structure = "STRONG BULLISH"
        bias = "Uptrend"
    elif price < latest['ema21']:
        structure = "BEARISH"
        bias = "Downtrend"
    else:
        structure = "NEUTRAL / CONSOLIDATION"
        bias = "Sideways"
    
    return {"structure": structure, "bias": bias, "price": round(price, 4)}

def get_key_levels(df):
    price = df['close'].iloc[-1]
    # Swing High/Low
    resistance = df['high'].rolling(window=10).max().iloc[-1]
    support = df['low'].rolling(window=10).min().iloc[-1]
    
    return {
        "current_price": round(price, 4),
        "strong_support": round(support, 2),
        "strong_resistance": round(resistance, 2),
        "liq_long_zone": round(support * 0.992, 2),   # Longs liquidate yahan
        "liq_short_zone": round(resistance * 1.008, 2), # Shorts liquidate
        "long_entry": round(support * 1.003, 2),
        "short_entry": round(resistance * 0.997, 2),
        "suggested_sl": round(support * 0.975, 2) if price > support else round(resistance * 1.025, 2)
    }

def calculate_confluence(df, price):
    score = 45
    reasons = ["Base Structure"]
    
    if price > df['close'].rolling(20).mean().iloc[-1]:
        score += 25
        reasons.append("Price > 20MA")
    if price > df['ema21'].iloc[-1]:
        score += 20
        reasons.append("Above EMA21")
    if 'volume' in df.columns and len(df) > 20:
        vol_ma = df['volume'].rolling(20).mean().iloc[-1]
        if df['volume'].iloc[-1] > vol_ma * 1.8:
            score += 15
            reasons.append("High Volume Surge")
    
    return min(score, 100), reasons
