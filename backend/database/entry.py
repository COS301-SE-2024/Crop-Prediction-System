from pydantic import BaseModel

class Entry(BaseModel):
    weather_temperature: float
    weather_humidity: float
    weather_uv: float
    weather_rainfall: float
    soil_moisture: float
    soil_ph: float
    soil_conductivity: float
    is_manual: bool
    field_id: int