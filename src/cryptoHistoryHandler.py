import ccxt
import os 
import pandas as pd
import warnings
from datetime import datetime, timezone, timedelta
from tqdm import tqdm

warnings.simplefilter(action='ignore', category=FutureWarning)

class cryptoHistoryHandler:
    def __init__(self,symbol,timeframe):
        # Initialize exchange as Binance
        self.exchange = ccxt.binance()
        self.symbol = symbol
        self.timeframe = timeframe  # timeframe to inspect - 1d, 1h, 1m
        self.lookback = 5    # lookback in years
        self.symbolReplaced = self.symbol.replace('/','-')
        self.filename = f'{self.symbolReplaced}-{self.timeframe}-history.csv'
        self.savepath = os.path.join('src','history',self.filename)

    # method to load and store historic data of a specific currency
    def updateHistory(self):
        # 5 years is 0 to 4
        # Define column names
        columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        history = pd.DataFrame(columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        for years in tqdm(range(self.lookback),desc='Loading historical data'):
            startDate = datetime.now(tz=timezone.utc) - timedelta(days=365*(years+1))
            startDate = startDate.strftime('%Y-%m-%d %H:%M:%S')
            since = self.exchange.parse8601(startDate) 
            data = self.exchange.fetch_ohlcv(self.symbol, self.timeframe, since) # Fetch historical data
            dataFrame = pd.DataFrame(data, columns=columns) # put loaded data into DataFrame
            if self.timeframe == '1d':
                # Convert timestamps from ms to y-m-d H:M:S format
                dataFrame['timestamp'] = dataFrame['timestamp'].apply(
                    lambda time: datetime.fromtimestamp(time / 1000).strftime('%Y-%m-%d')
                )
                history['timestamp'] = pd.to_datetime(history['timestamp'],format='%Y-%m-%d')
            # TODO: Implement 1h and 1m timeframes
            """elif self.timeframe == '1h':
                # Convert timestamps from ms to y-m-d H:M:S format
                dataFrame['timestamp'] = dataFrame['timestamp'].apply(
                    lambda time: datetime.fromtimestamp(time / 1000).strftime('%Y-%m-%d %H')
                )
                history['timestamp'] = pd.to_datetime(history['timestamp'],format='%Y-%m-%d %H')
            elif self.timeframe == '1m':
                # Convert timestamps from ms to y-m-d H:M:S format
                dataFrame['timestamp'] = dataFrame['timestamp'].apply(
                    lambda time: datetime.fromtimestamp(time / 1000).strftime('%Y-%m-%d %H:%M')
                )
                history['timestamp'] = pd.to_datetime(history['timestamp'],format='%Y-%m-%d %H:%M')"""
            history = pd.concat([history,dataFrame],ignore_index=True)
        
        history['timestamp'] = pd.to_datetime(history['timestamp'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
        history.sort_values(by='timestamp',inplace=True,ascending=True) 
        history = history[~history['timestamp'].duplicated(keep='first')]
        history = history.dropna(subset=['timestamp'])  # Remove entries without timestamp
        history.to_csv(self.savepath) # save to csv

    # method to get the historic data of a specific symbol
    def getHistory(self):
        history = pd.read_csv(self.savepath, index_col=0)
        history['timestamp'] = pd.to_datetime(history['timestamp'], format='%Y-%m-%d', errors='coerce')
        return history

    # method to set the currently selected symbol
    def setSymbol(self,symbol):
        self.symbol = symbol
        self.symbolReplaced = self.symbol.replace('/','-')
        self.filename = f'{self.symbolReplaced}-{self.timeframe}-history.csv'
        self.savepath = os.path.join('src','history',self.filename)

    # TODO: Implement 1h and 1m timeframes
    # method to set the currently selected timeframe
    def setTimeframe(self,timeframe):
        self.timeframe = timeframe
        self.filename = f'{self.symbolReplaced}-{self.timeframe}-history.csv'
        self.savepath = os.path.join('src','history',self.filename)



