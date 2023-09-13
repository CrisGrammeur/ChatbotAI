from sqlalchemy import Boolean, Column, ForeignKey, Text, String
from sqlalchemy.orm import relationship
from uuid import uuid4

from config.database import Base

class Chat(Base):
    __tablename__ = "chats"

    id = Column(String, primary_key=True, index=True, default=str(uuid4()))
    query = Column(String, nullable=False)
    response = Column(String, nullable=False)
    discussion_id = Column(ForeignKey("discussions.id", ondelete='CASCADE'))
    is_liked = Column(Boolean, default=None)
    # description = Column(String, index=True)
    # chat_id = Column(ForeignKey("chats.id"), nullable=True)
    # is_ai = Column(Boolean, default=False)

    discussion = relationship("Discussion")
    # chat = relationship("Chat")