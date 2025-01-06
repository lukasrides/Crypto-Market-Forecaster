# Stock-Market-Forecaster
A python command line user interface that can be used to load the historic prices of BTC, ETH, IOTA and XRP and do a 14 day prediction of the price charts using nixtla timeGPT.

## Installation
First, create a new python virtual environment (tested on 3.11.9). Then install required dependencies using pip.
```pip install -r requirements.txt ```

## Usage
The command line interface will prompt the user for the desired action. 'Set Parameters' lets the user selec the desired symbol. 'Update History' downloads the last 5 years of data to the ./history folder. 'Forecast' predicts the upcoming 14 days based on the stored history. If no .csv file holding the history is present, it will be automatically downloaded first.
