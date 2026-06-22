"""Catalog Sync Router for versioning and catalog management."""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from src.database.session import get_db
from src.models.exercise import CatalogVersionResponse

router = APIRouter(prefix="/catalog", tags=["Catalog Sync"])


@router.get("/", summary="Get catalog info", tags=["Catalog Sync"])
async def get_catalog_info(request: Request):
    """Get catalog version information."""
    return {
        "name": "GymTracker Exercise Catalog",
        "version": "0.1.0",
        "description": comprehensive gym exercise database with muscle groups, movements, and equipment
    }


@router.get("/stats", summary="Get catalog statistics")
async def get_catalog_stats():
    """Get general catalog statistics."""
    return {
        "collections": [
            {"name": "exercises", "description": "Complete exercise library"},
            {"name": "muscle_groups", "description": "Muscle group taxonomy"},
            {"name": "movement_groups", "description": "Movement pattern groups"},
            {"name": "equipment", "description": "Equipment types"}
        ]
    }
