from sqlalchemy import Boolean, Column, ForeignKey, text, String, CHAR
from sqlalchemy.orm import relationship
from uuid import uuid4

from config.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True, default=str(uuid4()))
    name = Column(String, unique=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    bio = Column(String, nullable=True)
    location = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

    # owner = relationship("Discussion", back_populates="user")
    