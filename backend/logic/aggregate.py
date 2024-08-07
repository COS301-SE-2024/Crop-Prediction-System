# This function aggregates data from daily to staged

from definitions.entry import Entry
from definitions.crop import Crop
from definitions.data import Data
from database import supabaseInstance
import datetime
from typing import List

class Aggregate:
    __sbClient = supabaseInstance.supabaseInstance().get_client()

    def __init__(self):
        pass

    @staticmethod
    def aggregate(entries: List[Entry], stage: str, field_id: str):
        print("Aggregating data for stage:", stage, flush=True)
        print("Field ID:", field_id, flush=True)

        if not entries:
            print("No entries to aggregate.", flush=True)
            return None
        
        # Initialize accumulators
        count = len(entries)
        sum_values = {
            'pet': 0,
            'cloud_cover': 0,
            'maximum_temperature': 0,
            'minimum_temperature': 0,
            'vapour_pressure': 0,
            'diurnal_temperature_range': 0,
            'mean_temperature': 0,
            'precipitation': 0,
            'rain_days': 0,
            'ground_frost_frequency': 0,
            'gdd': 0,
            'hdd': 0,
            'cumulative_precipitation': 0,
            'soil_moisture_index': 0,
            'soil_temperature_index': 0,
            'uv_index': 0
        }

        for entry in entries:
            sum_values['pet'] += entry.pet
            sum_values['cloud_cover'] += entry.clouds
            sum_values['maximum_temperature'] += entry.tempMax
            sum_values['minimum_temperature'] += entry.tempMin
            sum_values['vapour_pressure'] += entry.dew_point
            sum_values['diurnal_temperature_range'] += entry.tempDiurnal
            sum_values['mean_temperature'] += entry.tempMean
            sum_values['precipitation'] += entry.rain
            sum_values['rain_days'] += entry.pop
            sum_values['ground_frost_frequency'] += entry.gff
            sum_values['gdd'] += entry.gdd
            sum_values['hdd'] += entry.hdd
            sum_values['cumulative_precipitation'] += entry.rain
            sum_values['soil_moisture_index'] += entry.soil_moisture
            sum_values['soil_temperature_index'] += entry.soil_temperature
            sum_values['uv_index'] += entry.uvi

        # Calculate averages
        d = Data(
            year=datetime.datetime.fromtimestamp(entries[0].timestamp).year,
            stage=stage,
            pet=sum_values['pet'] / count,
            cloud_cover=sum_values['cloud_cover'] / count,
            maximum_temperature=sum_values['maximum_temperature'] / count,
            minimum_temperature=sum_values['minimum_temperature'] / count,
            vapour_pressure=sum_values['vapour_pressure'] / count,
            diurnal_temperature_range=sum_values['diurnal_temperature_range'] / count,
            mean_temperature=sum_values['mean_temperature'] / count,
            precipitation=sum_values['precipitation'] / count,
            rain_days=sum_values['rain_days'],
            ground_frost_frequency=sum_values['ground_frost_frequency'] / count,
            gdd=sum_values['gdd'] / count,
            hdd=sum_values['hdd'] / count,
            cumulative_precipitation=sum_values['cumulative_precipitation'] / count,
            soil_moisture_index=sum_values['soil_moisture_index'] / count,
            soil_temperature_index=sum_values['soil_temperature_index'] / count,
            uv_index=sum_values['uv_index'] / count
        )
        
        # Upload aggregated data
        Aggregate.upload(d, field_id)
        print("Aggregation completed.", flush=True)
        return d
    
    @staticmethod
    def upload(d : Data, field_id):
        try:
            response = Aggregate.__sbClient.table('model_data').upsert({
                'field_id': field_id,
                'year': d.year,
                'stage': d.stage,
                'pet': d.pet,
                'cloud_cover': d.cloud_cover,
                'maximum_temperature': d.maximum_temperature,
                'minimum_temperature': d.minimum_temperature,
                'vapour_pressure': d.vapour_pressure,
                'diurnal_temperature_range': d.diurnal_temperature_range,
                'mean_temperature': d.mean_temperature,
                'precipitation': d.precipitation,
                'rain_days': d.rain_days,
                'ground_frost_frequency': d.ground_frost_frequency,
                'gdd': d.gdd,
                'hdd': d.hdd,
                'cumulative_precipitation': d.cumulative_precipitation,
                'soil_moisture_index': d.soil_moisture_index,
                'soil_temperature_index': d.soil_temperature_index,
                'uv_index': d.uv_index
            }).execute()
            print(response, flush=True)
        except Exception as e:
            print(e, flush=True)
        return

    @staticmethod
    def countRainDays(arr, val):
        count = 0
        for i in arr:
            if i > val:
                count += 1
        return count

    @staticmethod
    def countGFF(arr1, arr2):
        count = 0
        for i in range(len(arr1)):
            if arr1[i] < 0 or arr2[i] < 0:
                count += 1
        return count