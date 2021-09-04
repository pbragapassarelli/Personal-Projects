import pytest

from app import get_price_for_ticker

from app import PortfolioAsset, Portfolio


def test_get_price_for_ticker():
    answer = get_price_for_ticker('ITSA4')

    assert type(answer) == float


def test_buy_asset_for_first_time():
    portfolio = Portfolio()
    ticker = 'ITSA4'
    qty = 100

    portfolio.buy(ticker, qty)

    assert portfolio.assets[ticker].quantity == qty