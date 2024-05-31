from pydantic import BaseModel
from typing import Optional

class Field(BaseModel):
    field_id: Optional[int] = None
    field_area: Optional[object] = None
    field_name: Optional[str] = None
    field_tph: Optional[float] = None
    field_health: Optional[float] = None
    crop_type: Optional[str] = None
    user_id: Optional[str] = None