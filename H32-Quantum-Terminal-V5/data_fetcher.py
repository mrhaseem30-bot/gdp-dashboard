import ccxt
import pandas as pd
from datetime import datetime

class DataFetcher:
    def __init__(self):
        self.exchange = ccxt.binance({
            'enableRateLimit': True,
        })
    
    def get_ohlcv(self, symbol, timeframe="4h", limit=300):
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['time'] = pd.to_datetime(df['timestamp'], unit='ms')
            return df[['time', 'open', 'high', 'low', 'close', 'volume']]
        except Exception as e:
            print(f"Error fetching {symbol}: {e}")
            return None
    
    def get_global_tickers(self):
        """Puri market ka overview"""
        try:
            tickers = self.exchange.fetch_tickers()
            return pd.DataFrame([{
                'symbol': k,
                'price': v['last'],
                'change': v['percentage']
            } for k, v in list(tickers.items())[:50]])
        except:
            return pd.DataFrame()
