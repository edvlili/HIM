from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Home(BaseModel):
    __tablename__ = "homes"

    name = Column(String, nullable=False)
    address = Column(String)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="homes")
    items = relationship("Item", back_populates="home", cascade="all, delete-orphan") 