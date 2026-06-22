from uuid import UUID
from datetime import datetime, timedelta, timezone
import bcrypt
import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.config import settings
from src.repositories.user_repository import UserRepository
from typing import List
from src.schemas.auth import (
    UserCreate, UserResponse, TokenResponse,
    UpdateProfileRequest, AdminUpdateUserRequest,
)


class AuthError(Exception):
    pass


class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = UserRepository(session)

    def _hash_password(self, password: str) -> str:
        return bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

    def _verify_password(self, password: str, hashed: str) -> bool:
        return bcrypt.checkpw(
            password.encode("utf-8"), hashed.encode("utf-8")
        )

    def _create_token(self, user_id: UUID, role: str = "user") -> str:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        payload = {
            "sub": str(user_id),
            "role": role,
            "exp": expire,
        }
        return jwt.encode(
            payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )

    @staticmethod
    def decode_token(token: str) -> dict:
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            return payload
        except jwt.PyJWTError as e:
            raise AuthError(str(e))

    async def register(self, in_data: UserCreate, role: str = "user") -> UserResponse:
        existing = await self.repository.get_by_email(in_data.email)
        if existing:
            raise AuthError("Email already registered")

        hashed = self._hash_password(in_data.password)
        user = await self.repository.create(
            email=in_data.email,
            hashed_password=hashed,
            name=in_data.name,
            role=role,
        )
        return UserResponse.model_validate(user)

    async def login(self, email: str, password: str) -> TokenResponse:
        user = await self.repository.get_by_email(email)
        if not user:
            raise AuthError("Invalid email or password")

        if not self._verify_password(password, user.hashed_password):
            raise AuthError("Invalid email or password")

        if not user.is_active:
            raise AuthError("Account is inactive")

        token = self._create_token(user.id, user.role)
        return TokenResponse(access_token=token)

    async def get_current_user(self, user_id: UUID) -> UserResponse:
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise AuthError("User not found")
        return UserResponse.model_validate(user)

    async def list_users(self, skip: int = 0, limit: int = 100) -> List[UserResponse]:
        users = await self.repository.list(skip=skip, limit=limit)
        return [UserResponse.model_validate(u) for u in users]

    async def update_profile(self, user_id: UUID, data: UpdateProfileRequest) -> UserResponse:
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise AuthError("User not found")

        kwargs = {}
        if data.name is not None:
            kwargs["name"] = data.name

        if data.new_password:
            if not data.current_password:
                raise AuthError("Current password is required to set a new password")
            if not self._verify_password(data.current_password, user.hashed_password):
                raise AuthError("Current password is incorrect")
            kwargs["hashed_password"] = self._hash_password(data.new_password)

        user = await self.repository.update(user, **kwargs)
        return UserResponse.model_validate(user)

    async def admin_update_user(self, user_id: UUID, data: AdminUpdateUserRequest) -> UserResponse:
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise AuthError("User not found")

        kwargs = {}
        if data.name is not None:
            kwargs["name"] = data.name
        if data.role is not None:
            kwargs["role"] = data.role
        if data.is_active is not None:
            kwargs["is_active"] = data.is_active

        user = await self.repository.update(user, **kwargs)
        return UserResponse.model_validate(user)
