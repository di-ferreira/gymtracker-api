from fastapi import APIRouter
from src.api.routers import muscle_groups, equipments, exercises, movement_groups, catalog
from src.core.config import settings

api_router = APIRouter()

# Register all domain routers
api_router.include_router(muscle_groups.router)
api_router.include_router(equipments.router)
api_router.include_router(exercises.router)
api_router.include_router(movement_groups.router)
api_router.include_router(catalog.router)
