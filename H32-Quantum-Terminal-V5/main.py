with st.sidebar:
    st.header("📍 Watchlist")
    
    coins = [
        "BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT", "XRP/USDT",
        "DOGE/USDT", "ADA/USDT", "AVAX/USDT", "SUI/USDT", "LINK/USDT",
        "DOT/USDT", "UNI/USDT", "LTC/USDT", "ONDO/USDT", "HYPE/USDT",
        "ASTER/USDT", "ZEC/USDT", "BGB/USDT", "XPL/USDT"
    ]
    
    symbol = st.selectbox("Select Coin", coins)
    tf = st.selectbox("Timeframe", ["15m", "1h", "4h", "1d", "1w"])
