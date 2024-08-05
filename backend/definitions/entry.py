from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import date

class Entry(BaseModel):
    id: Optional[UUID] = None      
    field_id: Optional[int] = None
    date: Optional[date] = None
    summary: Optional[str] = None
    tempMax: Optional[float] = None  
    tempMin: Optional[float] = None 
    tempDiurnal: Optional[float] = None
    tempMean: Optional[float] = None
    pressure: Optional[float] = None
    humidity: Optional[float] = None
    dew_point: Optional[float] = None
    wind_speed: Optional[float] = None
    wind_deg: Optional[float] = None
    wind_gust: Optional[float] = None
    clouds: Optional[float] = None
    pop: Optional[float] = None
    rain: Optional[float] = None
    uvi: Optional[float] = None
    gff: Optional[float] = None
    gdd: Optional[float] = None
    hdd: Optional[float] = None
    soil_moisture: Optional[float] = None
    soil_temperature: Optional[float] = None
    pet : Optional[float] = None
