import requests
import json
import pandas as pd

# graphql documentation
# https://graphql.org/learn/queries/

# information hub graphql playground
# https://api.informationhub.io/graphql

apiKey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoidVVtSHQwczFQRFhRUXJVUm5YbGx0MEVkUGF2MiIsImFwaV9rZXlfaWQiOiJjbHhjMTJkYnQwMDAwMDFzNmM0MTNndzhnIiwiaWF0IjoxNzE4MjA4NjQ3LCJhdWQiOiJpbmZvcm1hdGlvbi1odWItaW8iLCJpc3MiOiJodHRwczovL2FwcC5pbmZvcm1hdGlvbmh1Yi5pbyJ9.FhaFG_jh_L96Lw8QDn9KQPQuVHfEdhuFJaCKrgu_WEQ"

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

request = {
    "request": {
        "select": [{"column": "id"}, {"column": "device_eui"}, {"column": "soil_temperature"}, {"column": "soil_moisture"}, {"column": "temperature"}, {"column": "relative_humidity"}, {"column": "light"}, {"column": "co2"}, {"column": "battery"}, {"column": "received_at"}],
        "from": "clid3g4xn000hs601tz9hr3rw.\"sensecap_data_dump\"",
        "where": {
            "args": [
                "device_eui",
                "'2CF7F12025200135', '2CF7F12025200155', '2CF7F1202520013F'"
            ],
            "operation": "IN"},
        # "limit": 10
    }
}

headers = {"Authorization": "Bearer " + apiKey}

url = 'https://api.informationhub.io/graphql/'
r = requests.post(url, headers=headers, json={'query': query, 'variables': request})

print(r)

with open(f"dump.json", "w") as f:
    json.dump(r.json(), f, indent=4)

print(r.json())
