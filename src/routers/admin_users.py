from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, Security, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.session import get_db
from src.services.auth_service import AuthService, AuthError
from src.schemas.auth import UserResponse, AdminCreateUserRequest, AdminUpdateUserRequest
from src.core.dependencies import require_admin
from src.core.errors import not_found, bad_request

router = APIRouter(prefix="/users", tags=["Admin - Users"])


async def get_auth_service(db: AsyncSession = Depends(get_db)):
    return AuthService(db)


@router.post("/", response_model=UserResponse, status_code=201)
async def admin_create_user(
    in_data: AdminCreateUserRequest,
    _: dict = Security(require_admin),
    db: AsyncSession = Depends(get_db),
):
    service = AuthService(db)
    try:
        return await service.admin_create_user(in_data)
    except AuthError as e:
        if "already registered" in str(e):
            from src.core.errors import conflict
            raise conflict(str(e))
        from src.core.errors import bad_request
        raise bad_request(str(e))


@router.get("/", response_model=List[UserResponse])
async def admin_list_users(
    skip: int = 0,
    limit: int = 100,
    _: dict = Security(require_admin),
    db: AsyncSession = Depends(get_db),
):
    service = AuthService(db)
    return await service.list_users(skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserResponse)
async def admin_get_user(
    user_id: UUID,
    _: dict = Security(require_admin),
    db: AsyncSession = Depends(get_db),
):
    service = AuthService(db)
    try:
        return await service.get_user_by_id(user_id)
    except AuthError as e:
        raise not_found(str(e))


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
        raise not_found(str(e))


@router.delete("/{user_id}", status_code=204)
async def admin_delete_user(
    user_id: UUID,
    permanent: bool = Query(False, description="Hard delete the user from database"),
    _: dict = Security(require_admin),
    db: AsyncSession = Depends(get_db),
):
    service = AuthService(db)
    try:
        await service.admin_delete_user(user_id, permanent=permanent)
    except AuthError as e:
        raise not_found(str(e))
    return None
