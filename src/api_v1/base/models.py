from uuid import UUID

from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    __abstract__ = True  # Do not create in database

    # Tablename as class name + "s"
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    id: Mapped[UUID] = mapped_column(
        primary_key=True, server_default=func.gen_random_uuid()
    )

    def as_dict(self):
        """Sqlalchemy object to dict"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
