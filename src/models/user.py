import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean, func
from sqlalchemy import Uuid
from sqlalchemy.orm import Mapped, mapped_column
from src.database.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = Column(
        Uuid(), primary_key=True, default=uuid.uuid4
    )

    email: Mapped[str] = Column(
        String(255), nullable=False, unique=True, index=True
    )

    hashed_password: Mapped[str] = Column(
        String(255), nullable=False
    )

    name: Mapped[str] = Column(
        String(150), nullable=False
    )

    is_active: Mapped[bool] = Column(
        Boolean, default=True, nullable=False
    )

    role: Mapped[str] = Column(
        String(20), default="user", nullable=False
    )

    created_at: Mapped[datetime] = Column(
        DateTime, server_default=func.now(), nullable=False
    )

    updated_at: Mapped[datetime] = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )
