from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import date

class Response(BaseModel):
    id: Optional[UUID] = None      
    field_id: Optional[int] = None
    date: Optional[date] = None
    summary: Optional[str] = None
    xYield: Optional[float] = None
    health: Optional[float] = None
    sprayability: Optional[float] = None
    tempMax: Optional[float] = None  
    tempMin: Optional[float] = None 
    tempDiurnal: Optional[float] = None
    tempMean: Optional[float] = None
    pressure: Optional[float] = None
    humidity: Optional[float] = None
    dew_point: Optional[float] = None
    wind_speed: Optional[float] = None
    wind_deg: Optional[float] = None
    wind_gust: Optional[float] = None
    clouds: Optional[float] = None
    pop: Optional[float] = None
    rain: Optional[float] = None
    uvi: Optional[float] = None
    gff: Optional[float] = None
    gdd: Optional[float] = None
    hdd: Optional[float] = None
    soil_moisture: Optional[float] = None
    soil_temperature: Optional[float] = None
    pet : Optional[float] = None

# Returns a JSON object with the following structure:
# Option 1:
# {
#     "response" : [
#         {
#             "id": "b3b9c7c3-5b8b-4a5e-9d0e-4f1f3c7c3f4e",
#             "field_id": 0,
#             "date": "2021-08-01",
#             "summary": "This is a summary of the field",
#             "xYield": 0.0,
#             "health": 0.0,
#             "sprayability": 0.0,
#             "tempMax": 0.0,
#             "tempMin": 0.0,
#             "tempDiurnal": 0.0,
#             "tempMean": 0.0,
#             "pressure": 0.0,
#             "humidity": 0.0,
#             "dew_point": 0.0,
#             "wind_speed": 0.0,
#             "wind_deg": 0.0,
#             "wind_gust": 0.0,
#             "clouds": 0.0,
#             "pop": 0.0,
#             "rain": 0.0,
#             "uvi": 0.0,
#             "gff": 0.0,
#             "gdd": 0.0,
#             "hdd": 0.0,
#             "soil_moisture": 0.0,
#             "soil_temperature": 0.0,
#             "pet": 0.0
#         },
#         {
#             "id": "b3b9c7c3-5b8b-4a5e-9d0e-4f1f3c7c3f4e",
#             "field_id": 0,
#             "date": "2021-08-01",
#             "summary": "This is a summary of the field",
#             "xYield": 0.0,
#             "health": 0.0,
#             "sprayability": 0.0,
#             "tempMax": 0.0,
#             "tempMin": 0.0,
#             "tempDiurnal": 0.0,
#             "tempMean": 0.0,
#             "pressure": 0.0,
#             "humidity": 0.0,
#             "dew_point": 0.0,
#             "wind_speed": 0.0,
#             "wind_deg": 0.0,
#             "wind_gust": 0.0,
#             "clouds": 0.0,
#             "pop": 0.0,
#             "rain": 0.0,
#             "uvi": 0.0,
#             "gff": 0.0,
#             "gdd": 0.0,
#             "hdd": 0.0,
#             "soil_moisture": 0.0,
#             "soil_temperature": 0.0,
#             "pet": 0.0
#         }
#     ]
# }

# # Option 2:
# {
#     "id": "b3b9c7c3-5b8b-4a5e-9d0e-4f1f3c7c3f4e",
#     "field_id": 0,
#     "date": [
#         "2021-08-01",
#         "2021-08-01"
#     ],
#     "summary": [
#         "This is a summary of the field",
#         "This is a summary of the field"
#     ],
#     "xYield": [
#         0.0,
#         0.0
#     ],
#     "health": [
#         0.0,
#         0.0
#     ],
#     "sprayability": [
#         0.0,
#         0.0
#     ],
#     "tempMax": [
#         0.0,
#         0.0
#     ],
#     "tempMin": [
#         0.0,
#         0.0
#     ],
#     "tempDiurnal": [
#         0.0,
#         0.0
#     ],
#     "tempMean": [
#         0.0,
#         0.0
#     ],
#     "pressure": [
#         0.0,
#         0.0
#     ],
#     "humidity": [
#         0.0,
#         0.0
#     ],
#     "dew_point": [
#         0.0,
#         0.0
#     ],
#     "wind_speed": [
#         0.0,
#         0.0
#     ],
#     "wind_deg": [
#         0.0,
#         0.0
#     ],
#     "wind_gust": [
#         0.0,
#         0.0
#     ],
#     "clouds": [
#         0.0,
#         0.0
#     ],
#     "pop": [
#         0.0,
#         0.0
#     ],
#     "rain": [
#         0.0,
#         0.0
#     ],
#     "uvi": [
#         0.0,
#         0.0
#     ],
#     "gff": [
#         0.0,
#         0.0
#     ],
#     "gdd": [
#         0.0,
#         0.0
#     ],
#     "hdd": [
#         0.0,
#         0.0
#     ],
#     "soil_moisture": [
#         0.0,
#         0.0
#     ],
#     "soil_temperature": [
#         0.0,
#         0.0
#     ],
#     "pet": [
#         0.0,
#         0.0
#     ]
# }
