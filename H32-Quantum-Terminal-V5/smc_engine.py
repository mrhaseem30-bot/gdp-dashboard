import pandas as pd
import json
import os
from datetime import datetime

LOG_FILE = "analysis_log.json"

def load_learning_data():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            return json.load(f)
    return {"total_analysis": 0, "high_accuracy": []}

def save_learning(coin, decision, score, actual_result="pending"):
    data = load_learning_data()
    data["total_analysis"] += 1
    data.setdefault("coins", {})
    data["coins"][coin] = {
        "last_decision": decision,
        "score": score,
        "timestamp": str(datetime.now())
    }
    with open(LOG_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_quantum_decision(df, symbol):
    df = prepare_data(df)  # pehle wala prepare_data function
    price = float(df['close'].iloc[-1])
    support = float(df['low'].rolling(8).min().iloc[-1])
    resistance = float(df['high'].rolling(8).max().iloc[-1])
    
    score = 50
    reasons = []
    decision = "HOLD"
    
    # Advanced Logic
    if price > df['ema21'].iloc[-1] and price > df['ma20'].iloc[-1]:
        score += 35
        reasons.append("Bullish Alignment")
        decision = "BUY"
    
    if price < support * 1.006:
        score += 30
        reasons.append("Strong Support + Possible Whale Buy")
        decision = "STRONG BUY"
    
    if 'rsi' in df.columns and df['rsi'].iloc[-1] < 35:
        reasons.append("Oversold Condition")
    
    early_alert = f"{symbol} → {decision} | Next 1-3 hours high probability"

    # Learning Save
    save_learning(symbol, decision, score)
    
    return {
        "coin": symbol,
        "decision": decision,
        "score": min(score, 100),
        "price": round(price, 2),
        "support": round(support, 2),
        "resistance": round(resistance, 2),
        "early_alert": early_alert,
        "reasons": reasons
    }
