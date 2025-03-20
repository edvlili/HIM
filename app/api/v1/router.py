from fastapi import APIRouter

from app.api.v1.endpoints import auth, homes, items

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(homes.router, prefix="/homes", tags=["homes"])
api_router.include_router(items.router, prefix="/homes/{home_id}/items", tags=["items"]) 