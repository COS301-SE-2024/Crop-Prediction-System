from pydantic import BaseModel, Field
from typing import Dict, List

class Crop(BaseModel):
    t_base: float = Field(..., description="Base temperature for the crop.")
    stages: Dict[str, Dict[str, float]] = Field(
        ..., description="Associative 3D array for crop growth stages."
    )