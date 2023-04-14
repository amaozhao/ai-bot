from fastapi import HTTPException, status
from passlib.context import CryptContext
from sqlalchemy import or_, select
from sqlalchemy.orm import selectinload

from ..models import User
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
            return user

    async def check(self, username, email, mobile):
        async with self.session.begin() as session:
            stmt = (
                select(User)
                .filter(
                    or_(
                        User.username == username,
                        User.email == email,
                        User.mobile == mobile,
                    )
                )
                .options(selectinload(User.profile))
                .limit(1)
            )
            result = await session.execute(stmt)
            return result.scalars().first()

    async def get(self, username=None, email=None, mobile=None):
        if not (username or email or mobile):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        async with self.session.begin() as session:
            stmt = (
                select(User)
                .filter(
                    or_(
                        User.username == username,
                        User.email == email,
                        User.mobile == mobile,
                    )
                )
                .options(selectinload(User.profile))
                .limit(1)
            )
            result = await session.execute(stmt)
            return result.scalars().first()

    async def update_password(self, username, password: str):
        user = await self.get(username=username)
        async with self.session.begin() as session:
            stmt = (
                select(User)
                .filter(User.username == username)
                .options(selectinload(User.profile))
                .limit(1)
            )
            result = await session.execute(stmt)
            if user := result.scalars().first():
                user.password = self.pwd_context.hash(password)
                await session.commit()
                return user
            return None


user_service = UserService()
