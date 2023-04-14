from datetime import datetime, timedelta, timezone
from typing import Union

import jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from ..models import User
from ..settings import settings
from .base import BaseService


class AuthService(BaseService):
    def __init__(self):
        super().__init__()
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def get_user(self, username):
        async with self.session.begin() as session:
            stmt = (
                select(User)
                .where(User.username == username)
                .options(selectinload(User.profile))
                .limit(1)
            )
            result = await session.execute(stmt)
            return result.scalars().first()

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def create_access_token(
        self, data: dict, expires_delta: Union[timedelta, None] = None
    ):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(days=15)
        to_encode["exp"] = expire
        return jwt.encode(to_encode, settings.JWT_KEY, algorithm=settings.ALGORITHM)

    async def authenticate(self, username: str, password: str):
        if user := await self.get_user(username):
            return (
                user
                if self.verify_password(password, user.password)  # type: ignore
                else False
            )
        else:
            return False


auth_service = AuthService()
