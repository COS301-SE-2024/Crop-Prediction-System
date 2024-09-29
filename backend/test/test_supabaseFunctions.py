import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from backend.definitions.field import Field
from backend.definitions.entry import Entry
from backend.definitions.crop import Crop
from backend.logic.calculateHectare import calculate_hectares_from_coordinates
from backend.logic.weather import Weather
from backend.database import supabaseInstance

# Import your supabaseFunctions class here
from backend.database.supabaseFunctions import supabaseFunctions

class TestSupabaseFunctions:
    @patch('backend.database.supabaseInstance.supabaseInstance.get_client')
    def test_getCrop_success(self, mock_get_client):
        # Mock the Supabase client response
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [{
            "name": "maize",
            "stages": {
                "sowing": {"day": 1},
                "germination": {"day": 10},
                "tillering": {"day": 20}
            }
        }]
        
        crop: Crop = supabaseFunctions.getCrop("maize")
        assert isinstance(crop, Crop)

    @patch('backend.database.supabaseInstance.supabaseInstance.get_client')
    def test_getCrop_failure(self, mock_get_client):
        # Mock the Supabase client response
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.table.return_value.select.return_value.eq.return_value.execute.return_value.data = []

    @patch('backend.database.supabaseInstance.supabaseInstance.get_client')
    def test_getCrop_failure(self, mock_get_client):
        # Mock the Supabase client response
        response = supabaseFunctions.getCrop("invalid")
        assert "error" in response
        assert response["error"] == "Failed to get crop"

    @patch('backend.database.supabaseInstance.supabaseInstance.get_client')
    def test_getCurrentStage(self, mock_get_client):
        crop = Crop(
            name="wheat",
            t_base=5,
            stages={
                "sowing": {"day": 1},
                "germination": {"day": 10},
                "tillering": {"day": 20}
            }
        )
        
        stage = supabaseFunctions.getCurrentStage(crop)
        today = datetime.today().timetuple().tm_yday
        if today >= 20:
            assert stage == "tillering"

    @patch('backend.database.supabaseInstance.supabaseInstance.get_client')
    def test_addToTeam(self,mock_get_client):
        team = {
            "user_id": "8e0ac7f0-8df0-4127-9081-1ab99ee6ad4c",
            "team_id": "2dcf4ec3-8d29-461c-a053-48a0b73d9a2a",
            "role": "farm_manager"
        }
        result = supabaseFunctions.addToTeam(team)
        assert "success" in result

    @patch('backend.database.supabaseInstance.supabaseInstance.get_client')
    def test_getTeamId_success(self, mock_get_client):
        # Mock the Supabase client response
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [{
            "team_id": "12345"
        }]
        
        team_id = supabaseFunctions.getTeamId("8e0ac7f0-8df0-4127-9081-1ab99ee6ad4c")
        assert team_id == {'role': 'farm_manager','team_id': '2dcf4ec3-8d29-461c-a053-48a0b73d9a2a'}

    @patch('backend.database.supabaseInstance.supabaseInstance.get_client')
    def test_getTeamId_failure(self, mock_get_client):
        # Mock the Supabase client response
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.table.return_value.select.return_value.eq.return_value.execute.return_value.data = []

        team_id = supabaseFunctions.getTeamId("7e0ac7f0-8df0-4127-9081-1ab99ee6ad4c")
        assert "error" in team_id
        assert team_id["error"] == "Failed to get team ID"

    @patch('backend.database.supabaseInstance.supabaseInstance.get_client')
    def test_getFieldData_fail(self, mock_get_client):
        # Mock the Supabase client response
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [{
            "field_id": "12345",
            "name": "Field 1",
            "coordinates": "POINT(1 1)"
        }]

        field = supabaseFunctions.getFieldData("12345")
        # check if field contains error
        assert "error" in field

    @patch('backend.database.supabaseInstance.supabaseInstance.get_client')
    def test_getFieldData_success(self, mock_get_client):
        # Mock the Supabase client response
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.table.return_value.select.return_value.eq.return_value.execute.return_value.data = []

        result = supabaseFunctions.getFieldData("3f76f41f-f166-4248-a7bb-56acef104f7a")
        assert isinstance(result, list), "Result should be a list"

        # Test that the list is not empty
        assert len(result) > 0, "Result list should not be empty"

        # Test the structure of each item in the list
        for item in result:
            assert isinstance(item, dict), "Each item in the result should be a dictionary"

            # Check for required keys
            required_keys = ['date', 'tempmax', 'tempmin', 'tempdiurnal', 'tempmean', 'pressure', 'humidity', 
                             'dew_point', 'clouds', 'rain', 'uvi', 'soil_temperature', 'soil_moisture', 
                             'pred_health', 'pred_yield', 'pred_sprayability', 'field_id', 'summary', 'id']
            for key in required_keys:
                assert key in item, f"Each item should have a '{key}' key"

            # Check data types of some values
            assert isinstance(item['date'], str), "'date' should be a string"
            assert isinstance(item['tempmax'], (int, float)), "'tempmax' should be a number"
            assert isinstance(item['tempmin'], (int, float)), "'tempmin' should be a number"
            assert isinstance(item['field_id'], str), "'field_id' should be a string"
            assert isinstance(item['summary'], str), "'summary' should be a string"
            assert isinstance(item['id'], int), "'id' should be an integer"

        # Test specific data points (you may want to adjust these based on your actual data)
        assert result[0]['date'] == '2024-09-15', "First item should be for date 2024-09-15"
        assert result[-1]['date'] == '2024-10-05', "Last item should be for date 2024-10-04"

        # Test that dates are in order
        dates = [item['date'] for item in result]
        assert dates == sorted(dates), "Dates should be in ascending order"

        # Test that all items have the same field_id
        field_ids = set(item['field_id'] for item in result)
        assert len(field_ids) == 1, "All items should have the same field_id"

        # Test range of some values
        for item in result:
            assert -50 <= item['tempmax'] <= 50, "tempmax should be between -50 and 50"
            assert -50 <= item['tempmin'] <= 50, "tempmin should be between -50 and 50"
            assert 0 <= item['humidity'] <= 100, "humidity should be between 0 and 100"
            assert 0 <= item['pred_health'] <= 1, "pred_health should be between 0 and 1"
            assert item['pred_sprayability'] >= 0, "pred_sprayability should be non-negative"

    @patch('backend.database.supabaseInstance.supabaseInstance.get_client')
    def test_getFieldInfo(self, mock_get_client):
        mock_get_client = MagicMock()
        mock_get_client.return_value = mock_get_client
        mock_get_client.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [{
            "field_id": "14420bc8-48e3-47bc-ab83-1a6498380588",
            "name": "Backyard",
            "coordinates": "POINT(1 1)"
        }]
        result : Field = supabaseFunctions.getFieldInfo("14420bc8-48e3-47bc-ab83-1a6498380588")
        assert isinstance(result, Field)
        assert result.field_id == "14420bc8-48e3-47bc-ab83-1a6498380588"
        assert result.field_name == "Backyard"

    @patch('backend.database.supabaseInstance.supabaseInstance.get_client')
    def test_getFieldInfo_fail(self, mock_get_client):
        mock_get_client = MagicMock()
        mock_get_client.return_value = mock_get_client
        mock_get_client.table.return_value.select.return_value.eq.return_value.execute.return_value.data = []
        result = supabaseFunctions.getFieldInfo("14420bc7-48e3-47bc-ab83-1a6498380588")
        assert "error" in result
        assert result["error"] == "Failed to get field info"

    @patch('backend.database.supabaseInstance.supabaseInstance.get_client')
    def test_getTeamFieldData(self, mock_get_client):
        result = supabaseFunctions.getTeamFieldData(supabaseFunctions,"17383e3d-f211-4724-8515-8c4cb836c812",1)
        assert isinstance(result, list)

    @patch('backend.database.supabaseInstance.supabaseInstance.get_client')
    def test_getTeamFieldDataN0(self, mock_get_client):
        result = supabaseFunctions.getTeamFieldData(supabaseFunctions,"17383e3d-f211-4724-8515-8c4cb836c812",0)
        assert isinstance(result, list)

    def test_getTeamFieldData_invalid(self):
        result = supabaseFunctions.getTeamFieldData(supabaseFunctions,"17383e3f-f211-4724-8515-8c4cb836c812",1)
        assert "error" in result
        assert result["error"] == "Data not found. Team ID may be invalid or may not have any data."

    @patch('backend.database.supabaseInstance.supabaseInstance.get_client')
    def test_getPastYieldAvg(self, mock_get_client):
        result = supabaseFunctions.getPastYieldAvg("maize")
        assert isinstance(result, float)

    @patch('backend.database.supabaseInstance.supabaseInstance.get_client')
    def test_getPastYieldAvg_fail(self, mock_get_client):
        result = supabaseFunctions.getPastYieldAvg("invalid")
        assert "error" in result
        assert result["error"] == "Failed to get past yield average"

    @patch('backend.database.supabaseInstance.supabaseInstance.get_client')
    def test_createField_fail(self, mock_get_client):
        field = Field(
            field_name = "Stephan Test 2",
            crop_type = "wheat",
            field_area = {
                "type": "Polygon",
                "coordinates": [[-25.87074931861521, 28.159573936176287], [-25.870773452610735, 28.160054051589952], [-25.871036512841457, 28.160062098216997], [-25.87101479229413, 28.159563207340227]]
            },
        )
        result = supabaseFunctions.createField(field)
        assert "error" in result

    @patch('backend.database.supabaseInstance.supabaseInstance.get_client')
    def test_updateField(self, mock_get_client):
        field = Field(
            field_id = "2fea8a15-cf10-4db3-90b4-e2a5e3caabf8",
            field_name = "Stephan Test Field",
            crop_type = "wheat",
        )
        result = supabaseFunctions.updateField(field)
        assert "status" in result

    # @patch('backend.database.supabaseInstance.supabaseInstance.get_client')
    # def test_deleteField(self, mock_get_client):
    #     result = supabaseFunctions.deleteField("69908502-804d-457a-85bf-c0c6c85b289a")
    #     assert "status" in result

    @patch('backend.database.supabaseInstance.supabaseInstance.get_client')
    def test_updateEntry(self,mock_get_client):
        entry = {
            "field_id": "2fea8a15-cf10-4db3-90b4-e2a5e3caabf8",
            "date": "2024-09-15",
            "tempmax": 30,
            "tempmin": 20,
            "tempdiurnal": 10,
            "tempmean": 25,
            "pressure": 1010,
            "humidity": 50,
            "dew_point": 15,
            "clouds": 20,
            "rain": 0,
            "uvi": 5,
            "soil_temperature": 25,
            "soil_moisture": 50,
            "pred_health": 0.5,
            "pred_yield": 0.5,
            "pred_sprayability": 50,
            "summary": "Sunny day"
        }
        result = supabaseFunctions.updateEntry(entry)
        assert "status" in result
        assert "error_message" in result

    @patch('backend.database.supabaseInstance.supabaseInstance.get_client')
    def test_getTeamFields(self, mock_get_client):
        result = supabaseFunctions.getTeamFields("17383e3d-f211-4724-8515-8c4cb836c812")
        assert isinstance(result, list)

    @patch('backend.database.supabaseInstance.supabaseInstance.get_client')
    def test_addToTeam(self, mock_get_client):
        team = {
            "user_id": "8e0ac7f0-8df0-4127-9081-1ab99ee6ad4c",
            "team_id": "2dcf4ec3-8d29-461c-a053-48a0b73d9a2a",
            "role": "farm_manager"
        }
        result = supabaseFunctions.addToTeam(team)
        assert "success" in result

    @patch('backend.database.supabaseInstance.supabaseInstance.get_client')
    def test_removeFromTeam(self, mock_get_client):
        result = supabaseFunctions.removeFromTeam("8e0ac7f0-8df0-4127-9081-1ab99ee6ad4c")
        assert "success" in result

    @patch('backend.database.supabaseInstance.supabaseInstance.get_client')
    def test_getTeamDetails(self, mock_get_client):
        result = supabaseFunctions.getTeamDetails("17383e3d-f211-4724-8515-8c4cb836c812")
        assert isinstance(result, list)

    @patch('backend.database.supabaseInstance.supabaseInstance.get_client')
    def test_sendMessage(self, mock_get_client):
        # parameter of send message
        # {
        #     "team_id": "17383e3d-f211-4724-8515-8c4cb836c812",
        #     "user_email": "xavierrynolds@gmail.com",
        #     "user_name": "Xavier Reynolds",
        #     "message": "Testing 4"
        # }
        message = {
            "team_id": "2dcf4ec3-8d29-461c-a053-48a0b73d9a2a",
            "user_email": "stephantestuser@gmail.com",
            "user_name": "Stephan Test User",
            "message": "Testing 4"
        }
        result = supabaseFunctions.sendMessage(message)
        assert "success" in result

    @patch('backend.database.supabaseInstance.supabaseInstance.get_client')
    def test_getTeamMessages(self, mock_get_client):
        result = supabaseFunctions.getTeamMessages("2dcf4ec3-8d29-461c-a053-48a0b73d9a2a")
        assert isinstance(result, list)

    @patch('backend.database.supabaseInstance.supabaseInstance.get_client')
    def test_updateUser(self, mock_get_client):
        user = {
            "id": "8e0ac7f0-8df0-4127-9081-1ab99ee6ad4c",
            "full_name": "Stephan Test User" 
        }
        result = supabaseFunctions.updateUser(user)
        assert "success" in result

    @patch('backend.database.supabaseInstance.supabaseInstance.get_client')
    def test_getUser(self, mock_get_client):
        result = supabaseFunctions.getUser("8e0ac7f0-8df0-4127-9081-1ab99ee6ad4c")
        assert isinstance(result, dict)

    @patch('backend.database.supabaseInstance.supabaseInstance.get_client')
    def test_getTeamYield(self, mock_get_client):
        result = supabaseFunctions.getTeamYield("17383e3d-f211-4724-8515-8c4cb836c812")
        assert isinstance(result, list)

    @patch('backend.database.supabaseInstance.supabaseInstance.get_client')
    def test_getMarketData(self, mock_get_client):
        result = supabaseFunctions.getMarketData("wheat")
        assert isinstance(result, list)

    @patch('backend.database.supabaseInstance.supabaseInstance.get_client')
    def test_addFieldToSensor(self, mock_get_client):
        field = {
            "field_id": "9383ffd2-4e11-4053-9730-7439053a5a99",
            "sensor_id": "2CF7F1202520006A"
        }
        result = supabaseFunctions.addFieldToSensor("9383ffd2-4e11-4053-9730-7439053a5a99","2CF7F1202520006A")
        assert "success" in result

