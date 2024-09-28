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
    def test_getTeamId_success(self, mock_get_client):
        # Mock the Supabase client response
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [{
            "team_id": "12345"
        }]
        
        team_id = supabaseFunctions.getTeamId("0edb30e5-fb47-457a-a1d8-30c7e9cb4098")
        assert team_id == {'role': 'unassigned','team_id': 'df98d7f1-2351-46fb-9792-ad70b8efd81a'}

    @patch('backend.database.supabaseInstance.supabaseInstance.get_client')
    def test_getTeamId_failure(self, mock_get_client):
        # Mock the Supabase client response
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.table.return_value.select.return_value.eq.return_value.execute.return_value.data = []

        team_id = supabaseFunctions.getTeamId("0f543694-dba7-4858-bb34-23e88c844b76")
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


