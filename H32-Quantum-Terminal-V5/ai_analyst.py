class AIAnalyst:
    def analyze(self, df, obs):
        score = 50
        last = df.iloc[-1]
        
        if last['close'] > last['EMA21']: score += 20
        if last['RSI'] < 40: score += 15
        if last['RSI'] > 70: score -= 20
        
        bullish_ob = any(o['type'] == 'Bullish OB' for o in obs)
        if bullish_ob: score += 25
        
        confidence = max(30, min(95, score))
        
        if confidence >= 78:
            return {"signal": "🟢 STRONG BUY", "confidence": confidence, "reason": "SMC + Momentum Confirmed"}
        elif confidence >= 65:
            return {"signal": "🟡 Good Setup", "confidence": confidence, "reason": "Bullish Structure"}
        else:
            return {"signal": "🔴 Avoid", "confidence": confidence, "reason": "Weak or Risky"}
