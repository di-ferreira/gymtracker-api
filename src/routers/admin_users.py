from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Security, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.session import get_db
from src.services.auth_service import AuthService, AuthError
from src.schemas.auth import UserResponse, AdminUpdateUserRequest
from src.core.dependencies import require_admin

router = APIRouter(prefix="/users", tags=["Admin - Users"])


async def get_auth_service(db: AsyncSession = Depends(get_db)):
    return AuthService(db)


@router.get("/", response_model=List[UserResponse])
async def admin_list_users(
    skip: int = 0,
    limit: int = 100,
    _: dict = Security(require_admin),
    db: AsyncSession = Depends(get_db),
):
    service = AuthService(db)
    return await service.list_users(skip=skip, limit=limit)


@router.patch("/{user_id}", response_model=UserResponse)
async def admin_update_user(
    user_id: UUID,
    in_data: AdminUpdateUserRequest,
    _: dict = Security(require_admin),
    db: AsyncSession = Depends(get_db),
):
    service = AuthService(db)
    try:
        return await service.admin_update_user(user_id, in_data)
    except AuthError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
