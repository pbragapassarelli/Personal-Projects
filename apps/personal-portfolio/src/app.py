import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv('API_KEY')
MAX_REQUESTS_PER_MINUTE = 5
MAX_REQUESTS_PER_DAY = 500

MESSAGE_NOT_ON_PORTFOLIO = 'Asset is not on portfolio'
MESSAGE_TRYING_TO_SELL_MORE_THAN_AVAILABLE = 'Trying to sell more quantity than available'

def get_price_for_ticker(ticker, key=API_KEY):
    '''
    Receives a ticker and returns the current price
    
    ticker: str
    key: str
    ---------------------
    Returns: float
    '''

    import requests

    asset_ticker = f'{ticker}.SA'

    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={asset_ticker}&apikey={key}'

    data = requests.get(url).json()
    price = float(data['Global Quote']['05. price'])

    return price


class PortfolioAsset:
    '''
    ATTRIBUTES

    ticker: str
    quantity: float or int
    '''

    def __init__(self, ticker):
        self.ticker = ticker
        self.quantity = 0

    def get_attributes(self):
        '''
        Returns dict of relevant attributes, except ticker
        '''
        return {'quantity': self.quantity}


class Portfolio:
    '''
    ATTRIBUTES

    assets: dict of {'ticker': PortfolioAsset}
    -----------
    PUBLIC METHODS

    buy(ticker, quantity): buys asset on the desired quantity
    show(): returns portfolio dict
    '''

    def __init__(self):
        self.assets = {}

    def _add_new_asset(self, ticker):
        self.assets[ticker] = PortfolioAsset(ticker)

    def _get_asset_by_ticker(self, ticker):
        return self.assets[ticker]

    def buy(self, ticker, quantity):
        if ticker not in self.assets:
            self._add_new_asset(ticker)     
        
        asset = self._get_asset_by_ticker(ticker)
        asset.quantity += quantity

    def sell(self, ticker, quantity):
        if ticker not in self.assets:
            raise Exception(MESSAGE_NOT_ON_PORTFOLIO)

        asset = self._get_asset_by_ticker(ticker)

        if quantity > asset.quantity:
            raise Exception(MESSAGE_TRYING_TO_SELL_MORE_THAN_AVAILABLE)

        if quantity == asset.quantity:
            asset.quantity = 0
            self.assets.pop(ticker)
            return

        asset.quantity -= quantity 

    def show(self):
        return {asset.ticker: asset.get_attributes() for asset in self.assets.values()}




#TODO: implement asset search
#TODO: modularize app in files: Portfolio, Assets, API Client