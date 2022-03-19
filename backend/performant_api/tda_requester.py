
from .secrets import tda_clientid
import requests

api_url = "https://api.tdameritrade.com/v1/marketdata/"


def price_history(ticker = "TSLA", start_date = "1639902207000"):
    # The start date is rounded to the next day.
    query={
        'apikey': tda_clientid,
        'periodType' : 'month',
        'frequencyType' : 'daily',
        'startDate' : start_date,
    }
    
    req_string = f'{api_url}{ticker}/pricehistory'
    response = requests.get(req_string, params=query)

    # req_string = f'{api_url}{ticker}/pricehistory?apikey={tda_clientid}&periodType=month&frequencyType=daily&startDate={start_date}'
    # response = requests.get(req_string)


    # print(req_string)
    return response.json()['candles']