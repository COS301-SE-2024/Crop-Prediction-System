from pydantic import BaseModel

class Field(BaseModel):
    field_area: object
    field_name: str
    field_tph: float
    field_health: float
    crop_type: str
    user_id: str