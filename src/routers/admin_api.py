from fastapi import APIRouter
from src.routers.exercises import router as exercises_router
from src.routers.equipment import router as equipment_router
from src.routers.movement_groups import router as movement_group_router
from src.routers.muscle_groups import router as muscle_group_router

admin_router = APIRouter(prefix="/catalog", tags=["Catalog Management"])


@admin_router.get(
    "/health",
    response_model=dict,
    summary="Health check for admin panel",
    tags=["Admin Health"],
)
async def admin_health_check():
    return {"status": "ok", "message": "GymTracker Catalog Admin"}


admin_router.include_router(exercises_router)
admin_router.include_router(equipment_router)
admin_router.include_router(movement_group_router)
admin_router.include_router(muscle_group_router)
