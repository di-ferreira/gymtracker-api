from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.session import get_db
from src.services.auth_service import AuthService, AuthError
from src.schemas.auth import (
    UserCreate, UserResponse, LoginRequest, TokenResponse,
)
from src.core.dependencies import get_token_data

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
    token_data: dict = Depends(get_token_data),
    service: AuthService = Depends(get_auth_service),
):
    user_id = UUID(token_data["sub"])
    try:
        return await service.get_current_user(user_id)
    except AuthError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
