import pytest
from unittest.mock import patch, MagicMock
from backend.IoT.getData import getNewSensorData
import datetime
from uuid import uuid4

# get data is already a function hence no fixture

def test_get_single_line_data():
    sensorID = '2CF7F12025200009'
    result = getNewSensorData(sensorID)
    assert result is not None

