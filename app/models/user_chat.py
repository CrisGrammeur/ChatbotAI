from sqlalchemy import Boolean, Column, ForeignKey, text, String, Date,Integer
from sqlalchemy.orm import relationship
from uuid import uuid4

from config.database import Base

class User_chat(Base):
    __tablename__ = "user_chat"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, unique=True, nullable=False)
    key = Column(String, nullable=False)
    date = Column(Date, nullable=False, server_default=text("CURRENT_DATE"))
    user_id = Column(String, ForeignKey("users.id", ondelete='CASCADE'))
    is_active = Column(Boolean, default=True)

    user = relationship("User")
    # chat = relationship("Chat", back_populates="discussion")
    
    
    
class User_Eventchat(Base):
    __tablename__ = "user_eventchat"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, unique=True, nullable=False)
    key = Column(String, nullable=False)
    date = Column(Date, nullable=False, server_default=text("CURRENT_DATE"))
    user_id = Column(String, ForeignKey("users.id", ondelete='CASCADE'))
    is_active = Column(Boolean, default=True)

    user = relationship("User")
    # chat = relationship("Chat", back_populates="discussion")