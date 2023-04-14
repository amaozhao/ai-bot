from datetime import datetime, timedelta, timezone
from typing import Union

import jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from ..models import User
from ..settings import settings
from .base import BaseService


class UserService(BaseService):
    def __init__(self):
        super().__init__()
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def create(self, username, password, email, mobile):
        async with self.session.begin() as session:
            user = User(
                username=username,
                email=email,
                mobile=mobile,
                password=self.pwd_context.hash(password),
            )
            session.add(user)
            await session.commit()
            print(self.pwd_context.hash(password), 1111)
            return user

    async def get(self, username):
        async with self.session.begin() as session:
            stmt = (
                select(User)
                .where(User.username == username)
                .options(selectinload(User.profile))
                .limit(1)
            )
            result = await session.execute(stmt)
            return result.scalars().first()


user_service = UserService()
