from .base import BaseService
from passlib.context import CryptContext
from ..models import User, Profile
from sqlalchemy import select
from sqlalchemy.orm import selectinload

class AuthService(BaseService):

    def __init__(self):
        super().__init__()
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def get_user(self, username):
        return {
            "username": "johndoe",
            "full_name": "John Doe",
            "email": "johndoe@example.com",
            "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
            "disabled": False,
        }

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    async def authenticate(self, username: str, password: str):
        async with self.session.begin() as session:
            stmt = select(User).options(selectinload(User.profile))
            print(1111)
            await session.commit()
        if user := await self.get_user(username):
            return user if self.verify_password(password, user.get('hashed_password')) else False
        else:
            return False


auth_service = AuthService()
