from pydantic import BaseModel, Field

class Data(BaseModel):
    year: int
    stage: str = Field(..., description="Growth stage of the crop")
    pet: float = Field(..., description="Potential Evapotranspiration")
    cloud_cover: float = Field(..., description="Cloud cover percentage")
    maximum_temperature: float = Field(..., description="Maximum temperature (°C)")
    minimum_temperature: float = Field(..., description="Minimum temperature (°C)")
    vapour_pressure: float = Field(..., description="Vapour pressure (hPa)")
    diurnal_temperature_range: float = Field(..., description="Diurnal temperature range (°C)")
    mean_temperature: float = Field(..., description="Mean temperature (°C)")
    precipitation: float = Field(..., description="Precipitation (mm)")
    rain_days: int = Field(..., description="Number of rain days")
    ground_frost_frequency: int = Field(..., description="Frequency of ground frost")
    gdd: float = Field(..., description="Growing Degree Days")
    hdd: float = Field(..., description="Heating Degree Days")
    cumulative_precipitation: float = Field(..., description="Cumulative precipitation (mm)")
    soil_moisture_index: float = Field(..., description="Soil moisture index")
    soil_temperature_index: float = Field(..., description="Soil temperature index")
    uv_index: float = Field(..., description="UV index")
