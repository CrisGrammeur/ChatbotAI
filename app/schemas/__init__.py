from schemas.user import UserRequest, UserResponse
from pydantic import BaseModel

class OurBaseModel(BaseModel):
    class Config:
        orm_mode = True