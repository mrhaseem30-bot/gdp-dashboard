import ccxt
import pandas as pd

class DataFetcher:
    def __init__(self):
        self.exchange = ccxt.binance({'enableRateLimit': True})
    
    def get_ohlcv(self, symbol, timeframe="4h", limit=200):
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['time'] = pd.to_datetime(df['timestamp'], unit='ms')
            return df[['time', 'open', 'high', 'low', 'close', 'volume']]
        except:
            return None
