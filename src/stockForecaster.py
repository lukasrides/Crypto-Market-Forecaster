from nixtla import NixtlaClient
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt
import plotly.express as px
import cryptoHistoryHandler as chh

# lodas env variables
load_dotenv()
# Initialize nixtla with my own API-Key TODO: Change to env file
nixtla_client = NixtlaClient(
    api_key = os.getenv('NIXTLA_API_KEY'),
)

# Initialize cryptoHistoryHandler (symbol,timeframe,lookback)
cryptoHandler = chh.cryptoHistoryHandler('BTC/USDT','1d',5)
#cryptoHandler.updateHistory() # Update history
history = cryptoHandler.getHistory()

"""forecast = nixtla_client.forecast(history,
                                  h=30,
                                  level=[50,80,90],
                                  time_col='timestamp',
                                  target_col='close',
                                  freq='D'
                                  )

chart = nixtla_client.plot(history, forecast,
                           time_col='timestamp',
                           target_col='close',
                           engine='plotly') # Plot closing prices
chart.update_layout(title=f'{cryptoHandler.symbol} Closing Prices')
chart.show()
"""

