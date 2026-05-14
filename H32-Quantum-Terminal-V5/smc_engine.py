import pandas as pd

class SMCEngine:
    def get_indicators(self, df):
        df = df.copy()
        df['EMA21'] = df['close'].ewm(span=21, adjust=False).mean()
        df['EMA50'] = df['close'].ewm(span=50, adjust=False).mean()
        
        # Simple RSI
        delta = df['close'].diff()
        gain = delta.where(delta > 0, 0).rolling(14).mean()
        loss = -delta.where(delta < 0, 0).rolling(14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        return df
    
    def detect_liquidity_grab(self, df):
        """Liquidity Grab Detection"""
        recent_high = df['high'].tail(30).max()
        recent_low = df['low'].tail(30).min()
        current_high = df['high'].iloc[-1]
        current_low = df['low'].iloc[-1]
        
        if abs(current_high - recent_high) < (recent_high * 0.002):  # 0.2% ke andar
            return "🔥 Upper Liquidity Grab (Sell Signal)"
        if abs(current_low - recent_low) < (recent_low * 0.002):
            return "🔥 Lower Liquidity Grab (Buy Signal)"
        return None
    
    def get_signal(self, df):
        lg = self.detect_liquidity_grab(df)
        last = df.iloc[-1]
        
        if lg and "Lower" in str(lg) and last['close'] > last['EMA21']:
            return "🟢 STRONG BUY", "Lower Liquidity Grab + Bullish EMA"
        elif lg and "Upper" in str(lg) and last['close'] < last['EMA21']:
            return "🔴 STRONG SELL", "Upper Liquidity Grab + Bearish EMA"
        elif last['close'] > last['EMA21'] and last['RSI'] < 65:
            return "🟡 BUY Setup", "Bullish Structure"
        else:
            return "⚪ Monitor", "Waiting for Liquidity or Break"
