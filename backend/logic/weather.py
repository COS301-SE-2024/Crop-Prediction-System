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
            entry = self.featureEngineering(entry)
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
    def featureEngineering(self, e : Entry):
        tempmean = e.tempMean
        humidity = e.humidity

        soil_moisture, soil_temperature = self.sm.predict(tempmean, humidity)

        e.soil_temperature = soil_temperature[0]
        e.soil_moisture = soil_moisture[0]

        # Convert to float8
        e.soil_temperature = math.ceil(e.soil_temperature * 100) / 100
        e.soil_moisture = math.ceil(e.soil_moisture * 100) / 100

        e.sprayability = Weather.calculate_sprayability(e)

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
                        'pred_sprayability': entry.sprayability
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
                    'pred_sprayability': entry.sprayability
                }, returning='representation'
                ).eq('field_id', entry.field_id).eq('date', dt.datetime.fromtimestamp(entry.timestamp).strftime('%Y-%m-%d')).execute()
        return

    @staticmethod
    def update_allFeatures():
        entries = Weather.__sbClient.table('data').select('*').execute()
        for entry in entries.data:
            # updating entry x of n
            print("Updating entry " + str(entries.data.index(entry) + 1) + " of " + str(len(entries.data)), flush=True)
            e = Entry(
                field_id = entry['field_id'] if 'field_id' in entry else None,
                timestamp = datetime.datetime.strptime(entry['date'], '%Y-%m-%d').timestamp(),
                summary = entry['summary'],
                tempMax = entry['tempmax'],
                tempMin = entry['tempmin'],
                tempDiurnal = entry['tempdiurnal'],
                tempMean = entry['tempmean'],
                pressure = entry['pressure'],
                humidity = entry['humidity'],
                dew_point = entry['dew_point'],
                clouds = entry['clouds'],
                rain = entry['rain'],
                uvi = entry['uvi'],
                soil_moisture = entry['soil_moisture'],
                soil_temperature = entry['soil_temperature'],
                sprayability = entry['pred_sprayability']
            )
            e = Weather().featureEngineering(e)
            if e.field_id is None:
                response = Weather.__sbClient.table('data').update({
                    'soil_moisture': e.soil_moisture,
                    'soil_temperature': e.soil_temperature,
                    'pred_sprayability': e.sprayability
                }).eq('date', dt.datetime.fromtimestamp(e.timestamp).strftime('%Y-%m-%d')).execute()
            else:
                response = Weather.__sbClient.table('data').update({
                    'soil_moisture': e.soil_moisture,
                    'soil_temperature': e.soil_temperature,
                    'pred_sprayability': e.sprayability
                }).eq('field_id', e.field_id).eq('date', dt.datetime.fromtimestamp(e.timestamp).strftime('%Y-%m-%d')).execute()
        return
    
# if __name__ == '__main__':
#     w = Weather()
#     w.update_allFeatures()
#     print('Updated all features', flush=True)