from pydantic import BaseModel, Field
from typing import Dict, List

class Crop(BaseModel):
    t_base: float = Field(..., description="Base temperature for the crop.")
    stages: Dict[str, Dict[str, List[float]]] = Field(
        ..., description="Associative 3D array for crop growth stages."
    )

# Usage:
# wheat = Crop(
#     t_base=5.0, 
#     stages={
#         "sowing": {
#             "start_day": 1
#         },
#         "germination": {
#             "start_day": 2
#         },
#         ...
#     }
# )
