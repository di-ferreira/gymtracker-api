from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    def __repr__(self):
        return f"<{self.__tablename__}(id={self.id})>"
