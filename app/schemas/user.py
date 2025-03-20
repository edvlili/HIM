from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    username: str
    first_name: str
    last_name: str


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    hashed_password: str 