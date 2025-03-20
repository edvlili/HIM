from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class HomeBase(BaseModel):
    name: str
    address: Optional[str] = None


class HomeCreate(HomeBase):
    pass


class HomeUpdate(HomeBase):
    pass


class HomeInDBBase(HomeBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Home(HomeInDBBase):
    pass 