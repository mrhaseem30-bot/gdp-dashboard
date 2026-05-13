import pandas as pd

def prepare_data(df):
    """Sab EMAs aur indicators ek baar mein calculate karo"""
    df = df.copy()
    if len(df) < 50:
        return df
    
    df['ema9'] = df['close'].ewm(span=9).mean()
    df['ema21'] = df['close'].ewm(span=21).mean()
    df['ema50'] = df['close'].ewm(span=50).mean()
    df['ema200'] = df['close'].ewm(span=200).mean()
    df['ma20'] = df['close'].rolling(window=20).mean()
    
    return df

def detect_market_structure(df):
    df = prepare_data(df)
    latest = df.iloc[-1]
    price = latest['close']
    
    if price > latest['ema9'] > latest['ema21'] > latest['ema50'] > latest.get('ema200', price):
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
    df = prepare_data(df)
    price = df['close'].iloc[-1]
    
    resistance = df['high'].rolling(window=10).max().iloc[-1]
    support = df['low'].rolling(window=10).min().iloc[-1]
    
    return {
        "current_price": round(price, 4),
        "strong_support": round(support, 2),
        "strong_resistance": round(resistance, 2),
        "liq_long_zone": round(support * 0.992, 2),
        "liq_short_zone": round(resistance * 1.008, 2),
        "long_entry": round(support * 1.003, 2),
        "short_entry": round(resistance * 0.997, 2),
        "suggested_sl": round(support * 0.975, 2)
    }

def calculate_confluence(df, price):
    df = prepare_data(df)
    score = 45
    reasons = ["Base Structure Checked"]
    
    if len(df) > 20:
        if price > df['ma20'].iloc[-1]:
            score += 25
            reasons.append("Price Above 20MA")
        if price > df['ema21'].iloc[-1]:
            score += 20
            reasons.append("Above EMA21")
        
        # Volume check
        if 'volume' in df.columns:
            vol_ma = df['volume'].rolling(20).mean().iloc[-1]
            if df['volume'].iloc[-1] > vol_ma * 1.7:
                score += 15
                reasons.append("Volume Surge")
    
    return min(score, 100), reasons
