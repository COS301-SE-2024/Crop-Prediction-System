# market API
from dotenv import load_dotenv
import os
import requests

def market(function : str):
    load_dotenv()

    api_key = os.environ.get('ALPHA_VANTAGE_API_KEY')
    
    # make a request to the market API
    url = f"https://www.alphavantage.co/query?function={function}&interval=monthly&apikey={api_key}"

    response = requests.get(url)

    response = response.json()

    return response