from sqlalchemy import Boolean, Column, ForeignKey, text, String, Date
from sqlalchemy.orm import relationship
from uuid import uuid4

from config.database import Base

class Discussion(Base):
    __tablename__ = "discussions"

    id = Column(String, primary_key=True, index=True, default=str(uuid4()))
    title = Column(String, nullable=False)
    date = Column(Date, nullable=False, server_default=text("CURRENT_DATE"))
    user_id = Column(String, ForeignKey("users.id", ondelete='CASCADE'))
    is_active = Column(Boolean, default=True)

    user = relationship("User")
    # chat = relationship("Chat", back_populates="discussion")