import pandas as pd
import pandas_ta as ta
import numpy as np

class SMCEngine:
    def get_indicators(self, df):
        df = df.copy()
        df['EMA21'] = ta.ema(df['close'], 21)
        df['EMA50'] = ta.ema(df['close'], 50)
        df['RSI'] = ta.rsi(df['close'], 14)
        df['ATR'] = ta.atr(df['high'], df['low'], df['close'], 14)
        return df
    
    def detect_order_blocks(self, df):
        df = df.copy()
        swing = 5
        df['swing_low'] = df['low'] == df['low'].rolling(swing*2+1, center=True).min()
        df['swing_high'] = df['high'] == df['high'].rolling(swing*2+1, center=True).max()
        
        obs = []
        for i in range(10, len(df)-5):
            if df['swing_low'].iloc[i]:
                obs.append({'type': 'Bullish OB', 'price': round(float(df['low'].iloc[i]), 4), 'time': df['time'].iloc[i]})
            if df['swing_high'].iloc[i]:
                obs.append({'type': 'Bearish OB', 'price': round(float(df['high'].iloc[i]), 4), 'time': df['time'].iloc[i]})
        return obs[-5:]
    
    def detect_structure(self, df):
        recent_high = df['high'].tail(30).max()
        recent_low = df['low'].tail(30).min()
        current_high = df['high'].iloc[-1]
        current_low = df['low'].iloc[-1]
        
        if current_high > recent_high:
            return "BOS Bullish - Strong Momentum"
        if current_low < recent_low:
            return "BOS Bearish"
        return "Range / Waiting for Break"
