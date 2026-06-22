from fastapi import APIRouter, Depends, Security
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from src.routers.exercises import router as exercises_router
from src.routers.equipment import router as equipment_router
from src.routers.movement_groups import router as movement_group_router
from src.routers.muscle_groups import router as muscle_group_router
from src.routers.alternatives import router as alternatives_router
from src.routers.instructions import router as instructions_router
from src.database.session import get_db
from src.core.dependencies import require_admin

admin_router = APIRouter(
    prefix="/catalog",
    tags=["Catalog Management"],
)


@admin_router.get(
    "/health",
    response_model=dict,
    summary="Health check for admin panel",
    tags=["Admin Health"],
)
async def admin_health_check(db: AsyncSession = Depends(get_db)):
    db_ok = False
    try:
        await db.execute(text("SELECT 1"))
        db_ok = True
    except Exception:
        db_ok = False
    return {
        "status": "ok" if db_ok else "degraded",
        "message": "GymTracker Catalog Admin",
        "database": "connected" if db_ok else "unreachable",
    }


admin_router.include_router(
    exercises_router, dependencies=[Security(require_admin)]
)
admin_router.include_router(
    equipment_router, dependencies=[Security(require_admin)]
)
admin_router.include_router(
    movement_group_router, dependencies=[Security(require_admin)]
)
admin_router.include_router(
    muscle_group_router, dependencies=[Security(require_admin)]
)
admin_router.include_router(
    alternatives_router, dependencies=[Security(require_admin)]
)
admin_router.include_router(
    instructions_router, dependencies=[Security(require_admin)]
)
