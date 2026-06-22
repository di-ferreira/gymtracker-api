"""Admin API Router - Comprehensive catalog management with authentication."""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from uuid import UUID
from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.session import get_db
from src.api.admin_routers.exercise import exercise_router as exercises_router
from src.api.admin_routers.equipment import equipment_router
from src.api.admin_routers.movement_groups import movement_group_router
from src.api.admin_routers.muscle_groups import muscle_group_router

# Create the main admin router
admin_router = APIRouter(prefix="/catalog", tags=["Catalog Management"])


"""@router.get("/", response_model=dict, summary="Health check for admin panel", tags=[
"Admin Health"
])
async def admin_health_check(request: Request):
    """Check if admin system is healthy."""
    return {"status": "ok", "message": "GymTracker Catalog Admin"}"""


admin_router.include_router(exercises_router)
admin_router.include_router(equipment_router)
admin_router.include_router(movement_group_router)
admin_router.include_router(muscle_group_router)
