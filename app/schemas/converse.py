from pydantic import BaseModel
# from uuid import UUID, uuid4
# from typing import Optional

class OurBaseModel(BaseModel):
    class Config:
        from_attributes = True

class addConverse(OurBaseModel):
    query: str
    answer: str
    
    
class setLike(OurBaseModel):
    converse_id: str
    is_liked: bool

# To use with a postgres database
# class DiscussionResponse(OurBaseModel):
#     id: str
#     name: str
#     email: str
#     bio: str
#     location: str
#     is_active: bool