import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv('API_KEY')
MAX_REQUESTS_PER_MINUTE = 5

def get_price_for_ticker(ticker, key=API_KEY):

    import requests

    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}.SA&apikey={key}'
    data = requests.get(url).json()

    price = float(data['Global Quote']['05. price'])

    return price