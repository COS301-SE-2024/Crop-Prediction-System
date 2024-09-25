# market API
from dotenv import load_dotenv
import os
import requests
import json

def market(function : str):
    load_dotenv()

    api_key = os.environ.get('ALPHA_VANTAGE_API_KEY')

    # get forex rates
    url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=USD&to_currency=ZAR&apikey={api_key}"

    exchange_rate = requests.get(url)

    exchange_rate = exchange_rate.json()

    exchange_rate = exchange_rate['Realtime Currency Exchange Rate']['5. Exchange Rate']
    
    # make a request to the market API
    url = f"https://www.alphavantage.co/query?function={function}&interval=monthly&apikey={api_key}"

    response = requests.get(url)

    response = response.json()

    response['data'] = [x for x in response['data'] if x['value'] != '.']

    # Convert this to ZAR
    for i in range(len(response['data'])):
        response['data'][i]['value'] = float(response['data'][i]['value']) * float(exchange_rate)

    # Round to 2 decimal places
    for i in range(len(response['data'])):
        response['data'][i]['value'] = round(response['data'][i]['value'], 2)

    # Change unit to ZAR
    response['unit'] = "ZAR per metric ton"
    
    return response