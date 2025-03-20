from typing import Any, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.home import Home as HomeModel
from app.models.item import Item as ItemModel, CategoryEnum
from app.models.user import User
from app.schemas.item import Item, ItemCreate, ItemUpdate

router = APIRouter()


def get_home(
    db: Session,
    home_id: UUID,
    current_user: User,
) -> HomeModel:
    """
    Get home and verify ownership.
    """
    home = db.query(HomeModel).filter(
        HomeModel.id == home_id,
        HomeModel.user_id == current_user.id
    ).first()
    if not home:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Home not found",
        )
    return home


@router.get("/", response_model=List[Item])
def get_items(
    *,
    db: Session = Depends(get_db),
    home_id: UUID,
    current_user: User = Depends(get_current_user),
    category: Optional[CategoryEnum] = None,
    search: Optional[str] = None,
) -> Any:
    """
    Get all items in a home.
    """
    home = get_home(db, home_id, current_user)
    
    query = db.query(ItemModel).filter(ItemModel.home_id == home.id)
    
    if category:
        query = query.filter(ItemModel.category == category)
    
    if search:
        query = query.filter(
            ItemModel.name.ilike(f"%{search}%") |
            ItemModel.brand.ilike(f"%{search}%") |
            ItemModel.barcode.ilike(f"%{search}%")
        )
    
    return query.all()


@router.post("/", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(
    *,
    db: Session = Depends(get_db),
    home_id: UUID,
    item_in: ItemCreate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Create new item.
    """
    home = get_home(db, home_id, current_user)
    
    item = ItemModel(**item_in.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("/{item_id}", response_model=Item)
def get_item(
    *,
    db: Session = Depends(get_db),
    home_id: UUID,
    item_id: UUID,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Get item by ID.
    """
    home = get_home(db, home_id, current_user)
    
    item = db.query(ItemModel).filter(
        ItemModel.id == item_id,
        ItemModel.home_id == home.id
    ).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )
    return item


@router.put("/{item_id}", response_model=Item)
def update_item(
    *,
    db: Session = Depends(get_db),
    home_id: UUID,
    item_id: UUID,
    item_in: ItemUpdate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Update item.
    """
    home = get_home(db, home_id, current_user)
    
    item = db.query(ItemModel).filter(
        ItemModel.id == item_id,
        ItemModel.home_id == home.id
    ).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )
    
    for field, value in item_in.model_dump(exclude_unset=True).items():
        setattr(item, field, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def delete_item(
    *,
    db: Session = Depends(get_db),
    home_id: UUID,
    item_id: UUID,
    current_user: User = Depends(get_current_user),
) -> None:
    """
    Delete item.
    """
    home = get_home(db, home_id, current_user)
    
    item = db.query(ItemModel).filter(
        ItemModel.id == item_id,
        ItemModel.home_id == home.id
    ).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )
    
    db.delete(item)
    db.commit()
    return None 