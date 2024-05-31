import json
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

# sbClient: Client = create_client(url, key)
sbClient: Client = create_client("https://iimtpbzfrdcuuklwnprq.supabase.co", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlpbXRwYnpmcmRjdXVrbHducHJxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTU4MTQ1MDMsImV4cCI6MjAzMTM5MDUwM30.o2gbIkgZaTQlFRLabs-abzkim462xatVumMJXo06m6w")

def sbGetFieldData(fieldid: int):
    return sbClient.rpc("get_field_data_by_id", {"fieldid":fieldid}).execute()

def sbGetFieldInfo():
    return sbClient.rpc("get_field_info").execute()

def sbCreateField(field_area, field_name: str, field_tph: float, field_health: float, crop_type: str, user_id: str):
    parsed_user_id = json.loads(user_id)
    # check if userID is null:
    if parsed_user_id == None:
        return sbClient.table("field_info").insert([{"field_area": field_area, "field_name": field_name, "field_tph": field_tph, "field_health": field_health, "crop_type": crop_type }]).execute()

    return sbClient.table("field_info").insert([{"field_area": field_area, "field_name": field_name, "field_tph": field_tph, "field_health": field_health, "crop_type": crop_type, "user_id": user_id}]).execute()

def sbUpdateField(field_id: int, field_area: object, field_name: str, field_tph: float, field_health: float, crop_type: str, user_id: int):
    return sbClient.rpc("update_field", {"fieldarea": field_area, "fieldname": field_name, "fieldtph": field_tph, "fieldhealth": field_health, "croptype": crop_type, "userid": user_id}).execute()

def sbDeleteField(field_id: int):
    return sbClient.rpc("delete_field", {"fieldid": field_id}).execute()

def sbCreateEntry(weather_temperature: float, weather_humidity: float, weather_uv: float, weather_rainfall: float, soil_moisture: float, soil_ph:float, soil_conductivity: float, is_manual: bool, field_id: int):
    return sbClient.rpc("create_entry", {"weathertemperature": weather_temperature, "weatherhumidity": weather_humidity, "weatheruv": weather_uv, "weatherrainfall": weather_rainfall, "soilmoisture": soil_moisture, "soilph": soil_ph, "soilconductivity": soil_conductivity, "ismanual": is_manual, "fieldid": field_id}).execute()

def sbUpdateEntry(entry_id: int, weather_temperature: float, weather_humidity: float, weather_uv: float, weather_rainfall: float, soil_moisture: float, soil_ph:float, soil_conductivity: float, is_manual: bool, field_id: int):
    return sbClient.rpc("update_entry", {"entryid": entry_id, "weathertemperature": weather_temperature, "weatherhumidity": weather_humidity, "weatheruv": weather_uv, "weatherrainfall": weather_rainfall, "soilmoisture": soil_moisture, "soilph": soil_ph, "soilconductivity": soil_conductivity, "ismanual": is_manual, "fieldid": field_id}).execute()

def sbDeleteEntry(entry_id: int):
    return sbClient.rpc("delete_entry", {"entryid": entry_id}).execute()