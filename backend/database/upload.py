from typing import List, Optional
from pydantic import BaseModel
from uuid import UUID
from datetime import date

class FieldData(BaseModel):
    field_id: Optional[UUID] = None
    location: Optional[List[float]] = None
    health: Optional[List[float]] = None
    ton_per_hectare: Optional[List[float]] = None
    sprayability: Optional[List[float]] = None
    temperature: Optional[List[dict]] = None  # Example dict: {'min': float, 'max': float}
    precipitation: Optional[List[float]] = None
    probability_precipitation: Optional[List[float]] = None
    humidity: Optional[List[float]] = None
    wind: Optional[List[float]] = None
    pressure: Optional[List[float]] = None
    cloud_cover: Optional[List[float]] = None
    soil_moisture: Optional[float] = None
    phosphorus: Optional[float] = None
    potassium: Optional[float] = None
    nitrogen: Optional[float] = None
    fertilizer: Optional[str] = None
