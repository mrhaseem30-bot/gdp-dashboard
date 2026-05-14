import pandas as pd

class SMCEngine:
    def get_indicators(self, df):
        """Simple indicators without pandas_ta"""
        df = df.copy()
        # Simple moving average manually
        df['EMA21'] = df['close'].ewm(span=21, adjust=False).mean()
        # Simple RSI (basic version)
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        return df
    
    def detect_order_blocks(self, df):
        """Simple Order Block Detection"""
        return [{'type': 'Bullish OB', 'price': round(float(df['low'].tail(10).min()), 2)}]
    
    def detect_structure(self, df):
        return "Bullish Structure"
