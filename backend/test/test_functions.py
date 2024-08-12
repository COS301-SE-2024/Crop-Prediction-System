import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from backend.definitions.field import Field
from backend.definitions.entry import Entry
from backend.definitions.crop import Crop
from backend.logic.calculateHectare import calculate_hectares_from_coordinates
from backend.logic.weather import Weather
from backend.logic.aggregate import Aggregate
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
            "name": "wheat",
            "t_base": 5,
            "stages": {
                "sowing": {"day": 1},
                "germination": {"day": 10},
                "tillering": {"day": 20}
            }
        }]
        
        crop = supabaseFunctions.getCrop("wheat")
        assert crop.name == "wheat"
        assert crop.t_base == 10
        assert "tillering" in crop.stages

    @patch('backend.database.supabaseInstance.supabaseInstance.get_client')
    def test_getCrop_failure(self, mock_get_client):
        # Mock the Supabase client response
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.table.return_value.select.return_value.eq.return_value.execute.return_value.data = []

        crop = supabaseFunctions.getCrop("invalid_crop")
        assert "error" in crop
        assert crop["error"] == "Data not found. Crop type may be invalid or may not have any data."

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
        elif today >= 10:
            assert stage == "germination"
        else:
            assert stage == "sowing"
