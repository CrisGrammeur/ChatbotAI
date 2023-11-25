from sqlalchemy import Boolean, Column, ForeignKey, Text, String, Date, text,Integer,DateTime
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from config.database import Base
from models import User
    
class eventConverse(Base):
    __tablename__ = "eventconverse"

    # id = Column(Integer,  primary_key=True, unique=True, index=True, nullable=False, autoincrement=True)
    id = Column(String, primary_key=True, index=True, default=str(uuid.uuid4()))
    user_chat_id = Column(String, nullable=False)
    user_name = Column(String, nullable=False)
    query = Column(String , nullable=False)
    answer = Column(String, nullable=False)
    dislike_reason = Column(String, nullable=True, default=None)
    isliked = Column(Boolean, nullable=True)
    raison = Column(String, nullable=True, default=None)
    created_at = Column(DateTime, default=datetime.now, name="created_at")
    user_id = Column(String,ForeignKey("users.id", ondelete='CASCADE'))
    user = relationship("User", back_populates='eventconverse')
    is_deleted = Column(Boolean, nullable=False, default=False)
    is_active = Column(Boolean, nullable=False, default=True)
    # relationship
    # user_chat = relationship("User_chat", back_populates="converse")