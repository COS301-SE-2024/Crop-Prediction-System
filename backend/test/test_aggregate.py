import pytest
from backend.logic.aggregate import Aggregate
from backend.definitions.entry import Entry
from backend.definitions.data import Data
from typing import List
import uuid

# Create a test class
a = Aggregate()

# Field ID
field_id = str(uuid.uuid4())

# Create 2 random entries
entry1 = Entry(
    id = uuid.uuid4(),    
    field_id = field_id,
    timestamp = 1,
    summary = 'sunny',
    tempMax = 20,
    tempMin = 15,
    tempDiurnal = 5,
    tempMean = 17.5,
    pressure = 1000,
    humidity = 50,
    dew_point = 0,
    wind_speed = 10,
    wind_deg = 180,
    wind_gust = 1,
    clouds = 10,
    pop = 0,
    rain = 1,
    uvi = 0,
    gff = 0,
    gdd = 4,
    hdd = 1,
    soil_moisture = 0,
    soil_temperature = 0,
    pet = 0
)


entry2 = Entry(
    id = uuid.uuid4(),    
    field_id = field_id,
    timestamp = 1,
    summary = 'sunny',
    tempMax = 25,
    tempMin = 15,
    tempDiurnal = 10,
    tempMean = 20,
    pressure = 1000,
    humidity = 50,
    dew_point = 0,
    wind_speed = 10,
    wind_deg = 180,
    wind_gust = 1,
    clouds = 10,
    pop = 0,
    rain = 1,
    uvi = 0,
    gff = 0,
    gdd = 4,
    hdd = 1,
    soil_moisture = 0,
    soil_temperature = 0,
    pet = 0
)

# Create a list of entries
entries = [entry1, entry2]

# Stage
stage = 'test'

# Test the aggregate function
# def aggregate(entries: List[Entry], stage: str, field_id: str, test=False) -> Data:
def test_aggregate():
    result = a.aggregate(entries, stage, field_id, test=True)

    expectedGroundFrostFrequency = entry1.gff + entry2.gff
    expectedPrecipitation = entry1.rain + entry2.rain
    # Test averages
    assert result.mean_temperature == ((entry1.tempMean + entry2.tempMean) / 2)
    assert result.maximum_temperature == ((entry1.tempMax + entry2.tempMax) / 2)
    assert result.minimum_temperature == ((entry1.tempMin + entry2.tempMin) / 2)
    # Test sums
    assert result.ground_frost_frequency == expectedGroundFrostFrequency
    assert result.cumulative_precipitation == expectedPrecipitation
    # Test the return type
    assert isinstance(result, Data)
    # Test the return value
    assert a.aggregate([], stage, field_id, test=True) == None

def test_upload():
    result = a.upload(entries, field_id, test=True)

    assert result == None
    assert a.upload([], field_id) == None

def test_countRainDays():
    arr = [1, 2, 3, 4, 5]
    val = 3
    result = a.countRainDays(arr, val)
    expected = 2
    assert result == expected
    assert a.countRainDays([], val) == 0
    assert a.countRainDays(arr, 0) == 5

def test_countGFF():
    arr1 = [1, 2, 3, 4, 5]
    arr2 = [1, 2, 3, 4, 5]
    result = a.countGFF(arr1, arr2)
    expected = 0
    assert result == expected
    assert a.countGFF([], arr2) == 0
    assert a.countGFF(arr1, []) == 0
    arr1 = [-1, 2, 3, 4, 5]
    arr2 = [1, 2, 3, 4, 5]
    result = a.countGFF(arr1, arr2)
    expected = 1
    assert result == expected




