from sqlalchemy import Boolean, Column, ForeignKey, text, String
from sqlalchemy.orm import relationship
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID

from config.database import Base

class Chat(Base):
    __tablename__ = "chats"

    id = Column(String, primary_key=True, index=True, default=str(uuid4()))
    content = Column(String)
    description = Column(String, index=True)
    owner_id = Column(String, ForeignKey("users.id"))

    owner = relationship("User", back_populates="chats")