import os
from dotenv import load_dotenv

load_dotenv()

CONFIG = {
    "risk_percent": 1.0,
    "watchlist": ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT"],
    "timeframes": ["15m", "1h", "4h", "1d"],
    "default_tf": "4h"
}
