from pydantic import BaseModel, EmailStr
from uuid import UUID, uuid4
from typing import Optional

class OurBaseModel(BaseModel):
    class Config:
        from_attributes = True

class UserRequest(OurBaseModel):
    # id: Optional[UUID] = uuid4
    name: str
    email: EmailStr
    password: str
    bio: str
    location: str

# To use with a postgres database
class UserResponse(OurBaseModel):
    id: str
    name: str
    email: str
    bio: str
    location: str
    is_active: bool