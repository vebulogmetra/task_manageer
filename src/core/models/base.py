from uuid import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    """Base class for the models"""

    __abstract__ = True  # Do not create in database

    # Tablename as class name + "s"
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    id: Mapped[UUID] = mapped_column(
        primary_key=True, server_default=func.uuid_generate_v4()
    )
