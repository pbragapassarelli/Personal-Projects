import pytest

from app import get_price_for_ticker
from app import PortfolioAsset, Portfolio
from app import MESSAGE_NOT_ON_PORTFOLIO, MESSAGE_TRYING_TO_SELL_MORE_THAN_AVAILABLE


# def test_get_price_for_ticker():
#     answer = get_price_for_ticker('ITSA4')

#     assert type(answer) == float


def test_buy_asset_for_first_time():
    portfolio = Portfolio()
    ticker = 'ITSA4'
    qty = 100
    price = 12

    portfolio.buy(ticker, qty, price)

    assert portfolio._get_asset_by_ticker(ticker).quantity == qty
    assert portfolio._get_asset_by_ticker(ticker).amount_invested == qty * price
    assert portfolio._get_asset_by_ticker(ticker).average_price == price


def test_buy_existing_asset():
    portfolio = Portfolio()
    
    ticker = 'ITSA4'
    qty = 100
    price = 13
    asset = PortfolioAsset(ticker, quantity=qty, amount_invested=qty*price)
    portfolio.assets.append(asset)
    
    new_qty = 200
    new_price = 11
    portfolio.buy(ticker, new_qty, new_price)

    assert portfolio._get_asset_by_ticker(ticker).quantity == qty + new_qty
    assert portfolio._get_asset_by_ticker(ticker).amount_invested == (qty*price) + (new_qty*new_price)
    assert portfolio._get_asset_by_ticker(ticker).average_price == ((qty*price) + (new_qty*new_price)) / (qty+new_qty)


def test_sell_asset_not_on_portfolio():
    portfolio = Portfolio()

    with pytest.raises(Exception) as excinfo:
        portfolio.sell('ITSA4', 200, 12)

    assert str(excinfo.value) == MESSAGE_NOT_ON_PORTFOLIO


def test_sell_more_than_in_portfolio():
    portfolio = Portfolio()
    
    ticker = 'ITSA4'
    qty = 100
    amount = 1200
    asset = PortfolioAsset(ticker, quantity=qty, amount_invested=amount)
    portfolio.assets.append(asset)

    sell_qty = 200
    with pytest.raises(Exception) as excinfo:
        portfolio.sell(ticker, sell_qty, 12)

    assert str(excinfo.value) == MESSAGE_TRYING_TO_SELL_MORE_THAN_AVAILABLE


def test_sell_all():
    portfolio = Portfolio()
    
    ticker = 'ITSA4'
    qty = 100
    amount = 1200
    asset = PortfolioAsset(ticker, quantity=qty, amount_invested=amount)
    portfolio.assets.append(asset)

    sell_qty = qty
    price = 13
    portfolio.sell(ticker, sell_qty, price)

    assert asset.quantity == 0
    assert asset.amount_invested == 0
    assert asset.average_price == amount / qty
    assert portfolio.assets == []


def test_sell_partially():
    portfolio = Portfolio()
    
    ticker = 'ITSA4'
    buy_qty = 100
    buy_price = 12
    asset = PortfolioAsset(ticker, quantity=buy_qty, amount_invested=buy_qty*buy_price)
    portfolio.assets.append(asset)

    sell_qty = 50
    sell_price = 13
    portfolio.sell(ticker, sell_qty, sell_price)

    assert asset.quantity == buy_qty - sell_qty
    assert asset.amount_invested == buy_qty*buy_price - sell_qty*buy_price
    assert asset.average_price == buy_price