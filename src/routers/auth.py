from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Security, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.session import get_db
from src.services.auth_service import AuthService, AuthError
from src.schemas.auth import (
    UserCreate, UserResponse, LoginRequest, TokenResponse,
    UpdateProfileRequest,
)
from src.core.dependencies import require_auth, get_current_user

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
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.post("/login", response_model=TokenResponse)
async def login(
    in_data: LoginRequest,
    service: AuthService = Depends(get_auth_service),
):
    try:
        return await service.login(in_data.email, in_data.password)
    except AuthError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user: UserResponse = Depends(get_current_user),
):
    return current_user


@router.patch("/me", response_model=UserResponse)
async def update_me(
    in_data: UpdateProfileRequest,
    token_data: dict = Security(require_auth),
    db: AsyncSession = Depends(get_db),
):
    service = AuthService(db)
    try:
        return await service.update_profile(UUID(token_data["sub"]), in_data)
    except AuthError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
