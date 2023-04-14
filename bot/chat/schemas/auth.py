from typing import Union

from pydantic import BaseModel, EmailStr, validator


class SignIn(BaseModel):
    username: str
    password: str


class SignUp(BaseModel):
    username: str
    email: EmailStr
    mobile: str
    password1: str
    password2: str

    @validator("password2")
    def passwords_match(cls, v, values, **kwargs):
        if "password1" in values and v != values["password1"]:
            raise ValueError("passwords do not match")
        return v

    @validator("username")
    def username_alphanumeric(cls, v):
        assert v.isalnum(), "must be alphanumeric"
        return v


class JWTToken(BaseModel):
    token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None
