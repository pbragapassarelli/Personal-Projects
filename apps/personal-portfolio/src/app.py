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
    average_price: float
    amount_invested: float
    '''

    def __init__(
        self, 
        ticker,
        quantity=0,
        amount_invested=0
    ):
        self.ticker = ticker
        self.quantity = quantity
        self.average_price = amount_invested / quantity if quantity > 0 else 0
        self.amount_invested = amount_invested

    def get_attributes(self):
        '''
        Returns dict of relevant attributes, except ticker
        '''
        return {
            'quantity': self.quantity,
            'average_price': self.average_price,
            'amount_invested': self.amount_invested
        }


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

    def buy(self, ticker, quantity, price):
        if ticker not in self.assets:
            self._add_new_asset(ticker)     
        
        asset = self._get_asset_by_ticker(ticker)
        
        asset.quantity += quantity
        asset.amount_invested += quantity * price
        asset.average_price = asset.amount_invested / asset.quantity

    def sell(self, ticker, quantity, price):
        if ticker not in self.assets:
            raise Exception(MESSAGE_NOT_ON_PORTFOLIO)

        asset = self._get_asset_by_ticker(ticker)

        if quantity > asset.quantity:
            raise Exception(MESSAGE_TRYING_TO_SELL_MORE_THAN_AVAILABLE)

        asset.quantity -= quantity
        asset.amount_invested -= quantity * asset.average_price

        if asset.quantity == 0:
            self.assets.pop(ticker)

    def show(self):
        return {asset.ticker: asset.get_attributes() for asset in self.assets.values()}
        