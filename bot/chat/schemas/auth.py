from pydantic import BaseModel
from typing import Union


class SignIn(BaseModel):
    username: str
    password: str


class SignUp(BaseModel):
    username: str
    email: str
    mobile: str
    password: str


class JWTToken(BaseModel):
    token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None
