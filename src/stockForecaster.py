from nixtla import NixtlaClient
import logging
from dotenv import load_dotenv
import warnings
import os
import cryptoHistoryHandler as chh
import inquirer
from prophet import Prophet
from prophet.plot import plot_plotly
import pandas as pd

# Set logging level to ERROR to suppress info and debug messages
logging.getLogger('nixtla').setLevel(logging.ERROR)
# Suppress specific warnings
warnings.filterwarnings("ignore", message="`df` contains the following exogenous features")

def setParameters():
    choices = [
    inquirer.List(
        'action',
        message='Please select the desired symbol.',
        choices=['BTC/USDT','ETH/USDT','XRP/USDT','IOTA/USDT'],
    ),
    ]
    selection = inquirer.prompt(choices)
    cryptoHandler.setSymbol(selection['action'])

    # TODO: Add timeframe selection
    """# set timeframe
    choices = [
    inquirer.List(
        'action',
        message='Please select the desired timeframe.',
        choices=['1h','1d','1m'],
    ),
    ]
    selection = inquirer.prompt(choices)
    cryptoHandler.setTimeframe(selection['action'])"""

def forecast():
    print('\nForecasting... 📉📈')
    history = cryptoHandler.getHistory()

    # create prophet prediction
    prophetDataFrame = pd.DataFrame(columns=['ds','y'])
    prophetDataFrame['ds'] = history['timestamp']
    prophetDataFrame['y'] = history['close']
    prophet.fit(prophetDataFrame)
    futureDataFrame = prophet.make_future_dataframe(periods=14) # creates future dataFrame for 14 days ahead
    prophetForecast = prophet.predict(futureDataFrame)
    prophetForecast.rename(columns={'ds':'timestamp','yhat':'close'},inplace=True)

    # create nixtla prediction
    nixtlaForecast = nixtla_client.forecast(history,
                                h=14,
                                level=[50,80,90],
                                time_col='timestamp',
                                target_col='close',
                                freq='D'
                                )

    # create nixtla plot
    chartNixtla = nixtla_client.plot(history, nixtlaForecast,
                            level=[50,80,90],
                            time_col='timestamp',
                            target_col='close',
                            max_insample_length=365,
                            engine='plotly') # Plot closing prices
    # create prophet plot    
    chartProphet = nixtla_client.plot(history, prophetForecast,
                        time_col='timestamp',
                        target_col='close',
                        max_insample_length=365,
                        engine='plotly') # Plot closing prices
    
    chartNixtla.update_layout(title=f'{cryptoHandler.symbol} Closing Price (TimeGPT)', width=2400, height=1200)
    chartNixtla.show()
    chartProphet.update_layout(title=f'{cryptoHandler.symbol} Closing Prices (Prophet)', width=2400, height=1200)
    chartProphet.show()


    print('\nPlot opened in a browser window. 🚀🌕\n')



# lodas env variables
load_dotenv()
nixtla_client = NixtlaClient(
    api_key = os.getenv('NIXTLA_API_KEY'),
)

prophet = Prophet()

# Initialize cryptoHistoryHandler (symbol,timeframe,lookback)
cryptoHandler = chh.cryptoHistoryHandler('BTC/USDT','1d')
quit = False

while not quit:
    print(f'\n₿₿ Welcome to the Crypto Forecaster! ₿₿ \n\n Currently selected symbol: {cryptoHandler.symbol}\n Currently selected timeframe: {cryptoHandler.timeframe}\n ')
    choices = [
        inquirer.List(
            'action',
            message='What would you like to do?',
            choices=['Set Parameters','Update History','Forecast','Quit'],
        ),
    ]
    selection = inquirer.prompt(choices)

    match selection['action']:
        case 'Set Parameters':
            setParameters() # Set parameters
        case 'Update History':
            cryptoHandler.updateHistory() # Update history
        case 'Forecast':
            if not os.path.exists(cryptoHandler.savepath):
                print('No history available. Starting update...')
                cryptoHandler.updateHistory()
            forecast()
        case 'Quit':
            quit = True
            print('Goodbye!')







