import requests
import json
import pandas as pd

# graphql documentation
# https://graphql.org/learn/queries/

# information hub graphql playground
# https://api.informationhub.io/graphql

apiKey = process.env.SENSOR_API_KEY

sensors = "'2CF7F12025200009', '2CF7F1202520006A', '2CF7F1202520010D', '2CF7F120252000E7'"

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

# to get the latest data from the sensors use "order": [{"column": "received_at", "ascending": False}], limit sets the number of rows to return
request = {
    "request": {
        "select": [{"column": "id"}, {"column": "device_eui"}, {"column": "soil_temperature"}, {"column": "soil_moisture"}, {"column": "temperature"}, {"column": "relative_humidity"}, {"column": "light"}, {"column": "co2"}, {"column": "battery"}, {"column": "received_at"}],
        "from": "clid3g4xn000hs601tz9hr3rw.\"sensecap_data_dump\"",
        "where": {
            "args": [
                "device_eui",
                "'2CF7F12025200009'"
            ],
            "operation": "IN"},
        "order": [
            {"column": "received_at", "ascending": False}
        ],
        "limit": 1
    }
}

headers = {"Authorization": "Bearer " + apiKey}

url = process.env.SENSOR_API_URL

r = requests.post(url, headers=headers, json={'query': query, 'variables': request})

print(r)

with open(f"dump.json", "w") as f:
    json.dump(r.json(), f, indent=4)

print(r.json())