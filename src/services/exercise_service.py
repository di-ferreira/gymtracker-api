"""Service layer for Exercise operations."""

from uuid import UUID
from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from src.models.exercise import Exercise
from src.schemas.exercise import ExerciseCreate, ExerciseUpdate, ExerciseResponse, PaginationInfo
from src.repositories.exercise_repository import ExerciseRepository


class ExerciseValidationError(Exception):
    """Raised when exercise validation fails."""
    pass


class ExerciseService:
    """Exercise service business logic layer."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = ExerciseRepository(session)

    # ==================== CRUD Operations ==================== #
    
    async def create(
        self, 
        in_data: ExerciseCreate
    ) -> ExerciseResponse:
        """Create a new exercise."""
        db_obj = await self.repository.create(in_data)
        return ExerciseResponse.model_validate(db_obj)

    async def get_by_id(self, id: UUID) -> Optional[ExerciseResponse]:
        """Get exercise by ID."""
        db_obj = await self.repository.get_by_id(id)
        return ExerciseResponse.model_validate(db_obj) if db_obj else None

    async def update(
        self, 
        id: UUID,
        in_data: ExerciseUpdate
    ) -> Optional[ExerciseResponse]:
        """Update exercise by ID."""
        db_obj = await self.repository.update(id, in_data)
        return ExerciseResponse.model_validate(db_obj) if db_obj else None

    async def delete(self, id: UUID) -> bool:
        """Soft delete an exercise (mark as deleted)."""
        return await self.repository.delete(id)

    # ==================== List Operations with Pagination ==================== #
    
    async def list_exercises(
        self,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None,
        order_by: str = "name",
        order_dir: str = "asc"
    ) -> tuple[List[ExerciseResponse], PaginationInfo]:
        """
        List exercises with pagination and filtering.
        
        Args:
            skip: Number of items to skip (for pagination)
            limit: Number of items per page (max 100)
            filters: Filter criteria dict
            order_by: Field to sort by
            order_dir: Sort direction ('asc' or 'desc')
        
        Returns:
            Tuple of (items, PaginationInfo)
        """
        exercises, total = await self.repository.list_exercises(skip, limit, filters)
        total_pages = (total + limit - 1) // limit
        
        pagination_info = PaginationInfo(
            page=(skip // limit) + 1,
            per_page=limit,
            total_pages=total_pages,
            has_previous=(skip > 0),
            has_next=(total_pages > ((skip // limit) + 1)),
            total_items=total
        )
        
        return exercises, pagination_info

    # ==================== Search Operations ==================== #
    
    async def search_exercises(
        self,
        query: str,
        fuzzy: bool = False,
        limit: int = 50,
        order_by: Optional[str] = None
    ) -> List[ExerciseResponse]:
        """
        Search exercises by name or slug.
        
        Args:
            query: Search query string
            fuzzy: Whether to enable fuzzy matching
            limit: Maximum results (default 50)
            order_by: Sort field (optional)
        
        Returns:
            List of exercise responses
        """
        exercises, _ = await self.repository.search_exercises(
            query.lower(), 
            limit, 
            order_by or "name"
        )
        return [ExerciseResponse.model_validate(ex) for ex in exercises]

    # ==================== Relation Operations ==================== #
    
    async def delete_equipment(self, exercise_id: UUID, equipment_id: UUID) -> bool:
        """Remove equipment from exercise relationship."""
        result = await self.repository.delete_equipment(exercise_id, equipment_id)
        return result

    async def add_equipment(
        self, 
        exercise_id: UUID,
        equipment_id: UUID,
        usage_note: Optional[str] = None
    ) -> Optional[UUID]:
        """Add equipment to exercise relationship."""
        new_id = await self.repository.add_equipment(
            exercise_id, 
            equipment_id,
            usage_note
        )
        return new_id

    async def get_exercise_with_relations(self, id: UUID) -> Optional[Any]:
        """Get exercise with all its relationships (equipment, instructions)."""
        db_obj = await self.repository.get_by_id(id)
        if not db_obj:
            return None
        
        # Load equipment
        eq_query = await self.session.execute(
            select(Equipment)
            .join(ExerciseEquipment, ExerciseEquipment.equipment_id == Equipment.id)
            .filter(ExerciseEquipment.exercise_id == id)
        )
        
        exercises = [ExerciseResponse.model_validate(ex) for ex in 
                     (await self.repository.get_all(limit=0))[:5]]
