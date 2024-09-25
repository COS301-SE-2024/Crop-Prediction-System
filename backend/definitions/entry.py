from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class Entry(BaseModel):
    id: Optional[UUID] = None      
    field_id: Optional[UUID] = None
    timestamp: Optional[int] = None
    summary: Optional[str] = None
    tempMax: Optional[float] = None  
    tempMin: Optional[float] = None 
    tempDiurnal: Optional[float] = None
    tempMean: Optional[float] = None
    pressure: Optional[float] = None
    humidity: Optional[float] = None
    dew_point: Optional[float] = None
    clouds: Optional[float] = None
    rain: Optional[float] = None
    uvi: Optional[float] = None
    soil_moisture: Optional[float] = None
    soil_temperature: Optional[float] = None
    sprayability: Optional[float] = None
    health: Optional[float] = None
