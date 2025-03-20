from sqlalchemy import Column, String, Float, Date, JSON, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.models.base import BaseModel


class CategoryEnum(str, enum.Enum):
    FOOD = "FOOD"
    BEVERAGES = "BEVERAGES"
    CLEANING = "CLEANING"
    PERSONAL_CARE = "PERSONAL_CARE"
    HOUSEHOLD = "HOUSEHOLD"
    PRODUCE = "PRODUCE"
    OTHER = "OTHER"


class UnitEnum(str, enum.Enum):
    UNITS = "UNITS"
    KG = "KG"
    G = "G"
    L = "L"
    ML = "ML"
    OZ = "OZ"
    LB = "LB"


class StorageEnum(str, enum.Enum):
    ROOM_TEMP = "ROOM_TEMP"
    REFRIGERATED = "REFRIGERATED"
    FROZEN = "FROZEN"


class Item(BaseModel):
    __tablename__ = "items"

    barcode = Column(String)
    name = Column(String, nullable=False)
    brand = Column(String)
    category = Column(Enum(CategoryEnum), nullable=False)
    subcategory = Column(String)
    quantity = Column(Float, nullable=False)
    unit = Column(Enum(UnitEnum), nullable=False)
    expiration_date = Column(Date)
    nutritional_info = Column(JSON)
    storage = Column(Enum(StorageEnum))
    home_id = Column(UUID(as_uuid=True), ForeignKey("homes.id"), nullable=False)

    # Relationships
    home = relationship("Home", back_populates="items") 