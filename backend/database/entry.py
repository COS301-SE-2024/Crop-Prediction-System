from pydantic import BaseModel
from typing import Optional

class Entry(BaseModel):
    entry_id: Optional[int] = None
    weather_temperature: Optional[float] = None
    weather_humidity: Optional[float] = None
    weather_uv: Optional[float] = None
    weather_rainfall: Optional[float] = None
    soil_moisture: Optional[float] = None
    soil_ph: Optional[float] = None
    soil_conductivity: Optional[float] = None
    is_manual: Optional[bool] = None
    field_id: Optional[int] = None