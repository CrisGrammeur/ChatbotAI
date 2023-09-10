from pydantic import BaseModel
# from uuid import UUID, uuid4
# from typing import Optional

class OurBaseModel(BaseModel):
    class Config:
        from_attributes = True

class MessageRequest(OurBaseModel):
    content: str