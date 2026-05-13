import pandas as pd

def prepare_data(df):
    df = df.copy()
    if len(df) < 30:
        return df
    df['ema9'] = df['close'].ewm(span=9).mean()
    df['ema21'] = df['close'].ewm(span=21).mean()
    df['ema50'] = df['close'].ewm(span=50).mean()
    df['ma20'] = df['close'].rolling(20).mean()
    # RSI
    delta = df['close'].diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = abs(delta.clip(upper=0)).rolling(14).mean()
    rs = gain / loss
    df['rsi'] = 100 - (100 / (1 + rs))
    return df

def get_quantum_decision(df, symbol):
    df = prepare_data(df)
    price = float(df['close'].iloc[-1])
    support = float(df['low'].rolling(8).min().iloc[-1])
    resistance = float(df['high'].rolling(8).max().iloc[-1])
    
    score = 48
    reasons = []
    decision = "HOLD"
    urgency = "Normal"
    
    if price > df['ema21'].iloc[-1] and price > df['ma20'].iloc[-1]:
        score += 32
        reasons.append("Bullish Structure + EMA Alignment")
        decision = "BUY"
        urgency = "High"
    
    if price < support * 1.006:
        score += 28
        reasons.append("Strong Support Zone - Accumulation Possible")
        decision = "STRONG BUY"
        urgency = "High"
    
    if 'rsi' in df.columns:
        rsi = df['rsi'].iloc[-1]
        if rsi < 35:
            reasons.append("RSI Oversold - Bounce Expected")
    
    if price < df['ema21'].iloc[-1]:
        score -= 20
        reasons.append("Bearish Pressure")
        decision = "CAUTION / SELL"
    
    early_alert = f"Next 1-3 hours mein {decision} signal strong hai."
    
    return {
        "coin": symbol,
        "decision": decision,
