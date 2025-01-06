import ccxt
import os 
import pandas as pd
import warnings
from datetime import datetime, timezone, timedelta

warnings.simplefilter(action='ignore', category=FutureWarning)

class cryptoHistoryHandler:
    def __init__(self,symbol,timeframe,lookback):
        # Initialize exchange as Binance
        self.exchange = ccxt.binance()
        self.symbol = symbol
        self.timeframe = timeframe  # timeframe to inspect - 1d, 1h, 1m
        self.lookback = lookback    # lookback in years
        self.symbolReplaced = self.symbol.replace('/','-')
        self.filename = f'{self.symbolReplaced}-{self.timeframe}-{self.lookback}-history.csv'
        self.savepath = os.path.join('src','history',self.filename)

    # method to load and store historic data of a specific currency
    def updateHistory(self):
        # 5 years is 0 to 4
        # Define column names
        columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        history = pd.DataFrame(columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        for years in range(self.lookback):
            startDate = datetime.now(tz=timezone.utc) - timedelta(days=365*(years+1))
            startDate = startDate.strftime('%Y-%m-%d %H:%M:%S')
            since = self.exchange.parse8601(startDate) 
            data = self.exchange.fetch_ohlcv(self.symbol, self.timeframe, since) # Fetch historical data
            dataFrame = pd.DataFrame(data, columns=columns) # put loaded data into DataFrame
            # Convert timestamps from ms to y-m-d H:M:S format
            dataFrame['timestamp'] = dataFrame['timestamp'].apply(
                lambda time: datetime.fromtimestamp(time / 1000).strftime('%Y-%m-%d')
            )
            history = pd.concat([history,dataFrame],ignore_index=True)
        history['timestamp'] = pd.to_datetime(history['timestamp'],format='%Y-%m-%d')
        history.sort_values(by='timestamp',inplace=True,ascending=True) 
        history = history[~history['timestamp'].duplicated(keep='first')]
        history.to_csv(self.savepath) # save to csv

    # method to get the historic data of a specific symbol
    def getHistory(self):
        return pd.read_csv(self.savepath, index_col=0)

    # method to set the currently selected symbol
    def setSymbol(self,symbol):
        self.symbol = symbol
        self.savepath = f'src\history\{self.symbol}-{self.timeframe}-history.csv'
    
    # method to set the currently selected timeframe
    def setTimeframe(self,timeframe):
        self.timeframe = timeframe
    
    # method to set the currently selected lookback
    def setLookback(self,lookback):
        self.lookback = lookback


