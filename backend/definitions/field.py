from pydantic import BaseModel
from typing import Optional

class Field(BaseModel):
    field_id: Optional[int] = None
    field_area: Optional[object] = None
    hectare: Optional[float] = None
    field_name: Optional[str] = None
    crop_type: Optional[str] = None
    team_id: Optional[str] = None