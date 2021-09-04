import pytest

from app import get_price_for_ticker
from app import PortfolioAsset, Portfolio


# def test_get_price_for_ticker():
#     answer = get_price_for_ticker('ITSA4')

#     assert type(answer) == float


def test_buy_asset_for_first_time():
    portfolio = Portfolio()
    ticker = 'ITSA4'
    qty = 100

    portfolio.buy(ticker, qty)

    assert portfolio.assets[ticker].quantity == qty


def test_buy_existing_asset():
    portfolio = Portfolio()
    
    ticker = 'ITSA4'
    qty = 100
    asset = PortfolioAsset(ticker)
    asset.quantity = qty
    portfolio.assets[ticker] = asset
    
    new_qty = 200
    portfolio.buy(ticker, new_qty)

    assert portfolio.assets[ticker].quantity == qty + new_qty


def test_sell_asset_not_on_portfolio():
    portfolio = Portfolio()
    portfolio.sell('ITSA4', 200)

    assert portfolio.assets == {}


def test_sell_more_than_in_portfolio():
    portfolio = Portfolio()
    
    ticker = 'ITSA4'
    qty = 100
    asset = PortfolioAsset(ticker)
    asset.quantity = qty
    portfolio.assets[ticker] = asset

    sell_qty = 200
    portfolio.sell(ticker, sell_qty)

    assert asset.quantity == qty


def test_sell_all():
    portfolio = Portfolio()
    
    ticker = 'ITSA4'
    qty = 100
    asset = PortfolioAsset(ticker)
    asset.quantity = qty
    portfolio.assets[ticker] = asset

    sell_qty = qty
    portfolio.sell(ticker, sell_qty)

    assert asset.quantity == 0
    assert portfolio.assets == {}


def test_sell_partially():
    portfolio = Portfolio()
    
    ticker = 'ITSA4'
    qty = 100
    asset = PortfolioAsset(ticker)
    asset.quantity = qty
    portfolio.assets[ticker] = asset

    sell_qty = 50
    portfolio.sell(ticker, sell_qty)

    assert asset.quantity == qty - sell_qty