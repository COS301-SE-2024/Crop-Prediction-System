from pydantic import BaseModel, Field
from typing import Dict, List

class Crop(BaseModel):
    name: str = Field(..., description="Name of the crop.")
    stages: Dict[str, Dict[str, float]] = Field(
        ..., description="Associative 3D array for crop growth stages."
    )

