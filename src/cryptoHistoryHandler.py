import ccxt
import pandas as pd
import numpy as np
from datetime import datetime, timezone, timedelta


class cryptoHistoryHandler:
    def __init__(self,symbol,timeframe,lookback):
        # Initialize exchange as Binance
        self.exchange = ccxt.binance()
        self.symbol = symbol
        self.timeframe = timeframe  # timeframe to inspect 
        self.lookback = lookback    # lookback in years
        self.savepath = f'src\history\{self.symbol}-history.csv'

    # method to load and store historic data of a specific currency
    def updateHistory(self):
        # 5 years is 0 to 4
        history = pd.DataFrame()
        tempHistory = np.array()
        for years in range(self.lookback):
            startDate = datetime.now(tz=timezone.utc).strftime('%Y-%m-%dT00:00:00Z') - timedelta(days=365)
            since = self.exchange.parse8601(startDate) 
            # Fetch historical data
            data = self.exchange.fetch_ohlcv(self.symbol, self.timeframe, since)
            # TODO: Store data
    
    def setSymbol(self,symbol):
        self.symbol = symbol
        self.savepath = f'src\history\{self.symbol}-history.csv'
    
    def setTimeframe(self,timeframe):
        self.timeframe = timeframe
    
    def setLookback(self,lookback):
        self.lookback = lookback




# Fetch historical OHLCV (Open, High, Low, Close, Volume)
symbol = 'BTC/USDT'  # BTC to USDT
timeframe = '1d'  # Daily data
since = exchange.parse8601('2024-01-01T00:00:00Z')  # Start date

# Fetch historical data
data = exchange.fetch_ohlcv(symbol, timeframe, since)

# Print data (timestamp, open, high, low, close, volume)
for row in data:
    print(datetime.fromtimestamp(float(row[0])/1000,tz=timezone.utc).strftime('%Y-%m-%d'),row[1:])
