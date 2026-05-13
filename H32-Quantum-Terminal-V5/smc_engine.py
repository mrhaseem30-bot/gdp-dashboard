import pandas as pd
import pandas_ta as ta

def detect_market_structure(df):
    df['ema20'] = ta.ema(df['close'], 20)
    df['ema50'] = ta.ema(df['close'], 50)
    df['rsi'] = ta.rsi(df['close'])
    
    latest = df.iloc[-1]
    structure = "Bullish" if latest['close'] > latest['ema20'] > latest['ema50'] else "Bearish" if latest['close'] < latest['ema20'] else "Neutral"
    return structure, df

def calculate_confluence(df, price):
    score = 0
    reasons = []
    
    if df['ema20'].iloc[-1] > df['ema50'].iloc[-1]:
        score += 25
        reasons.append("EMA Bullish Alignment")
    
    if 40 < df['rsi'].iloc[-1] < 75:
        score += 20
        reasons.append("RSI Healthy Range")
    
    vol_avg = df['volume'].rolling(20).mean().iloc[-1]
    if df['volume'].iloc[-1] > vol_avg * 1.4:
        score += 20
        reasons.append("Strong Volume Confirmation")
    
    recent_low = df['low'].rolling(30).min().iloc[-1]
    if price > recent_low * 1.008:
        score += 25
        reasons.append("Above Key Support")
    
    return min(score, 100), reasons
