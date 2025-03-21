from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.base import Base
from app.db.session import engine


def init_db() -> None:
    Base.metadata.create_all(bind=engine) 