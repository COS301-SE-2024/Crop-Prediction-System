import datetime
import requests
from backend.definitions.entry import Entry

class Weather:
    
    def __init__(self):
        self.api_key = 'c0c1ea0d60f1f744ac9ef92c0b4bc7fd'
        self.part = 'hourly,alerts'
        self.unit = 'metric'

    def getWeather(self, lat, lon, field_id) -> Entry:
        url = f'https`://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={self.part}&units={self.unit}&appid={self.api_key}'
        response = requests.get(url)
        data = response.json()
        entries = []
        entry = Entry(
                field_id = field_id,
                date = datetime.fromtimestamp(data['current']['dt']).date(), 
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
            )
        entry = self.get_features(entry)
        entries.append(entry)
        for i in range(7):
            entry = Entry(
                field_id = field_id,
                date = datetime.fromtimestamp(data['current']['dt']).date(), 
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
            )
            entry = self.get_features(entry)
            entries.append(entry)
        return entries
        
    def get_features(self, e : Entry):
        e.gff = min(e.dew_point, e.tempMin),
        e.gdd=max(0, (e.tempMax + e.tempMin) / 2 - self.c.t_base),
        e.hdd=max(0, e.tempean - self.c.t_base),
        e.Tdiurnal=e.temp_max - e.temp_min,
        e.Tmean=(e.temp_max + e.temp_min) / 2,
        e.soil_moisture=(e.pet - e.precipitation) / e.pet,
        e.soil_temperature=(e.temp_max + e.temp_min) / 2
        return e
        


# Make the request
# response = requests.get(url)

# def getWeather(lat, lon) -> Entry:
#     return Entry(
#         id=uuid4(),  # Generate a unique ID for each entry
#         date=datetime.fromtimestamp(weather_data["dt"]).date(),  # Convert timestamp to date
#         cloud_cover=weather_data.get("clouds"),
#         precipitation=weather_data.get("rain", 0),
#         maximum_temperature=weather_data["temp"]["max"],
#         minimum_temperature=weather_data["temp"]["min"],
#         diurnal_temperature_range=weather_data["temp"]["max"] - weather_data["temp"]["min"],
#         mean_temperature=weather_data["temp"]["day"],
#         # Add additional fields if needed
#     )

# import requests

# api_key = 'c0c1ea0d60f1f744ac9ef92c0b4bc7fd'
# lat = '-25.697760'  
# lon = '28.258630'
# part = 'hourly,alerts'
# unit = 'metric'
# url = f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={part}&units={unit}&appid={api_key}'

# # Make the request
# response = requests.get(url)

# # Check if the request was successful
# if response.status_code == 200:
#     data = response.json()
#     tempMin = [data['current']['temp']]  # Temperature for the today and the next 8 days
#     tempMax = [data['current']['temp']]  # Temperature for the today and the next 8 days
#     summary = [data['current']['weather'][0]['description']] # Weather summary for the current day
#     humidity = [data['current']['humidity']] # Weather summary for the current day
#     wind = [data['current']['wind_speed']] # Weather summary for the current day
#     pressure = [data['current']['pressure']] # Weather summary for the current day
#     uvi = [data['current']['uvi']] # Weather summary for the current day
#     if data['current']['pop']:
        
#     pop = [] # Weather summary for the current day
#     rain = []
#     for i in range(8):
#         tempMax.append(data['daily'][i]['temp']['max'])
#         tempMin.append(data['daily'][i]['temp']['min'])
#         summary.append(data['daily'][i]['summary'])
#         humidity.append(data['daily'][i]['humidity'])
#         wind.append(data['daily'][i]['wind_speed'])
#         pressure.append(data['daily'][i]['pressure'])
#         uvi.append(data['daily'][i]['uvi'])
#         pop.append(data['daily'][i]['pop'])
#     daily_weather = [tempMin, tempMax, humidity, wind, pressure, pop, uvi, summary]
#     print(daily_weather)
# else:
#     print('Error:', response.status_code, response.text)
