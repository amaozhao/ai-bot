from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class User(Base):
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(String(32), unique=True)
    email: Mapped[str] = mapped_column(String(128), unique=True)
    mobile: Mapped[str] = mapped_column(String(32), unique=True)
    nickname: Mapped[str] = mapped_column(String(32))
    profile: Mapped["Profile"] = relationship(lazy="raise")


class Profile(Base):
    __tablename__ = "profile"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    openai_key: Mapped[str] = mapped_column(String(128))
