from uuid import UUID
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.session import get_db
from src.services.auth_service import AuthService, AuthError
from src.schemas.auth import UserResponse

http_bearer = HTTPBearer()


async def require_auth(
    credentials: HTTPAuthorizationCredentials = Security(http_bearer),
) -> dict:
    try:
        return AuthService.decode_token(credentials.credentials)
    except AuthError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )


async def require_admin(
    token_data: dict = Depends(require_auth),
) -> dict:
    if token_data.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return token_data


async def get_current_user(
    token_data: dict = Depends(require_auth),
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    service = AuthService(db)
    user_id = UUID(token_data["sub"])
    try:
        return await service.get_current_user(user_id)
    except AuthError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )
