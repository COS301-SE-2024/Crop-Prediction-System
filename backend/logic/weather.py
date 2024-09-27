import datetime as dt
import math
import requests
from backend.definitions.entry import Entry
from backend.definitions.crop import Crop
from backend.database import supabaseInstance
from backend.logic.gemini import Gemini
from backend.sensor.SensorModel import SensorModel
from dotenv import load_dotenv
import os
import datetime
from math import log

class Weather:
    __sbClient = supabaseInstance.supabaseInstance().get_client()
    __gemini = Gemini()
    def __init__(self):
        load_dotenv()
        self.api_key = os.environ.get('OPENWEATHER_API_KEY')
        self.part = 'hourly,alerts'
        self.unit = 'metric'
        self.sm = SensorModel()

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
                tempDiurnal = data['daily'][i]['temp']['max'] - data['daily'][i]['temp']['min'] if 'temp' in data['daily'][i] else 0,
                tempMean = (data['daily'][i]['temp']['max'] + data['daily'][i]['temp']['min']) / 2 if 'temp' in data['daily'][i] else 0,
                pressure = data['daily'][i]['pressure'] if 'pressure' in data['daily'][i] else 0,
                humidity = data['daily'][i]['humidity'] if 'humidity' in data['daily'][i] else 0,
                clouds = data['daily'][i]['clouds'] if 'clouds' in data['daily'][i] else 0,
                rain = data['daily'][i]['rain'] if 'rain' in data['daily'][i] else 0,
                uvi = data['daily'][i]['uvi'] if 'uvi' in data['daily'][i] else 0,
                dew_point = data['daily'][i]['dew_point'] if 'dew_point' in data['daily'][i] else 0,
            )
            # print(entry, flush=True)
            entry = self.featureEngineering(entry, c)
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
            response = Weather.__sbClient.table('data').update({
                'summary': message,
            }).eq('field_id', field_id).eq('date', dt.datetime.now().strftime('%Y-%m-%d')).execute()
        except Exception as e:
            return {
                'error': e
            }

        return response.data
    
    # Feature Engineering
    def featureEngineering(self, e : Entry, c : Crop) -> Entry:
        tempmean = e.tempMean
        humidity = e.humidity

        soil_moisture, soil_temperature = self.sm.predict(tempmean, humidity)

        e.soil_temperature = soil_temperature[0]
        e.soil_moisture = soil_moisture[0]

        # Convert to float8
        e.soil_temperature = math.ceil(e.soil_temperature * 100) / 100
        e.soil_moisture = math.ceil(e.soil_moisture * 100) / 100

        e.sprayability = Weather.calculate_sprayability(e)

        e.health = Weather.calculateHealth(e.tempMin, e.tempMax, c.name)

        return e
    
    @staticmethod
    def calculate_sprayability(entry: Entry) -> float:
        humidity_factor = entry.humidity / 100.0 if entry.humidity else 0.5
        temperature_factor = min(max((entry.tempMean - 10) / 20.0, 0.0), 1.0) if entry.tempMean else 0.5
        soil_moisture_factor = min(entry.soil_moisture / 100.0, 1.0) if entry.soil_moisture else 0.5
        
        sprayability = (
            0.25 * humidity_factor +
            0.4 * temperature_factor +
            0.05 * soil_moisture_factor
        )

        # Convert to avalue between 0 and 1
        sprayability = 1 / (1 + math.exp(-sprayability)) * 100
        
        return round(sprayability, 2)
    
    # Uploads array of Entry objects to the database
    @staticmethod
    def upload(entries):
        for entry in entries:
            entry_date = dt.datetime.fromtimestamp(entry.timestamp).date()
            future_date = (dt.datetime.now() + dt.timedelta(days=6)).date()

            if (entry_date <= future_date):
                try:
                    response = Weather.__sbClient.table('data').insert({
                        'field_id': str(entry.field_id),
                        'date': dt.datetime.fromtimestamp(entry.timestamp).strftime('%Y-%m-%d'),
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
                        'uvi': entry.uvi,
                        'soil_moisture': entry.soil_moisture,
                        'soil_temperature': entry.soil_temperature,
                        'pred_sprayability': entry.sprayability,
                        'pred_health': entry.health
                    }, returning='representation'
                    ).execute()
                except Exception as e:
                    pass
            else:
                response = Weather.__sbClient.table('data').update({
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
                    'uvi': entry.uvi,
                    'soil_moisture': entry.soil_moisture,
                    'soil_temperature': entry.soil_temperature,
                    'pred_sprayability': entry.sprayability,
                    'pred_health': entry.health
                }, returning='representation'
                ).eq('field_id', entry.field_id).eq('date', dt.datetime.fromtimestamp(entry.timestamp).strftime('%Y-%m-%d')).execute()
        return

    @staticmethod
    def update_allFeatures():
        entries = Weather.__sbClient.table('data').select('*').execute()
        field_ids = []

        # Get all unique field_ids
        for entry in entries.data:
            if entry['field_id'] not in field_ids and entry['field_id'] is not None:
                field_ids.append(entry['field_id'])
            if entry['field_id'] is None:
                entries.data.remove(entry)

        crops_by_field = {}
        for field_id in field_ids:
            response = Weather.__sbClient.table('field_info').select('crop_type').eq('id', field_id).execute()
            crops_by_field[field_id] = response.data[0]['crop_type']

        print(crops_by_field, flush=True)
            

        for entry in entries.data:
            if entry['field_id'] is not None:
                print(entry, flush=True)
                response = Weather.__sbClient.table('data').update({
                    'pred_health': Weather.calculateHealth(entry['tempmin'], entry['tempmax'], crops_by_field[entry['field_id']])
                }).eq('field_id', entry['field_id']).eq('date', entry['date']).execute()
        return
    
    @staticmethod
    def calculateHealth(min, max, crop):
        response = Weather.__sbClient.table('crop_info').select("optimal_temp_max, optimal_temp_min").eq('name', crop).execute()

        crop_info = response.data[0]['optimal_temp_min'], response.data[0]['optimal_temp_max']

        # Calculate health as a percentage
        health = ((max + min) / 2) - crop_info[0]

        health = health / (crop_info[1] - crop_info[0])

        if health > 1 or health < 0:
            health = 1 / (1 + math.exp(-health))

        return health

# if __name__ == '__main__':
#     w = Weather()
#     w.calculateHealth(27, 10, "maize")
#     w.update_allFeatures()
    # print('Updated all features', flush=True)