from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.home import Home as HomeModel
from app.models.user import User
from app.schemas.home import Home, HomeCreate, HomeUpdate

router = APIRouter()


@router.get("/", response_model=List[Home])
def get_homes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Get all homes for current user.
    """
    return db.query(HomeModel).filter(HomeModel.user_id == current_user.id).all()


@router.post("/", response_model=Home, status_code=status.HTTP_201_CREATED)
def create_home(
    *,
    db: Session = Depends(get_db),
    home_in: HomeCreate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Create new home.
    """
    home = HomeModel(**home_in.model_dump(), user_id=current_user.id)
    db.add(home)
    db.commit()
    db.refresh(home)
    return home


@router.get("/{home_id}", response_model=Home)
def get_home(
    *,
    db: Session = Depends(get_db),
    home_id: UUID,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Get home by ID.
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


@router.put("/{home_id}", response_model=Home)
def update_home(
    *,
    db: Session = Depends(get_db),
    home_id: UUID,
    home_in: HomeUpdate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Update home.
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
    
    for field, value in home_in.model_dump(exclude_unset=True).items():
        setattr(home, field, value)
    
    db.add(home)
    db.commit()
    db.refresh(home)
    return home


@router.delete("/{home_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def delete_home(
    *,
    db: Session = Depends(get_db),
    home_id: UUID,
    current_user: User = Depends(get_current_user),
) -> None:
    """
    Delete home.
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
    
    db.delete(home)
    db.commit()
    return None 