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
        clouds=50,
        rain=0.5,
        uvi=5,
        soil_moisture=0.5,
        soil_temperature=15
    )

# Test initialization of Weather class
def test_weather_init(weather):
    assert isinstance(weather, Weather)