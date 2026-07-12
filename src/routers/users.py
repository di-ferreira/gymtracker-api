from uuid import UUID
from fastapi import APIRouter, Depends, Security, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.session import get_db
from src.services.auth_service import AuthService, AuthError
from src.schemas.auth import UserResponse, UpdateProfileRequest
from src.core.dependencies import require_auth
from src.core.errors import unauthorized, bad_request, not_found

router = APIRouter(prefix="/users", tags=["Users"])


async def get_auth_service(db: AsyncSession = Depends(get_db)):
    return AuthService(db)


@router.get("/me", response_model=UserResponse)
async def get_me(
    token_data: dict = Security(require_auth),
    service: AuthService = Depends(get_auth_service),
):
    return await service.get_current_user(UUID(token_data["sub"]))


@router.patch("/me", response_model=UserResponse)
async def update_me(
    in_data: UpdateProfileRequest,
    token_data: dict = Security(require_auth),
    service: AuthService = Depends(get_auth_service),
):
    try:
        return await service.update_profile(UUID(token_data["sub"]), in_data)
    except AuthError as e:
        raise bad_request(str(e))


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_me(
    token_data: dict = Security(require_auth),
    service: AuthService = Depends(get_auth_service),
):
    try:
        await service.delete_own_account(UUID(token_data["sub"]))
    except AuthError as e:
        raise not_found(str(e))
    return None
