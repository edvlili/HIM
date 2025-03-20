from datetime import datetime, date
from typing import Optional, Dict, List
from uuid import UUID
from pydantic import BaseModel

from app.models.item import CategoryEnum, UnitEnum, StorageEnum


class NutritionalInfo(BaseModel):
    calories: Optional[float] = None
    proteins: Optional[float] = None
    carbohydrates: Optional[float] = None
    fats: Optional[float] = None
    allergens: Optional[List[str]] = None


class ItemBase(BaseModel):
    barcode: Optional[str] = None
    name: str
    brand: Optional[str] = None
    category: CategoryEnum
    subcategory: Optional[str] = None
    quantity: float
    unit: UnitEnum
    expiration_date: Optional[date] = None
    nutritional_info: Optional[NutritionalInfo] = None
    storage: Optional[StorageEnum] = None


class ItemCreate(ItemBase):
    home_id: UUID


class ItemUpdate(ItemBase):
    pass


class ItemInDBBase(ItemBase):
    id: UUID
    home_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Item(ItemInDBBase):
    pass 