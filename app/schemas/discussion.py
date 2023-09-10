from pydantic import BaseModel
# from uuid import UUID, uuid4
# from typing import Optional

class OurBaseModel(BaseModel):
    class Config:
        from_attributes = True

class DiscussionRequest(OurBaseModel):
    title: str

# To use with a postgres database
class DiscussionResponse(OurBaseModel):
    id: str
    name: str
    email: str
    bio: str
    location: str
    is_active: bool