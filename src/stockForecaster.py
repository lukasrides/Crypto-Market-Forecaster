from nixtla import NixtlaClient
from dotenv import load_dotenv
import os
#import plotly.express as px
import cryptoHistoryHandler as chh
#from datetime import datetime, timezone,timedelta
import pandas as pd

# lodas env variables
load_dotenv()
nixtla_client = NixtlaClient(
    api_key = os.getenv('NIXTLA_API_KEY'),
)

# Initialize cryptoHistoryHandler (symbol,timeframe,lookback)
cryptoHandler = chh.cryptoHistoryHandler('BTC/USDT','1d',5)
#cryptoHandler.updateHistory() # Update history
history = cryptoHandler.getHistory()

# TODO: Add user Interface

# TODO: Create function
forecast = nixtla_client.forecast(history,
                                  h=14,
                                  level=[50,80,90],
                                  time_col='timestamp',
                                  target_col='close',
                                  freq='D'
                                  )

chart = nixtla_client.plot(history, forecast,
                           level=[50,80,90],
                           time_col='timestamp',
                           target_col='close',
                           max_insample_length=365,
                           engine='plotly') # Plot closing prices

chart.update_layout(title=f'{cryptoHandler.symbol} Closing Prices', width=2400, height=1200)
chart.show()


