from fastapi import APIRouter

router = APIRouter(prefix="/catalog", tags=["Catalog Sync"])


@router.get("/", summary="Get catalog info")
async def get_catalog_info():
    return {
        "name": "GymTracker Exercise Catalog",
        "version": "0.1.0",
        "description": "Comprehensive gym exercise database with muscle groups, movements, and equipment",
    }


@router.get("/stats", summary="Get catalog statistics")
async def get_catalog_stats():
    return {
        "collections": [
            {"name": "exercises", "description": "Complete exercise library"},
            {"name": "muscle_groups", "description": "Muscle group taxonomy"},
            {"name": "movement_groups", "description": "Movement pattern groups"},
            {"name": "equipment", "description": "Equipment types"},
        ]
    }
