from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class _Base(DeclarativeBase):
    pass


class Base(_Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created: Mapped[datetime] = mapped_column(insert_default=func.now())
    updated: Mapped[datetime] = mapped_column(onupdate=func.now())
    deleted: Mapped[bool] = mapped_column(default=False)
