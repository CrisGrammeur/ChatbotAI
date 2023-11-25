from sqlalchemy import Boolean, Column,DateTime, ForeignKey, text, String, CHAR
from sqlalchemy.orm import relationship
from uuid import uuid4
from datetime import datetime
from config.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True, default=str(uuid4()))
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    bio = Column(String, nullable=True)
    location = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    converse = relationship("Converse", back_populates='user')
    eventconverse = relationship("eventConverse", back_populates='user')
    created_at = Column(DateTime,nullable=True, default=datetime.now, name="created_at")    
    # owner = relationship("Discussion", back_populates="user")
    # created_at = Column(DateTime, default=datetime.now, name="created_at")