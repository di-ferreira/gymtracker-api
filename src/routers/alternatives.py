from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.session import get_db
from src.services.alternative_service import AlternativeService
from src.schemas.instruction import AlternativeCreate, AlternativeResponse

router = APIRouter(prefix="/exercises/{exercise_id}/alternatives", tags=["Exercise Alternatives"])


async def get_service(db: AsyncSession = Depends(get_db)):
    return AlternativeService(db)


@router.get("/", response_model=List[AlternativeResponse])
async def list_alternatives(
    exercise_id: UUID,
    service: AlternativeService = Depends(get_service),
):
    try:
        return await service.list_by_exercise(exercise_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/", response_model=AlternativeResponse, status_code=status.HTTP_201_CREATED)
async def create_alternative(
    exercise_id: UUID,
    in_data: AlternativeCreate,
    service: AlternativeService = Depends(get_service),
):
    try:
        return await service.create(exercise_id, in_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{alternative_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_alternative(
    exercise_id: UUID,
    alternative_id: UUID,
    service: AlternativeService = Depends(get_service),
):
    if not await service.delete(alternative_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alternative not found")
    return None
