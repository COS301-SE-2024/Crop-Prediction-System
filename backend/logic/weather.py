import datetime
import math
import requests
from backend.definitions.entry import Entry
from backend.definitions.crop import Crop
from backend.database import supabaseInstance
from backend.logic.gemini import Gemini
from dotenv import load_dotenv
import os

class Weather:
    __sbClient = supabaseInstance.supabaseInstance().get_client()
    __gemini = Gemini()
    def __init__(self):
        load_dotenv()
        self.api_key = os.environ.get('OPENWEATHER_API_KEY')
        self.part = 'hourly,alerts'
        self.unit = 'metric'

    def getWeather(self, lat, lon, field_id, c : Crop) -> Entry:
        url = f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={self.part}&units={self.unit}&appid={self.api_key}'
        response = requests.get(url)
        data = response.json()

        entries = []
        for i in range(7):
            entry = Entry(
                field_id = field_id,
                timestamp = data['daily'][i]['dt'], 
                summary = data['daily'][i]['summary'],
                tempMax = data['daily'][i]['temp']['max'] if 'temp' in data['daily'][i] else 0,
                tempMin = data['daily'][i]['temp']['min'] if 'temp' in data['daily'][i] else 0,
                pressure = data['daily'][i]['pressure'] if 'pressure' in data['daily'][i] else 0,
                humidity = data['daily'][i]['humidity'] if 'humidity' in data['daily'][i] else 0,
                wind_speed = data['daily'][i]['wind_speed'] if 'wind_speed' in data['daily'][i] else 0,
                wind_deg = data['daily'][i]['wind_deg'] if 'wind_deg' in data['daily'][i] else 0,
                wind_gust = data['daily'][i]['wind_gust'] if 'wind_gust' in data['daily'][i] else 0,
                clouds = data['daily'][i]['clouds'] if 'clouds' in data['daily'][i] else 0,
                pop = data['daily'][i]['pop'] if 'pop' in data['daily'][i] else 0,
                rain = data['daily'][i]['rain'] if 'rain' in data['daily'][i] else 0,
                uvi = data['daily'][i]['uvi'] if 'uvi' in data['daily'][i] else 0,
                dew_point = data['daily'][i]['dew_point'] if 'dew_point' in data['daily'][i] else 0,
            )
            # print(entry, flush=True)
            entry = Weather.get_features(entry, c)
            entries.append(entry)
        Weather.upload(entries)
        return entries
    
    # Gemini Summary
    def getSummary(self, lat, lon, field_id):
        summary_url = f'https://api.openweathermap.org/data/3.0/onecall/overview?lat={lat}&lon={lon}&exclude={self.part}&units={self.unit}&appid={self.api_key}'
        summary_response = requests.get(summary_url)
        summary_data = summary_response.json()

        message = self.__gemini.send_message(summary_data['weather_overview'])

        try:
            response = Weather.__sbClient.table('data').upsert({
                'field_id': str(field_id),
                'date': datetime.datetime.now().strftime('%Y-%m-%d'),
                'summary': message,
            }).execute()
        except Exception as e:
            return {
                'error': e
            }

        return response.data
    
    # Uploads array of Entry objects to the database
    @staticmethod
    def upload(entries):
        for entry in entries:
            # Let it upload to data as well
            response = Weather.__sbClient.table('data').upsert({
                'field_id': str(entry.field_id),
                'date': datetime.datetime.fromtimestamp(entry.timestamp).strftime('%Y-%m-%d'),
                'summary': entry.summary,
                'tempmax': entry.tempMax,
                'tempmin': entry.tempMin,
                'humidity': entry.humidity,
                'tempdiurnal': entry.tempDiurnal,
                'pressure': entry.pressure,
                'tempmean': entry.tempMean,
                'dew_point': entry.dew_point,
                'clouds': entry.clouds,
                'rain': entry.rain,
                'uvi': entry.uvi
            }, returning='representation'
            ).execute()
        return
