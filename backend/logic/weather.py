import datetime
import math
import requests
from definitions.entry import Entry
from definitions.crop import Crop

class Weather:
    def __init__(self):
        self.api_key = 'c0c1ea0d60f1f744ac9ef92c0b4bc7fd'
        self.part = 'hourly,alerts'
        self.unit = 'metric'

    def getWeather(self, lat, lon, field_id, c : Crop) -> Entry:
        url = f'https`://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={self.part}&units={self.unit}&appid={self.api_key}'
        response = requests.get(url)
        data = response.json()
        entries = []
        entry = Entry(
                field_id = field_id,
                date = datetime.datetime.fromtimestamp(data['current']['dt']).date(), 
                summary = data['current']['weather'][0]['description'], 
                pressure = data['current']['pressure'],
                humidity = data['current']['humidity'],
                wind_speed = data['current']['wind_speed'],
                wind_deg = data['current']['wind_deg'],
                wind_gust = data['current']['wind_gust'],
                clouds = data['current']['clouds'],
                pop = data['current']['pop'],
                rain = data['current']['rain'] or 0,
                uvi = data['current']['uvi'],
                dew_point = data['current']['dew_point'],
            )
        entry = self.get_features(entry, c)
        entries.append(entry)
        for i in range(7):
            entry = Entry(
                field_id = field_id,
                date = datetime.datetime.fromtimestamp(data['current']['dt']).date(), 
                summary = data['daily'][i]['summary'],
                tempMax = data['daily'][i]['temp']['max'],
                tempMin = data['daily'][i]['temp']['min'],
                pressure = data['daily'][i]['pressure'],
                humidity = data['daily'][i]['humidity'],
                wind_speed = data['daily'][i]['wind_speed'],
                wind_deg = data['daily'][i]['wind_deg'],
                wind_gust = data['daily'][i]['wind_gust'],
                clouds = data['daily'][i]['clouds'],
                pop = data['daily'][i]['pop'],
                rain = data['daily'][i]['rain'] or 0,
                uvi = data['daily'][i]['uvi'],
                dew_point = data['daily'][i]['dew_point'],
            )
            entry = self.get_features(entry)
            entries.append(entry)
        return entries
        
    def get_features(self, e : Entry, c : Crop):
        e.gff = min(e.dew_point, e.tempMin),
        e.gdd = max(0, (e.tempMax + e.tempMin) / 2 - c.t_base),
        e.hdd = max(0, e.tempMean - c.t_base),
        e.tempDiurnal = e.tempMax - e.tempMin,
        e.tempMean = (e.tempMax + e.tempMin) / 2,
        es = 0.6108 * math.exp(17.27 * e.tempMean/ (e.tempMean + 237.3))
        ea = 0.6108 * math.exp(17.27 * e.dew_point/ (e.dew_point + 237.3))
        delta = 4098 * es / (e.tempMean + 237.3) ** 2
        gamma = (0.655 * 0.001 * 101.5) / 2.45
        Rn = 0.0864 * e.uvi 
        u2 = 7.92 / 3.6
        e.pet = (0.408 * delta * (Rn - 0) + gamma * (900 / e.tempMean + 273) * u2 * (es - ea)) / (delta + gamma * (1 + 0.34 * u2))
        e.soil_moisture = (e.pet - e.rain) / e.pet if e.pet != 0 else None,
        e.soil_temperature = (e.tempMax + e.tempMin) / 2
        return e