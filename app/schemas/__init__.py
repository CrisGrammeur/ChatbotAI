from schemas.user import UserRequest, UserResponse
from schemas.login import Token, TokenData
from pydantic import BaseModel

# class OurBaseModel(BaseModel):
#     class Config:
#         orm_mode = True