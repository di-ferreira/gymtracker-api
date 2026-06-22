from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, email: str, hashed_password: str, name: str, role: str = "user") -> User:
        user = User(email=email, hashed_password=hashed_password, name=name, role=role)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(
            select(User).filter(User.email == email)
        )
        return result.scalar_one_or_none()

    async def get_by_id(self, id: UUID) -> User | None:
        result = await self.session.execute(
            select(User).filter(User.id == id)
        )
        return result.scalar_one_or_none()

    async def list(self, skip: int = 0, limit: int = 100) -> list[User]:
        result = await self.session.execute(
            select(User).offset(skip).limit(limit)
        )
        return list(result.scalars().all())

    async def update(self, user: User, **kwargs) -> User:
        for key, value in kwargs.items():
            setattr(user, key, value)
        await self.session.commit()
        await self.session.refresh(user)
        return user
