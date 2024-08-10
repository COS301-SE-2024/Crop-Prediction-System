import unittest
from unittest.mock import patch, MagicMock
from backend.definitions.crop import Crop
from backend.definitions.field import Field
from backend.definitions.entry import Entry
from datetime import date
from backend.database import supabaseFunctions

class TestSupabaseFunctions(unittest.TestCase):

    @patch('supabaseFunctions.supabaseInstance')
    def setUp(self, mock_supabase_instance):
        # Mock the Supabase client
        self.mock_sbClient = MagicMock()
        mock_supabase_instance.supabaseInstance().get_client.return_value = self.mock_sbClient
        self.sf = supabaseFunctions.supabaseFunctions()

    def test_getCrop_success(self):
        # Mock the response from Supabase
        crop_data = [{"name": "wheat", "t_base": 5, "stages": {"sowing": {"day": 1}, "germination": {"day": 30}}}]
        self.mock_sbClient.table().select().eq().execute.return_value.data = crop_data
        
        crop = self.sf.getCrop("wheat")

        # Assertions
        self.assertIsInstance(crop, Crop)
        self.assertEqual(crop.name, "wheat")
        self.assertEqual(crop.t_base, 5)
        self.assertIn("sowing", crop.stages)

    def test_getCrop_failure(self):
        # Mock an empty response
        self.mock_sbClient.table().select().eq().execute.return_value.data = []

        response = self.sf.getCrop("invalid_crop")

        # Assertions
        self.assertIn("error", response)
        self.assertEqual(response["error"], "Data not found. Crop type may be invalid or may not have any data.")

    def test_getCurrentStage(self):
        crop = Crop(
            name="wheat",
            t_base=5,
            stages={"sowing": {"day": 1}, "germination": {"day": 30}, "tillering": {"day": 60}}
        )

        # Mock today's date
        with patch('supabaseFunctions.date') as mock_date:
            mock_date.today.return_value = date(2024, 3, 1)  # March 1st
            mock_date.today().timetuple.return_value.tm_yday = 60  # 60th day of the year

            stage = self.sf.getCurrentStage(crop)

            # Assertions
            self.assertEqual(stage, "tillering")

    @patch('supabaseFunctions.Weather')
    def test_fetchWeatherForAllFields(self, mock_weather):
        # Mock the response from Supabase for fields
        field_data = [{"id": "field1", "crop_type": "wheat", "field_area": [[0, 0], [1, 1]]}]
        self.mock_sbClient.table().select().execute.return_value.data = field_data

        # Mock weather fetch
        mock_weather.getWeather.return_value = {"status": "success"}

        response = self.sf.fetchWeatherForAllFields()

        # Assertions
        self.assertEqual(response["success"], "Weather fetched for all fields")
        mock_weather.getWeather.assert_called_with(0, 0, "field1", mock.ANY)  # Assuming Crop object is passed as last argument

    @patch('supabaseFunctions.supabaseInstance')
    def test_createField(self, mock_supabase_instance):
        field_info = Field(
            field_id=None,
            field_area={"coordinates": [[0, 0], [1, 1]]},
            field_name="Test Field",
            crop_type="wheat",
            team_id="team1",
            hectare=1.0
        )

        # Mock the Supabase client
        self.mock_sbClient = MagicMock()
        mock_supabase_instance.supabaseInstance().get_client.return_value = self.mock_sbClient

        # Mock the response from Supabase for field creation
        self.mock_sbClient.table().insert().returning().execute.return_value.data = [{"id": "field1"}]

        response = self.sf.createField(field_info)

        # Assertions
        self.assertEqual(response["status"], "success")
        self.assertEqual(response["id"], "field1")

    # Additional tests can be written similarly for the remaining methods.

if __name__ == "__main__":
    unittest.main()
