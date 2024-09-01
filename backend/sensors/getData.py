import requests
import json
import pandas as pd
import os
from dotenv import load_dotenv

# graphql documentation
# https://graphql.org/learn/queries/

# information hub graphql playground
# https://api.informationhub.io/graphql

sensors = "'2CF7F12025200009', '2CF7F1202520006A', '2CF7F1202520010D', '2CF7F120252000E7'"

def getNewSensorData(sensorID: str, number_of_rows: int = 1):
    load_dotenv()
    url = os.environ.get("SENSOR_API_URL")
    apiKey = os.environ.get("SENSOR_API_KEY")

    query = """query QueryTable($request: QueryTableRequest!) {
      queryTable(request: $request) {
        rows {
          columns {
            key
            value
          }
        }
      }
    }"""
    
    request = {
        "request": {
            "select": [{"column": "id"}, {"column": "device_eui"}, {"column": "soil_temperature"}, {"column": "soil_moisture"}, {"column": "temperature"}, {"column": "relative_humidity"}, {"column": "light"}, {"column": "co2"}, {"column": "battery"}, {"column": "received_at"}],
            "from": "clid3g4xn000hs601tz9hr3rw.\"sensecap_data_dump\"",
            "where": {
                "args": [
                    "device_eui",
                    sensorID
                ],
                "operation": "IN"},
            "order": [
                {"column": "received_at", "ascending": False}
            ],
            "limit": number_of_rows
        }
    }
    headers = {"Authorization": "Bearer " + apiKey}
    r = requests.post(url, headers=headers, json={'query': query, 'variables': request})

    return r.json()

if __name__ == "__main__":
    print("Getting data")
    sensor = "'2CF7F12025200009'"
    data = getNewSensorData(sensor)
    print(data)