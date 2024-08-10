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

        # print(summary_data['weather_overview'], flush=True)

        message = self.__gemini.send_message(summary_data['weather_overview'])

        try:
            response = Weather.__sbClient.table('field_data').upsert({
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
            response = Weather.__sbClient.table('field_data').upsert({
                'field_id': str(entry.field_id),
                'date': datetime.datetime.fromtimestamp(entry.timestamp).strftime('%Y-%m-%d'),
                'summary': entry.summary,
                'health': Weather.calculate_health(entry),
                'sprayability': Weather.calculate_sprayability(entry),
                'tempmax': entry.tempMax,
                'tempmin': entry.tempMin,
                'humidity': entry.humidity,
                'tempdiurnal': entry.tempDiurnal,
                'pressure': entry.pressure,
                'tempmean': entry.tempMean,
                'soil_moisture': entry.soil_moisture,
                'dew_point': entry.dew_point,
                'wind_speed': entry.wind_speed,
                'wind_deg': entry.wind_deg,
                'wind_gust': entry.wind_gust,
                'clouds': entry.clouds,
                'pop': entry.pop,
                'rain': entry.rain,
                'uvi': entry.uvi,
                'gff': entry.gff,
                'gdd': entry.gdd,
                'hdd': entry.hdd,
                'soil_temperature': entry.soil_temperature,
                'pet': entry.pet
            }, returning='representation'
            ).execute()
        return
        
    @staticmethod
    def get_features(e : Entry, c : Crop):
        # print(c.t_base, flush=True)
        e.tempMean = (e.tempMax + e.tempMin) / 2
        e.gdd = max(0, e.tempMean - c.t_base)
        e.hdd = max(0, c.t_base - e.tempMin)
        e.gff = 1 if e.tempMin < 0 else 0
        e.tempDiurnal = e.tempMax - e.tempMin
        es = 0.6108 * math.exp(17.27 * e.tempMean / (e.tempMean + 237.3))
        ea = 0.6108 * math.exp(17.27 * e.dew_point / (e.dew_point + 237.3))
        delta = 4098 * es / (e.tempMean + 237.3) ** 2
        gamma = (0.655 * 0.001 * 101.5) / 2.45
        Rn = 0.0864 * e.uvi
        u2 = 7.92 / 3.6
        
        ep = (0.408 * delta * (Rn - 0) + gamma * (900 / e.tempMean + 273) * u2 * (es - ea)) / (delta + gamma * (1 + 0.34 * u2))

        max_pet = 220
        e.pet = min(ep / max_pet, 1)  # Scale PET to a max of 1

        humidity_effect = 1 + (e.humidity / 100) * 0.05
        wind_effect = 1 - (e.wind_speed / 100) * 0.05
        temp_effect = 1 + (e.tempMean - c.t_base) * 0.05

        if e.pet > 0:
            adjusted_pet = e.pet * wind_effect * temp_effect
            e.soil_moisture = (e.rain - adjusted_pet + humidity_effect) / max(1, adjusted_pet)
        else:
            e.soil_moisture = 1
        e.soil_moisture = math.sqrt(e.soil_moisture * e.soil_moisture)

        damping_factor = 0.2  # Assume a constant or vary based on soil moisture
        e.soil_temperature = e.tempMean + e.tempDiurnal * damping_factor

        return e
    
    @staticmethod
    def calculate_sprayability(e: Entry) -> float:
        # Extract variables from the data
        humidity = e.humidity
        wind_speed = e.wind_speed
        temp_mean = e.tempMean
        dew_point = e.dew_point
        
        # Define normalization functions
        def normalize_humidity(humidity):
            return 1 - humidity / 100
        
        def normalize_wind_speed(wind_speed):
            return max(0, 1 - wind_speed / 10)  # Assuming wind speed > 10 is not typical

        def normalize_temperature(temp_mean):
            min_temp = 10
            max_temp = 25
            return max(0, min(1, (temp_mean - min_temp) / (max_temp - min_temp)))
        
        def normalize_dew_point(dew_point):
            # Adjust based on expected dew point range
            return max(0, 1 - (dew_point + 10) / 10)
        
        # Calculate normalized indices
        humidity_index = normalize_humidity(humidity)
        wind_speed_index = normalize_wind_speed(wind_speed)
        temperature_index = normalize_temperature(temp_mean)
        dew_point_index = normalize_dew_point(dew_point)
        
        # Define weights
        w1 = 0.25
        w2 = 0.25
        w3 = 0.25
        w4 = 0.25
        
        # Calculate sprayability score
        sprayability = (w1 * humidity_index +
                        w2 * wind_speed_index +
                        w3 * temperature_index +
                        w4 * dew_point_index) * 100
        
        return sprayability
    
    @staticmethod
    def calculate_health(entry: Entry) -> float:
        health = (0.25 * entry.tempMean + 0.25 * entry.humidity + 0.25 * entry.wind_speed + 0.25 * entry.soil_moisture + 0.25 * entry.uvi + 0.25 * entry.rain + 0.25 * entry.clouds + 0.25 * entry.pressure + 0.25 * entry.dew_point + 0.25 * entry.gdd + 0.25 * entry.hdd + 0.25 * entry.gff + 0.25 * entry.pet) / 300.0 * 100.0

        return round(health, 2)
