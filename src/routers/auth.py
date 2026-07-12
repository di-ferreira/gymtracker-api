from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.session import get_db
from src.services.auth_service import AuthService, AuthError
from src.schemas.auth import (
    UserCreate, UserResponse, LoginRequest, TokenResponse,
)
from src.core.errors import conflict, unauthorized

router = APIRouter(prefix="/auth", tags=["Auth"])


async def get_auth_service(db: AsyncSession = Depends(get_db)):
    return AuthService(db)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    in_data: UserCreate,
    service: AuthService = Depends(get_auth_service),
):
    try:
        return await service.register(in_data)
    except AuthError as e:
        if "already registered" in str(e):
            raise conflict(str(e))
        raise unauthorized(str(e))


@router.post("/login", response_model=TokenResponse)
async def login(
    in_data: LoginRequest,
    service: AuthService = Depends(get_auth_service),
):
    try:
        return await service.login(in_data.email, in_data.password)
    except AuthError as e:
        raise unauthorized(str(e))


