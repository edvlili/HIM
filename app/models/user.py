from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)

    # Relationships
    homes = relationship("Home", back_populates="user", cascade="all, delete-orphan") 