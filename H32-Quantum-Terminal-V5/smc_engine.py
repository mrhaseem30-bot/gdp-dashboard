import pandas as pd

def detect_market_structure(df):
    # Simple logic without pandas_ta
    df['ema20'] = df['close'].ewm(span=20).mean()
    df['ema50'] = df['close'].ewm(span=50).mean()
    
    latest = df.iloc[-1]
    if latest['close'] > latest['ema20'] > latest['ema50']:
        structure = "Bullish"
    elif latest['close'] < latest['ema20']:
        structure = "Bearish"
    else:
        structure = "Neutral"
    return structure, df

def calculate_confluence(df, price):
    score = 50  # default
    reasons = ["Basic Structure Checked"]
    
    if df['close'].iloc[-1] > df['close'].rolling(20).mean().iloc[-1]:
        score += 30
        reasons.append("Price Above MA")
    
    return min(score, 100), reasons
