from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.session import get_db
from src.services.instruction_service import InstructionService
from src.schemas.instruction import InstructionCreate, InstructionUpdate, InstructionResponse
from src.core.errors import not_found

router = APIRouter(prefix="/exercises/{exercise_id}/instructions", tags=["Exercise Instructions"])


async def get_service(db: AsyncSession = Depends(get_db)):
    return InstructionService(db)


@router.get("/", response_model=List[InstructionResponse])
async def list_instructions(
    exercise_id: UUID,
    service: InstructionService = Depends(get_service),
):
    try:
        return await service.list_by_exercise(exercise_id)
    except ValueError as e:
        raise not_found(str(e))


@router.post("/", response_model=InstructionResponse, status_code=status.HTTP_201_CREATED)
async def create_instruction(
    exercise_id: UUID,
    in_data: InstructionCreate,
    service: InstructionService = Depends(get_service),
):
    try:
        return await service.create(exercise_id, in_data)
    except ValueError as e:
        raise not_found(str(e))


@router.patch("/{instruction_id}", response_model=InstructionResponse)
async def update_instruction(
    exercise_id: UUID,
    instruction_id: UUID,
    in_data: InstructionUpdate,
    service: InstructionService = Depends(get_service),
):
    result = await service.update(instruction_id, in_data)
    if not result:
        raise not_found("Instruction not found")
    return result


@router.delete("/{instruction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_instruction(
    exercise_id: UUID,
    instruction_id: UUID,
    service: InstructionService = Depends(get_service),
):
    if not await service.delete(instruction_id):
        raise not_found("Instruction not found")
    return None
