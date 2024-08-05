# This function aggregates data from daily to staged

from definitions.entry import Entry
from definitions.crop import Crop
from definitions.data import Data

# e as array of entries, c as crop, stage as string, returns Data object
def aggregate(e, c, stage):
    d = Data(
        year = e.year,
        stage = stage,
        pet = sum(e.pet) / len(e.pet),
        cloud_cover = sum(e.cloud_cover) / len(e.cloud_cover),
        maximum_temperature = sum(e.maximum_temperature) / len(e.maximum_temperature),
        minimum_temperature = sum(e.minimum_temperature) / len(e.minimum_temperature),
        vapour_pressure = sum(e.vapour_pressure) / len(e.vapour_pressure),
        diurnal_temperature_range = sum(e.diurnal_temperature_range) / len(e.diurnal_temperature_range),
        mean_temperature = sum(e.mean_temperature) / len(e.mean_temperature),
        precipitation = sum(e.precipitation) / len(e.precipitation),
        rain_days = countRainDays(e.rain, 0),
        # ground_frost_frequency is a count of days with ground frost
        ground_frost_frequency = sum(e.gff),
        gdd = sum(e.gdd),
        hdd = sum(e.hdd),
        cumulative_precipitation = sum(e.rain),
        soil_moisture_index = sum(e.soil_moisture_index) / len(e.soil_moisture_index),
        soil_temperature_index = sum(e.soil_temperature_index) / len(e.soil_temperature_index),
        uv_index = sum(e.uv_index) / len(e.uv_index)
    )

    return d

def countRainDays(arr, val):
    count = 0
    for i in arr:
        if i > val:
            count += 1
    return count

def countGFF(arr1, arr2):
    count = 0
    for i in range(len(arr1)):
        if arr1[i] < 0 or arr2[i] < 0:
            count += 1
    return count