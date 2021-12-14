import os
import time
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv('API_KEY')
MAX_REQUESTS_PER_MINUTE = 5
MAX_REQUESTS_PER_DAY = 500

SECONDS_IN_A_MINUTE = 60

MESSAGE_NOT_ON_PORTFOLIO = 'Asset is not on portfolio'
MESSAGE_TRYING_TO_SELL_MORE_THAN_AVAILABLE = \
    'Trying to sell more quantity than available'


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
    current_price: float
    current_exposition: float
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
        self.current_price = 0
        self.current_exposition = self.current_price * self.quantity

    def get_attributes(self):
        '''
        Returns dict of relevant attributes, except ticker
        '''
        return {
            'quantity': self.quantity,
            'average_price': self.average_price,
            'amount_invested': self.amount_invested,
            'current_price': self.current_price,
            'current_exposition': self.current_exposition
        }

    def update_price_and_exposition(self):
        # TODO: Como testar?
        self.current_price = get_price_for_ticker(self.ticker)
        self.current_exposition = self.current_price * self.quantity


class Portfolio:
    '''
    ATTRIBUTES

    assets: list of PortfolioAsset elements
    '''

    def __init__(self):
        self.assets = []

    def _add_new_asset(self, ticker):
        self.assets.append(PortfolioAsset(ticker))

    def _get_asset_by_ticker(self, ticker):
        return next(filter(lambda x: x.ticker == ticker,  self.assets), None)

    def _has(self, ticker):
        return not self._get_asset_by_ticker(ticker) is None

    def buy(self, ticker, quantity, price):
        if not self._has(ticker):
            self._add_new_asset(ticker)

        asset = self._get_asset_by_ticker(ticker)

        asset.quantity += quantity
        asset.amount_invested += quantity * price
        asset.average_price = asset.amount_invested / asset.quantity

    def sell(self, ticker, quantity, price):
        if not self._has(ticker):
            raise Exception(MESSAGE_NOT_ON_PORTFOLIO)

        asset = self._get_asset_by_ticker(ticker)

        if quantity > asset.quantity:
            raise Exception(MESSAGE_TRYING_TO_SELL_MORE_THAN_AVAILABLE)

        asset.quantity -= quantity
        asset.amount_invested -= quantity * asset.average_price

        if asset.quantity == 0:
            # TODO: é responsabilidade do sell() remover o ativo da carteira?
            self.assets.remove(asset)

    def update(self):
        # TODO: como testar?
        i = 0
        for asset in self.assets:
            i += 1
            asset.update_price_and_exposition()
            if i < len(self.assets):
                time.sleep(SECONDS_IN_A_MINUTE/MAX_REQUESTS_PER_MINUTE)

    def show(self):
        return {asset.ticker: asset.get_attributes() for asset in self.assets}
