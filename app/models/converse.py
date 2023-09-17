from sqlalchemy import Boolean, Column, ForeignKey, Text, String, Date, text,Integer,DateTime
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from config.database import Base
from models import User
    
class Converse(Base):
    __tablename__ = "converse"

    # id = Column(Integer,  primary_key=True, unique=True, index=True, nullable=False, autoincrement=True)
    id = Column(String, primary_key=True, index=True, default=str(uuid.uuid4()))
    query = Column(String , nullable=False)
    answer = Column(String, nullable=False)
    isliked = Column(Boolean, nullable=True)
    created_at = Column(DateTime, default=datetime.now, name="created_at")
    user_id = Column(String , nullable=False)
    # user_id = Column(ForeignKey("user.id", ondelete='CASCADE'))
    # user = relationship("User")