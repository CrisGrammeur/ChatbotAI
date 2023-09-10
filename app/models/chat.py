from sqlalchemy import Boolean, Column, ForeignKey, Text, String
from sqlalchemy.orm import relationship
from uuid import uuid4

from config.database import Base

class Chat(Base):
    __tablename__ = "chats"

    id = Column(String, primary_key=True, index=True, default=str(uuid4()))
    content = Column(Text, nullable=False)
    # description = Column(String, index=True)
    discussion_id = Column(ForeignKey("discussions.id", ondelete='CASCADE'))
    chat_id = Column(ForeignKey("chats.id"), nullable=True)
    is_ai = Column(Boolean, default=False)

    discussion = relationship("Discussion")
    # chat = relationship("Chat")