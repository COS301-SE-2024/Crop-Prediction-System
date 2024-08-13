import pytest
from unittest.mock import patch, MagicMock
from backend.logic.weather import Weather
from backend.definitions.entry import Entry
from backend.definitions.crop import Crop
import datetime
from uuid import uuid4

@pytest.fixture
def weather():
    return Weather()

@pytest.fixture
def mock_crop():
    return Crop(
        name="Example crop",
        t_base=10,
        stages={
            "sowing": {"day": 111},
            "germination": {"day": 151},
            "tillering": {"day": 182},
            "heading": {"day": 243},
            "maturity": {"day": 304}
        }
    )

@pytest.fixture
def entry():
    return Entry(
        tempMax=20,
        tempMin=10,
        tempDiurnal=10,
        tempMean=15,
        pressure=1000,
        humidity=50,
        dew_point=5,
        wind_speed=10,
        wind_deg=180,
        wind_gust=15,
        clouds=50,
        pop=0.5,
        rain=0.5,
        uvi=5,
        gff=0,
        gdd=5,
        hdd=5,
        soil_moisture=0.5,
        soil_temperature=15,
        pet=5
    )

def test_get_features(entry, mock_crop):
    Weather.get_features(entry, mock_crop)
    assert entry.tempMean == 15
    assert entry.gdd == 5
    assert entry.hdd == 0
    assert entry.gff == 0
    assert entry.tempDiurnal == 10

def test_calculate_sprayability(entry, weather):
    expected_sprayability = 21
    sprayability = round(weather.calculate_sprayability(entry), 0)
    assert sprayability == expected_sprayability

def test_calculate_health(entry, weather):
    expected_health = 96
    health = round(weather.calculate_health(entry), 0)
    assert health == expected_health
