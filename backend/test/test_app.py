import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock

from database.supabaseFunctions import supabaseFunctions
from database.field import Field
from database.entry import Entry
from app import app, api_instance  # Adjust the import according to your project structure

# Create a TestClient instance
client = TestClient(app)

@pytest.fixture
def mock_supabase_functions(mocker):
    mocker.patch.object(supabaseFunctions, 'getFieldInfo', return_value={"data": "field info"})
    mocker.patch.object(supabaseFunctions, 'getFieldData', return_value={"data": "field data"})
    mocker.patch.object(supabaseFunctions, 'createField', return_value={"success": "Field created"})
    mocker.patch.object(supabaseFunctions, 'updateField', return_value={"success": "Field updated"})
    mocker.patch.object(supabaseFunctions, 'deleteField', return_value={"success": "Field deleted"})
    mocker.patch.object(supabaseFunctions, 'createEntry', return_value={"success": "Entry created"})
    mocker.patch.object(supabaseFunctions, 'updateEntry', return_value={"success": "Entry updated"})
    mocker.patch.object(supabaseFunctions, 'deleteEntry', return_value={"success": "Entry deleted"})
    mocker.patch.object(supabaseFunctions, 'test', return_value={"success": "All tests passed", "tests_passed": 8})

def test_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "Welcome": "Welcome to the TerraByte API",
        "Link to Documentation": "https://documenter.getpostman.com/view/26558432/2sA3Qwaoyd"
    }

# def test_init_model():
#     response = client.get("/startModel")
#     assert response.status_code == 200
#     assert response.json() == api_instance.ml.startModel()

def test_get_field_info(mock_supabase_functions):
    response = client.get("/getFieldInfo?fieldid=1")
    assert response.status_code == 200
    assert response.json() == {"data": "field info"}

def test_get_field_data(mock_supabase_functions):
    response = client.get("/getFieldData?fieldid=1")
    assert response.status_code == 200
    assert response.json() == {"data": "field data"}

def test_create_field(mock_supabase_functions):
    field_info = {
        "field_area": 1000,
        "field_name": "Test Field",
        "field_tph": 50.0,
        "field_health": 80.0,
        "crop_type": "Corn",
        "user_id": "user123"
    }
    response = client.post("/createField", json=field_info)
    assert response.status_code == 200
    assert response.json() == {"success": "Field created"}

def test_update_field(mock_supabase_functions):
    field_info = {
        "field_id": 1,
        "field_area": 1000,
        "field_name": "Updated Field",
        "field_tph": 55.0,
        "field_health": 85.0,
        "crop_type": "Wheat",
        "user_id": "user123"
    }
    response = client.put("/updateField", json=field_info)
    assert response.status_code == 200
    assert response.json() == {"success": "Field updated"}

def test_delete_field(mock_supabase_functions):
    response = client.post("/deleteField", json={"field_id": 1})
    assert response.status_code == 200
    assert response.json() == {"success": "Field deleted"}

def test_create_entry(mock_supabase_functions):
    entry_info = {
        "weather_temperature": 30.5,
        "weather_humidity": 60.0,
        "weather_uv": 5.0,
        "weather_rainfall": 100.0,
        "soil_moisture": 20.0,
        "soil_ph": 6.5,
        "soil_conductivity": 1.0,
        "is_manual": True,
        "field_id": 1
    }
    response = client.post("/createEntry", json=entry_info)
    assert response.status_code == 200
    assert response.json() == {"success": "Entry created"}

def test_update_entry(mock_supabase_functions):
    entry_info = {
        "entry_id": 0,
        "weather_temperature": 32.0,
        "weather_humidity": 65.0,
        "weather_uv": 6.0,
        "weather_rainfall": 120.0,
        "soil_moisture": 22.0,
        "soil_ph": 6.8,
        "soil_conductivity": 1.1,
        "is_manual": False,
        "field_id": 1
    }
    response = client.put("/updateEntry", json=entry_info)
    assert response.status_code == 200
    assert response.json() == {"success": "Entry updated"}

def test_delete_entry(mock_supabase_functions):
    response = client.post("/deleteEntry", json={"entry_id": 1})
    assert response.status_code == 200
    assert response.json() == {"success": "Entry deleted"}

def test_test(mock_supabase_functions):
    response = client.get("/test")
    assert response.status_code == 200
    assert response.json() == {
        "success": "All tests passed",
        "tests_passed": 8
    }

# supabaseFunctions
# Path: Crop-Prediction-System/backend/database/supabaseFunctions.py

def test_get_field_info():
    sb = supabaseFunctions()
    response = sb.getFieldInfo("0")
    assert response != []

def test_get_field_data():
    sb = supabaseFunctions()
    response = sb.getFieldData("0")
    assert response != []

def test_create_field():
    sb = supabaseFunctions()
    field_info = Field(
        field_area=1000,
        field_name="Test Field",
        field_tph=50.0,
        field_health=80.0,
        crop_type="Corn",
        user_id="user123"
    )
    assert sb.createField(field_info) == {"success": "Field created"}

def test_update_field():
    sb = supabaseFunctions()
    field_info = Field(
        field_id=0,
        field_area=1000,
        field_name="Updated Field",
        field_tph=55.0,
        field_health=85.0,
        crop_type="Wheat"
    )
    assert sb.updateField(field_info) == {"success": "Field updated"}

# def test_delete_field():
#     sb = supabaseFunctions()
#     response = sb.deleteField(0)
#     assert response == {"success": "Field deleted"}

def test_create_entry():
    sb = supabaseFunctions()
    entry_info = Entry(
        entry_id=1,
        weather_temperature=30.5,
        weather_humidity=60.0,
        weather_uv=5.0,
        weather_rainfall=100.0,
        soil_moisture=20.0,
        soil_ph=6.5,
        soil_conductivity=1.0,
        is_manual=True,
        field_id=0
    )
    assert sb.createEntry(entry_info) == {"success": "Entry created"}

def test_update_entry():
    sb = supabaseFunctions()
    entry_info = Entry(
        entry_id=1,
        weather_temperature=32.0,
        weather_humidity=65.0,
        weather_uv=6.0,
        weather_rainfall=120.0,
        soil_moisture=22.0,
        soil_ph=6.8,
        soil_conductivity=1.1,
        is_manual=False,
        field_id=0
    )
    assert sb.updateEntry(entry_info) == {"success": "Entry updated"}

def test_delete_entry():
    sb = supabaseFunctions()
    response = sb.deleteEntry(1)
    assert response == {"success": "Entry deleted"}

def test_test():
    sb = supabaseFunctions()
    response = sb.test()
    assert response == {
        "success": "All tests passed",
        "tests_passed": 8
    }